"""Command-line interface for the superpowers marketplace."""

from __future__ import annotations

import click

from . import marketplace, registry
from .installer import (
    AlreadyInstalledError,
    NotFoundError,
    NotInstalledError,
    install,
    uninstall,
    update,
)

_BOLD = lambda s: click.style(s, bold=True)  # noqa: E731
_GREEN = lambda s: click.style(s, fg="green")  # noqa: E731
_RED = lambda s: click.style(s, fg="red")  # noqa: E731
_YELLOW = lambda s: click.style(s, fg="yellow")  # noqa: E731
_CYAN = lambda s: click.style(s, fg="cyan")  # noqa: E731


def _print_superpower(sp: dict, *, installed: bool = False) -> None:
    status = _GREEN(" [installed]") if installed else ""
    click.echo(f"  {_BOLD(sp['name'])} v{sp['version']} by {sp['author']}{status}")
    click.echo(f"    {sp['description']}")
    if sp.get("tags"):
        click.echo(f"    tags: {', '.join(_CYAN(t) for t in sp['tags'])}")


@click.group()
@click.version_option(package_name="superpowers-marketplace")
def main() -> None:
    """Superpowers Marketplace — discover and install Python superpowers."""


@main.command("search")
@click.argument("query")
def cmd_search(query: str) -> None:
    """Search the marketplace for superpowers matching QUERY."""
    results = marketplace.search(query)
    if not results:
        click.echo(f"No superpowers found for '{query}'.")
        return
    installed_names = {sp["name"] for sp in registry.list_installed()}
    click.echo(f"\nFound {len(results)} superpower(s) matching '{_BOLD(query)}':\n")
    for sp in results:
        _print_superpower(sp, installed=sp["name"] in installed_names)
        click.echo()


@main.command("browse")
def cmd_browse() -> None:
    """List all available superpowers in the marketplace."""
    all_sp = marketplace.get_all()
    installed_names = {sp["name"] for sp in registry.list_installed()}
    click.echo(f"\nSuperpowers Marketplace — {len(all_sp)} available:\n")
    for sp in all_sp:
        _print_superpower(sp, installed=sp["name"] in installed_names)
        click.echo()


@main.command("info")
@click.argument("name")
def cmd_info(name: str) -> None:
    """Show detailed information about a superpower."""
    sp = marketplace.get_by_name(name)
    if sp is None:
        click.echo(_RED(f"Superpower '{name}' not found."), err=True)
        raise SystemExit(1)
    installed = registry.is_installed(name)
    click.echo()
    _print_superpower(sp, installed=installed)
    if sp.get("dependencies"):
        click.echo(f"    depends on: {', '.join(sp['dependencies'])}")
    click.echo()


@main.command("install")
@click.argument("name")
def cmd_install(name: str) -> None:
    """Install a superpower by NAME."""
    try:
        sp = install(name)
        click.echo(_GREEN(f"Installed '{sp['name']}' v{sp['version']}."))
    except AlreadyInstalledError as e:
        click.echo(_YELLOW(str(e)))
    except NotFoundError as e:
        click.echo(_RED(str(e)), err=True)
        raise SystemExit(1)


@main.command("uninstall")
@click.argument("name")
def cmd_uninstall(name: str) -> None:
    """Uninstall an installed superpower by NAME."""
    try:
        uninstall(name)
        click.echo(_GREEN(f"Uninstalled '{name}'."))
    except NotInstalledError as e:
        click.echo(_RED(str(e)), err=True)
        raise SystemExit(1)


@main.command("update")
@click.argument("name")
def cmd_update(name: str) -> None:
    """Update an installed superpower to its latest catalog version."""
    try:
        sp = update(name)
        click.echo(_GREEN(f"Updated '{sp['name']}' to v{sp['version']}."))
    except (NotInstalledError, NotFoundError) as e:
        click.echo(_RED(str(e)), err=True)
        raise SystemExit(1)


@main.command("list")
def cmd_list() -> None:
    """List all installed superpowers."""
    installed = registry.list_installed()
    if not installed:
        click.echo("No superpowers installed. Run 'superpowers browse' to explore.")
        return
    click.echo(f"\nInstalled superpowers ({len(installed)}):\n")
    for sp in installed:
        _print_superpower(sp, installed=True)
        click.echo()
