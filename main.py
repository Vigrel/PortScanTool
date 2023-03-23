import click
import nmap
from art import text2art
from colorama import Fore
from colorama import init as colorama_init

colorama_init(autoreset=True)


def get_user_info():
    art = text2art("Port Scan", font="small")
    print(f"{Fore.BLUE}{art}")
    art = text2art("       Tool", font="small")
    print(f"{Fore.BLUE}{art}")

    click.pause()
    click.clear()

    host = click.prompt(
        f"{Fore.GREEN}Select a Host", type=str, default="www.google.com"
    )
    ports = click.prompt(f"{Fore.GREEN}Select port range", type=str, default="0-1023")
    click.echo(f"\n{Fore.GREEN}Scaning ports...")

    return ports, host


def scanPort(port, host):
    scanner = nmap.PortScanner()
    scanner.scan(host, str(port))
    ip = scanner.all_hosts()[0]

    click.echo(f"\n{Fore.GREEN}IP: {Fore.WHITE}{ip}")
    click.echo(f"{Fore.GREEN}hostnames:")
    for name in scanner[ip].hostnames():
        click.echo(f"{Fore.WHITE}{name['name']}")

    click.echo(f"{Fore.GREEN}protocol:")
    protocols = scanner[ip].all_protocols()
    if len(protocols) == 0:
        print(f"{Fore.RED} NO PORTS OPEN")
        exit()
    for protocol in protocols:
        click.echo(f"   {Fore.WHITE}{protocol}:")
        for port in scanner[ip][protocol].keys():
            click.echo(
                f"      {Fore.GREEN}ports: {Fore.WHITE}{port} {Fore.GREEN}state: {Fore.WHITE}{scanner[ip][protocol][port]['state']} {Fore.GREEN}application: {Fore.WHITE}{scanner[ip][protocol][port]['product']}"
            )


@click.command()
def makeCLI():
    ports, host = get_user_info()

    if ports.split("-")[0].isdigit():
        scanPort(ports, host)
    else:
        print(
            f"{Fore.RED}Insert the ports like the default example {Fore.BLUE}initialPort-FinalPort"
        )
    exit()


if __name__ == "__main__":
    makeCLI()
