"""
Manage code on your website.

- Supports [PEP 503 -- Simple Repository API][0] managing Python packages.

[0]: https://www.python.org/dev/peps/pep-0503/

"""

# TODO PEP 592 -- Adding "Yank" Support to the Simple API
# TODO PEP 658 -- Serve Distribution Metadata in the Simple Repository API

import importlib.metadata
import pathlib
import re
import shutil
import subprocess
import time

import pkg_resources
import semver
import web
import webagt

app = web.application(__name__, prefix="system")

code_dir = pathlib.Path.home() / "code"
meta_dir = code_dir / "meta"
working_dir = code_dir / "working"


def get_ip():
    return subprocess.check_output(["hostname", "-I"]).split()[0].decode()


def update_system(*packages):
    print(
        subprocess.run(
            ["/home/gaea/runinenv", "/home/gaea/app", "pip", "install", "-U"]
            + list(packages),
            capture_output=True,
        )
    )


def get_versions(package):
    """Return the latest version if currently installed `package` is out of date."""
    current_version = pkg_resources.get_distribution(package).version
    current_version = current_version.partition("a")[0]  # TODO FIXME strips alpha/beta
    update_available = False
    versions_rss = webagt.get(
        f"https://pypi.org/rss/project/{package}/releases.xml"
    ).xml
    latest_version = [
        child.getchildren()[0].text
        for child in versions_rss.getchildren()[0].getchildren()
        if child.tag == "item"
    ][0]
    if semver.compare(current_version, latest_version) == -1:
        update_available = latest_version
    return current_version, update_available


@app.wrap
def set_working_dir(handler, main_app):
    web.tx.host.working_dir = working_dir
    yield


@app.control("")
class System:
    """The system that runs your website."""

    def get(self):
        """"""
        if not web.tx.user.is_owner:
            return "owner only"
        try:
            with open("/home/gaea/app/run/onion") as fp:
                onion = fp.read().strip()
        except FileNotFoundError:
            onion = None
        with open("domains") as fp:
            domains = fp.readlines()
        webint_metadata = importlib.metadata.metadata("webint")
        webint_versions = get_versions("webint")
        return app.view.index(
            get_ip(),
            onion,
            domains,
            web.tx.app.cfg,
            web.tx.app,
            web.get_apps(),
            webint_metadata,
            webint_versions,
        )


@app.control("addresses")
class Addresses:
    """System addresses."""

    def post(self):
        """"""
        return "addresses have been updated"


@app.control("addresses/domains")
class Domains:
    """System addresses."""

    def get(self):
        """"""
        form = web.form("domain")
        records = {}
        for record in ("A", "CNAME", "MX", "NS"):
            try:
                records[record] = web.dns.resolve(form.domain, record)
            except (web.dns.NoAnswer, web.dns.NXDOMAIN):
                pass
        return app.view.addresses.domains(get_ip(), form.domain, records)

    def post(self):
        form = web.form("domain")
        web.enqueue(add_domain, form.domain)
        return "adding domain"


def add_domain(domain):
    """Begin handling requests at given domain."""
    ip = get_ip()
    onions = []
    with open("onion") as fp:
        onions.append(fp.read())

    domain_path = pathlib.Path("domains")
    with domain_path.open() as fp:
        domains = {domain: True for domain in fp.readlines()}
    domains[domain] = False

    run_dir = "/home/gaea/app/run"
    nginx_conf_path = pathlib.Path("/etc/nginx/nginx.conf")
    with nginx_conf_path.open("w") as fp:
        fp.write(str(web.host.templates.nginx(run_dir, ip, onions, domains)))
    subprocess.call(["sudo", "service", "nginx", "restart"])

    web.generate_cert(domain)

    domains[domain] = True
    with nginx_conf_path.open("w") as fp:
        fp.write(str(web.host.templates.nginx(run_dir, ip, onions, domains)))
    subprocess.call(["sudo", "service", "nginx", "restart"])

    with domain_path.open("w") as fp:
        for domain in domains:
            print(domain, file=fp)


@app.control("software")
class Software:
    """System software."""

    def post(self):
        """"""
        web.enqueue(
            update_system,
            "canopy-platform",
            "webint",
            *[a.project_name for a in web.get_apps().keys()],
        )
        return "software update has been started"


@app.control("settings")
class Settings:
    """System settings."""

    def post(self):
        """"""
        form = web.form("key", "value")
        web.tx.app.update_config(form.key, form.value)
        return "settings have been updated"


@app.control("robots.txt", prefixed=False)
class RobotsTXT:
    """A robots.txt file."""

    def get(self):
        """Return a robots.txt file."""
        all_bots = ["User-agent: *"]
        for project in web.application("webint_code").model.get_projects():
            all_bots.append(f"Disallow: /code/{project}/releases/")
        return "\n".join(all_bots)
