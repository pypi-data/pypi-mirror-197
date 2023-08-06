from base64 import b64decode
from importlib.machinery import PathFinder
from os import path
from pathlib import Path
import json
import os
import re
import sys
import zlib
import click
from kubeconfig import KubeConfig
import yaml
import requests
import base64
import datetime
import hashlib


class CheckException(Exception):
    def __init__(self, mitigation):
        self._mitigation = mitigation

    def mitigation(self):
        return self._mitigation


class ModuleResolutionException(CheckException):
    def __init__(self, module_name, mitigation=None):
        super().__init__(mitigation)
        self.module_name = module_name
        self.package_paths = [p for p in sys.path if p.endswith("site-packages")]

    def __str__(self):
        return "Unable to resolve module '{}'.".format(self.module_name)


class InstallValidationException(CheckException):
    def __init__(self, message, mitigation=None):
        super().__init__(mitigation)
        self.message = message

    def __str__(self):
        return self.message


NO_METAFLOW_INSTALL_MESSAGE = "Resolution of 'metaflow' module succeeded but no Metaflow installation was detected."

EXISTING_METAFLOW_MESSAGE = """It seems that there is an existing Metaflow package on your workstation which conflicts with
the Outerbounds platform.


To remove that package, please try `python -m pip uninstall metaflow -y` or reach out to Outerbounds support.
After uninstalling the Metaflow package, please reinstall the Outerbounds package using `python -m pip
install outerbounds --force`.

As always, please reach out to Outerbounds support for any questions."""

MISSING_EXTENSIONS_MESSAGE = (
    "The Outerbounds Platform extensions for Metaflow was not found."
)

BAD_EXTENSION_MESSAGE = (
    "Mis-installation of the Outerbounds Platform extension package has been detected."
)


class Narrator:
    def __init__(self, verbose):
        self.verbose = verbose

    def announce_section(self, name):
        if not self.verbose:
            click.secho("Validating {}...".format(name), nl=False)

    def section_ok(self):
        if not self.verbose:
            click.secho("\U0001F600")

    def section_not_ok(self):
        if not self.verbose:
            click.secho("\U0001F641")

    def announce_check(self, name):
        if self.verbose:
            click.secho("Checking {}...".format(name), nl=False)

    def ok(self, force=False):
        if self.verbose or force:
            click.secho("OK", fg="green")

    def not_ok(self, reason=None, force=False):
        if self.verbose or force:
            if reason is None:
                click.secho("NOT OK", fg="red")
            else:
                message = click.style("NOT OK", fg="red")
                message = "{} {}".format(
                    message, click.style("(" + reason + ")", fg="white")
                )
                click.secho(message)

    def show_error(self, err):
        if self.verbose:
            click.echo("")
            click.secho(str(err))
            mitigation = err.mitigation()
            if mitigation is not None:
                click.secho(mitigation, bold=True)


class Checker:
    def check(self):
        pass


class InstallChecker(Checker):
    def __init__(self, narrator):
        self.narrator = narrator

    def check(self):
        try:
            self.narrator.announce_section("installed packages")
            self.narrator.announce_check("Outerbounds Metaflow package")
            self.check_ob_metaflow()
            self.narrator.ok()

            self.narrator.announce_check("Outerbounds Platform extensions package")
            self.check_ob_extension()
            self.narrator.ok()
            return True
        except CheckException as e:
            self.narrator.not_ok()
            self.narrator.show_error(e)
            return False

    def check_ob_metaflow(self):
        spec = PathFinder.find_spec("metaflow")
        # We can't resolve metaflow module.
        if spec is None:
            raise ModuleResolutionException("metaflow")
        # We can resolve the module but we need to
        # make sure we're getting it from the correct
        # package.
        basedir = Path(path.join(path.dirname(spec.origin), ".."))
        # Next, let's check for parallel installations of ob-metaflow
        # and OSS metaflow. This can cause problems because they
        # overwrite each other.
        found = list(basedir.glob("metaflow-*.dist-info"))
        if len(found) > 0:
            # We found an existing OSS Metaflow install.
            raise InstallValidationException(EXISTING_METAFLOW_MESSAGE)
        # For completeness, let's verify ob_metaflow is really installed.
        # Should never get here since importing Metaflow's vendored version of click
        # would've failed much earlier on.
        found = list(basedir.glob("ob_metaflow-*.dist-info"))
        if len(found) == 0:
            raise InstallValidationException(
                NO_METAFLOW_INSTALL_MESSAGE,
                mitigation="Please reinstall the Outerbounds package using `python -m pip install outerbounds --force`.",
            )

    def check_ob_extension(self):
        spec = PathFinder.find_spec("metaflow")
        basedir = Path(path.join(path.dirname(spec.origin), ".."))
        # Metaflow install looks fine. Let's verify the correct extensions were installed.
        extensions = Path(basedir, "metaflow_extensions", "outerbounds")
        # Outerbounds extensions not found at all
        if not extensions.exists():
            raise InstallValidationException(
                MISSING_EXTENSIONS_MESSAGE,
                mitigation="""Please remove any existing Metaflow installations and reinstall the Outerbounds
                package using `python -m pip install outerbounds --force`.""",
            )
        subdirs = [
            d.name
            for d in extensions.glob("*")
            if d.is_dir() and not d.name.startswith("__")
        ]
        subdirs.sort()
        if subdirs != ["config", "plugins", "toplevel"]:
            raise InstallValidationException(
                BAD_EXTENSION_MESSAGE,
                mitigation="Please reinstall the Outerbounds package using `python -m pip install outerbounds --force`.",
            )


class ConfigEntrySpec:
    def __init__(self, name, expr, expected=None):
        self.name = name
        self.expr = re.compile(expr)
        self.expected = expected


def get_config_specs():
    return [
        ConfigEntrySpec("METAFLOW_DATASTORE_SYSROOT_S3", "s3://[a-z0-9\-]+/metaflow"),
        ConfigEntrySpec("METAFLOW_DATATOOLS_S3ROOT", "s3://[a-z0-9\-]+/data"),
        ConfigEntrySpec("METAFLOW_DEFAULT_AWS_CLIENT_PROVIDER", "obp", expected="obp"),
        ConfigEntrySpec("METAFLOW_DEFAULT_DATASTORE", "s3", expected="s3"),
        ConfigEntrySpec("METAFLOW_DEFAULT_METADATA", "service", expected="service"),
        ConfigEntrySpec(
            "METAFLOW_KUBERNETES_NAMESPACE", "jobs\-default", expected="jobs-default"
        ),
        ConfigEntrySpec("METAFLOW_KUBERNETES_SANDBOX_INIT_SCRIPT", "eval \$\(.*"),
        ConfigEntrySpec("METAFLOW_SERVICE_AUTH_KEY", "[a-zA-Z0-9!_\-\.]+"),
        ConfigEntrySpec("METAFLOW_SERVICE_URL", "https://metadata\..*"),
        ConfigEntrySpec("METAFLOW_UI_URL", "https://ui\..*"),
        ConfigEntrySpec("OBP_AUTH_SERVER", "auth\..*"),
    ]


class ConfigurationChecker(Checker):
    def __init__(self, narrator):
        self.narrator = narrator

    def check(self):
        self.narrator.announce_section("local Metaflow config")
        from metaflow import metaflow_config_funcs

        has_err = False
        config = metaflow_config_funcs.init_config()
        for spec in get_config_specs():
            self.narrator.announce_check("config entry " + spec.name)
            if spec.name not in config:
                if not has_err:
                    has_err = True
                reason = "Missing"
                if spec.expected is not None:
                    reason = "".join([reason, ", expected '{}'".format(spec.expected)])
                self.narrator.not_ok(reason=reason)
            else:
                v = config[spec.name]
                if spec.expr.fullmatch(v) is None:
                    if not has_err:
                        has_err = True
                    if spec.name.find("AUTH") == -1:
                        reason = "Have '{}'".format(v)
                        if spec.expected is not None:
                            reason += ", expected '{}'".format(spec.expected)
                    else:
                        reason = "Bad value"
                    self.narrator.not_ok(reason=reason)
                else:
                    self.narrator.ok()
        if has_err:
            self.narrator.section_not_ok()
        else:
            self.narrator.section_ok()
        return not has_err


def read_input(encoded):
    if encoded == "-":
        return "".join(sys.stdin.readlines()).replace("\n", "")
    else:
        return encoded


def to_unicode(x):
    if isinstance(x, bytes):
        return x.decode("utf-8")
    else:
        return str(x)


class ConfigurationWriter:
    def __init__(self, encoded_config, out_dir, profile):
        self.existing = dict()
        self.encoded_config = read_input(encoded_config)
        self.decoded_config = None
        self.out_dir = out_dir
        self.profile = profile

    def decode(self):
        compressed = b64decode(bytes(self.encoded_config, "UTF-8"))
        uncompressed = zlib.decompress(compressed)
        self.decoded_config = json.loads(to_unicode(uncompressed))

    def path(self):
        if self.profile == "":
            return path.join(self.out_dir, "config.json")
        else:
            return path.join(self.out_dir, "config_{}.json".format(self.profile))

    def display(self):
        # Create a copy so we can use the real config later, possibly
        display_config = dict()
        for k in self.decoded_config.keys():
            # Replace any auth sensitive bits with placeholder values for security
            if k.find("AUTH_KEY") > -1 or k.find("AUTH_TOKEN") > -1:
                display_config[k] = "*****"
            else:
                display_config[k] = self.decoded_config[k]
        click.echo(json.dumps(display_config, indent=4))

    def confirm_overwrite(self):
        return self.confirm_overwrite_config(self.path())

    def write_config(self):
        config_path = self.path()
        # TODO config contains auth token - restrict file/dir modes
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        self.existing.update(self.decoded_config)
        with open(config_path, "w") as fd:
            json.dump(self.existing, fd, indent=4)

    def confirm_overwrite_config(self, config_path):
        if os.path.exists(config_path):
            if not click.confirm(
                click.style(
                    "We found an existing configuration for your "
                    + "profile. Do you want to replace the existing "
                    + "configuration?",
                    fg="red",
                    bold=True,
                )
            ):
                click.secho(
                    "You can configure a different named profile by using the "
                    "--profile argument. You can activate this profile by setting "
                    "the environment variable METAFLOW_PROFILE to the named "
                    "profile.",
                    fg="yellow",
                )
                return False
        return True


@click.group(help="The Outerbounds Platform CLI", no_args_is_help=True)
def cli(**kwargs):
    pass


@cli.command(help="Check packages and configuration for common errors")
@click.option(
    "-n",
    "--no-config",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip validating local Metaflow configuration",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose output")
def check(no_config, verbose):
    narrator = Narrator(verbose)
    ic = InstallChecker(narrator)
    icr = ic.check()
    ccr = True
    if icr:
        narrator.section_ok()
    else:
        narrator.section_not_ok()
    if icr:
        if not no_config:
            cc = ConfigurationChecker(narrator)
            ccr = cc.check()
    if (not icr or not ccr) and not verbose:
        click.echo("Run 'outerbounds check -v' to see more details.")
        sys.exit(1)


@cli.command(help="Decode Outerbounds Platform configuration strings")
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="Configure a named profile. Activate the profile by setting "
    "`METAFLOW_PROFILE` environment variable.",
)
@click.option(
    "-e",
    "--echo",
    is_flag=True,
    help="Print decoded configuration to stdout",
)
@click.argument("encoded_config", required=True)
def configure(encoded_config=None, config_dir=None, profile=None, echo=None):
    writer = ConfigurationWriter(encoded_config, config_dir, profile)
    try:
        writer.decode()
    except:
        click.secho("Decoding the configuration text failed.", fg="red")
        sys.exit(1)
    try:
        if echo == True:
            writer.display()
        if writer.confirm_overwrite():
            writer.write_config()
    except Exception as e:
        click.secho("Writing the configuration file '{}' failed.".format(writer.path()))
        click.secho("Error: {}".format(str(e)))


def get_k8s_token_response(config_dir, profile):
    config_path = path.join(config_dir, "config.json")
    if profile != "":
        config_path = path.join(config_dir, "config_{}.json".format(profile))
    with open(config_path) as json_file:
        config = json.load(json_file)
        metaflow_token = config["METAFLOW_SERVICE_AUTH_KEY"]

        if config["OBP_AUTH_SERVER"].startswith("https://"):
            auth_endpoint = config["OBP_AUTH_SERVER"]
        else:
            auth_endpoint = "https://{}".format(config["OBP_AUTH_SERVER"])

        if auth_endpoint.endswith("/"):
            auth_endpoint = auth_endpoint[:-1]

        generate_token_url = "{}/generate/k8s".format(auth_endpoint)
        headers = {"x-api-key": metaflow_token}
        response = requests.get(generate_token_url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            raise Exception(
                "Failed to get response. Error: {}".format(response.status_code)
            )


@cli.command(help="Generate a token to use your cloud workstation")
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def generate_workstation_token(config_dir=None, profile=None):
    try:
        token = get_k8s_token_response(config_dir, profile)["token"]
        token_data = base64.b64decode(token.split(".")[1] + "==")
        exec_creds = {
            "kind": "ExecCredential",
            "apiVersion": "client.authentication.k8s.io/v1beta1",
            "spec": {},
            "status": {
                "token": token,
                "expirationTimestamp": datetime.datetime.fromtimestamp(
                    json.loads(token_data)["exp"], datetime.timezone.utc
                ).isoformat(),
            },
        }
        click.echo(json.dumps(exec_creds))
    except Exception as e:
        click.secho("Failed to generate workstation token.", fg="red")
        click.secho("Error: {}".format(str(e)))


@cli.command(help="Configure a cloud workstation")
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="The named metaflow profile in which your workstation exists",
)
def configure_cloud_workstation(config_dir=None, profile=None):
    k8s_response = get_k8s_token_response(config_dir, profile)
    token_data = base64.b64decode(k8s_response["token"].split(".")[1] + "==")
    ws_namespace = "ws-{}".format(
        hashlib.md5(bytes(json.loads(token_data)["username"], "utf-8")).hexdigest()
    )

    kube_config_path = path.expanduser(os.environ.get("KUBECONFIG", "~/.kube/config"))
    kube_config = KubeConfig(kube_config_path)
    kube_config.set_context(
        "outerbounds-workstations", "outerbounds-cluster", ws_namespace, "obp-user"
    )

    kube_config.set_cluster(
        "outerbounds-cluster",
        server=k8s_response["endpoint"],
        insecure_skip_tls_verify=True,
    )

    with open(kube_config_path, "r") as f:
        kube_yaml = yaml.safe_load(f)

    gen_creds_args = ["generate-workstation-token"]
    if profile != "":
        gen_creds_args.append("--profile")
        gen_creds_args.append(profile)

    gen_creds_args.append("--config-dir")
    gen_creds_args.append(config_dir)

    user_exec_creds = {
        "exec": {
            "apiVersion": "client.authentication.k8s.io/v1beta1",
            "command": "outerbounds",
            "args": gen_creds_args,
            "env": None,
            "interactiveMode": "Never",
            "provideClusterInfo": False,
        }
    }

    user_updated = False

    if kube_yaml["users"] is None:
        kube_yaml["users"] = []

    for user in kube_yaml["users"]:
        if user["name"] == "obp-user":
            user["user"] = user_exec_creds
            user_updated = True

    if not user_updated:
        kube_yaml["users"].append({"name": "obp-user", "user": user_exec_creds})

    with open(kube_config_path, "w") as f:
        yaml.safe_dump(kube_yaml, f)

    kube_config.use_context("outerbounds-workstations")
