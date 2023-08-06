"""Command line tools for the web."""

import inspect
import json
import logging
import pathlib
import time
import webbrowser

import gevent
import txt
import webagt
from rich.pretty import pprint

import web
import web.host
from web.host import console, providers

__all__ = ["main"]


main = txt.application("web", web.__doc__)
config_file = pathlib.Path("~/.webint").expanduser()


def get_config():
    """Get configuration."""
    try:
        with config_file.open() as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}
    return config


def update_config(**items):
    """Update configuration."""
    config = get_config()
    config.update(**items)
    with config_file.open("w") as fp:
        json.dump(config, fp, indent=2, sort_keys=True)
        fp.write("\n")
    return get_config()


@main.register()
class Apps:
    """Show installed web apps."""

    def run(self, stdin, log):
        for pkg, apps in web.get_apps().items():
            for name, _, ns, obj in apps:
                print(f"{name} {ns}:{obj[0]}")
        return 0


@main.register()
class Fnord:
    def run(self, stdin, log):
        # import asyncio
        # asyncio.run(web.serve("web:abba", port=9999))
        web.StandaloneServer(web.abba, 9999).run()


@main.register()
class Run:
    """Run a web app locally."""

    def setup(self, add_arg):
        add_arg("app", help="name of web application")
        add_arg("--port", help="port to serve on")
        add_arg("--socket", help="file socket to serve on")
        add_arg("--watch", default=".", help="directory to watch for changes")

    def run(self, stdin, log):
        import asyncio

        if self.port:
            asyncio.run(web.serve(self.app, port=self.port, watch_dir=self.watch))
        elif self.socket:
            asyncio.run(web.serve(self.app, socket=self.socket, watch_dir=self.watch))
        else:
            print("must provide a port or a socket")
            return 1
        return 0

        # for pkg, apps in web.get_apps().items():
        #     for name, _, ns, obj in apps:
        #         if self.app == name:
        #             web.serve(ns, obj)
        #             return 0
        # return 1


def get_providers(provider_type):
    return [
        name.lower()
        for name, obj in inspect.getmembers(providers, inspect.isclass)
        if issubclass(obj, provider_type) and obj is not provider_type
    ]


@main.register()
class Config:
    """Config your environments."""

    def setup(self, add_arg):
        add_arg("token", help="API access token")
        add_arg(
            "--host",
            choices=get_providers(providers.Host),
            help="machine host",
        )
        add_arg(
            "--registrar",
            choices=get_providers(providers.Registrar),
            help="domain registrars",
        )

    def run(self, stdin, log):
        if self.host:
            update_config(host=self.host, host_token=self.token)
        elif self.registrar:
            update_config(registrar=self.registrar, registrar_token=self.token)
        return 0


@main.register()
class Bootstrap:
    """Bootstrap a website."""

    def setup(self, add_arg):
        add_arg("website", help="name of website")
        add_arg("package", help="name of PyPI package to install")
        add_arg("app", help="name of web app to run")
        add_arg("--domain", help="domain name of website")

    def run(self, stdin, log):
        logging.basicConfig(
            level=logging.DEBUG,
            filename="debug.log",
            filemode="w",
            force=True,
            format="%(levelname)s:%(asctime)s:%(name)s:%(message)s",
        )
        config = get_config()

        if config["host"] == "digitalocean":
            host = providers.DigitalOcean(config["host_token"])
        elif config["host"] == "linode":
            host = providers.Linode(config["host_token"])
        else:
            console.print(f"Host {config['host']} not available.")
            return 1

        # if config["registrar"] == "dynadot":
        #     registrar = providers.Dynadot(config["registrar_token"])
        # elif config["registrar"] == "linode":
        #     registrar = providers.Linode(config["registrar_token"])
        # else:
        #     console.print(f"Registrar {config['registrar']} not available.")
        #     return 1

        secret = web.nbrandom(4)
        machines = config.get("machines", {})
        versions = web.host.Machine.versions
        start_time = time.time()
        total_time = 14
        with console.status(
            f"[bold green]around {total_time} minutes remaining"
        ) as status:

            def update_status():
                while True:
                    remaining_time = total_time - round((time.time() - start_time) / 60)
                    if remaining_time < 1:
                        status.update("Finishing up..")
                        return
                    status.update(
                        f"[bold green]around {remaining_time} minutes remaining"
                    )
                    gevent.sleep(1)

            gevent.spawn(update_status)

            console.print(f"Spawning virtual machine at {host.__class__.__name__}")
            machine = web.host.spawn_machine(self.website, host)
            console.print("Updating system")
            machine._apt("update")
            console.print("Installing firewall")
            machine._apt("install -yq ufw")
            machine.open_ports(22)
            console.print("Installing system software")
            machine.setup_machine()
            # TODO console.print("Starting to mine for onion")
            console.print("Installing python")
            machine.setup_python()
            console.print("Installing tor")
            machine.setup_tor()
            # XXX machine = web.host.Machine("147.182.248.38", "root", "gaea_key")
            # XXX machine.onion = (
            # XXX     "hxpcvad6txrivhondry6htgmlc2idrxz37ofyobe7ynxpdxd7xdn5sid.onion"
            # XXX )
            console.print("Installing nginx")
            machine.setup_nginx()
            console.print(f"Installing application: {self.app} of {self.package}")
            machine.setup_app(self.package, self.app, config["host_token"], secret)
            # TODO console.print("Configuring domain name")
            time.sleep(2)
        console.rule(
            f"[green]Bootstrapped {self.package} ({self.app}) at {machine.address}"
        )
        webbrowser.open(f"https://{machine.address}?secret={secret}")
        machines[self.website] = machine.address
        update_config(machines=machines)
        return 0


@main.register()
class Host:
    """Manage your host."""

    def run(self, stdin, log):
        config = get_config()
        if config["host"] == "digitalocean":
            host = providers.DigitalOcean(config["host_token"])
        else:
            console.print(f"Host {config['host']} not available.")
            return 1
        for machine in host.machines:
            console.rule(f"[bold red]{machine['name']}")
            pprint(machine)
        return 0


@main.register()
class Registrar:
    """Manage your registrar."""

    def run(self, stdin, log):
        config = get_config()
        if config["registrar"] == "dynadot":
            registrar = providers.Dynadot(config["registrar_token"])
        else:
            console.print(f"Registrar {config['registrar']} not available.")
            return 1
        for domain in registrar.domains:
            print(domain)
        return 0


if __name__ == "__main__":
    main()

# nuitka-project: --include-package=gevent.signal
# nuitka-project: --include-package=gunicorn.glogging
# nuitka-project: --include-package=gunicorn.workers.sync
# nuitka-project: --include-package=web.framework.templates
# nuitka-project: --include-package=web.host.templates
## nuitka-project: --include-package-data=mf2py
## nuitka-project: --include-package-data=selenium
