from typing import Optional

import typer
from cups import Connection, IPPError, getServer, getPort
from pycups_po import PrinterOptionsGenerator
from rich import print
from rich.tree import Tree

main = typer.Typer()


def provide_exception(e, conn_params, printer_name: str = None):
    if e.args[0] == 1025:
        typer.secho(
            f'Host {conn_params["host"]}:{conn_params["port"]} access denied.',
            fg=typer.colors.RED,
        )
    elif e.args[0] == 1030:
        typer.secho(
            f"Printer '{printer_name}' does not exist on host {conn_params['host']}:{conn_params['port']}.\n"
            f"Use 'pycups_po printers' to get a list of printers.",
            fg=typer.colors.RED,
        )
    elif e.args[0] == "failed to connect to server":
        typer.secho(
            f'Unable to connect to {conn_params["host"]}:{conn_params["port"]}.',
            fg=typer.colors.RED,
        )
    else:
        typer.secho(
            repr(e),
            fg=typer.colors.RED,
        )
    raise typer.Exit(code=1)


@main.command()
def printers(
    host: Optional[str] = typer.Option(None, help="getHost() by default"),
    port: Optional[int] = typer.Option(None, help="getPort() by default"),
):
    conn_params = {
        "host": host or getServer(),
        "port": port or getPort(),
    }
    try:
        conn = Connection(**conn_params)
        cups_printers = conn.getPrinters()
        printers = Tree("🖨 Printers")
        for p_name, p_options in cups_printers.items():
            is_shared = p_options["printer-is-shared"]

            info = p_options["printer-info"]

            state = {3: "⏳ idle", 4: "📃 printing", 5: "🛑 stopped"}[
                p_options["printer-state"]
            ]

            branch_color = "green" if is_shared else "yellow"
            branch_color = (
                "blue" if state == 4 else "red" if state == 5 else branch_color
            )

            branch = printers.add(p_name, style=branch_color)
            branch.add(f"Info: {info}", style="default")
            branch.add(f"State: {state}", style="default")
        print(printers)
    except (IPPError, RuntimeError) as e:
        provide_exception(e, conn_params)


@main.command()
def generate(
    printer: str,
    output_file: typer.FileTextWrite = typer.Option(..., "--output_file", "-o"),
    host: Optional[str] = typer.Option(None, help="getHost() by default"),
    port: Optional[int] = typer.Option(None, help="getPort() by default"),
):
    conn_params = {
        "host": host or getServer(),
        "port": port or getPort(),
    }
    try:
        conn = Connection(**conn_params)
        generator = PrinterOptionsGenerator(conn)
        dataclass_content = generator.generate_options_dataclass(printer_name=printer)
        output_file.write(dataclass_content)
    except (IPPError, RuntimeError) as e:
        provide_exception(e, conn_params, printer)


@main.command()
def options(
    printer: str,
    host: Optional[str] = typer.Option(None, help="getHost() by default"),
    port: Optional[int] = typer.Option(None, help="getPort() by default"),
):
    conn_params = {
        "host": host or getServer(),
        "port": port or getPort(),
    }
    try:
        conn = Connection(**conn_params)
        generator = PrinterOptionsGenerator(conn)
        printer_options = generator.get_ppd_options(printer_name=printer)

        options_tree = Tree("⚙️ Options")

        for option in printer_options:
            option_branch = options_tree.add(
                f"{option.name} ({option.pretty_name})", style="green"
            )
            option_branch.add(f"Type: {option.type}", style="default")
            option_branch.add(f"Default: {option.default_value}", style="default")
            values_branch = option_branch.add("Values:", style="default")
            for value in option.values:
                values_branch.add(
                    f"'{value.value}' ({value.pretty_value}): {value.content}",
                    style="default",
                )

        print(options_tree)
    except (IPPError, RuntimeError) as e:
        provide_exception(e, conn_params, printer)


if __name__ == "__main__":
    main()
