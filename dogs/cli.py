import click
from dogs.dogs import DOGS

dogs = DOGS()

@click.group()
def cli():
    pass

@cli.command()
def list():
    click.echo("Available droplets:")
    for name in dogs.list_droplets():
        click.echo(f" - {name}")

@cli.command()
@click.argument('name')
def status(name):
    dm = dogs.get_droplet_manager(name)
    click.echo(f"Droplet '{name}' status: {dm.get_status()}")

@cli.command()
@click.argument('name')
@click.option('--wait', is_flag=True, help="Wait for the action to complete.")
@click.option('--timeout', default=300, help="Timeout in seconds.")
@click.option('--poll-interval', default=5, help="Polling interval in seconds.")
def toggle(name, wait, timeout, poll_interval):
    dm = dogs.get_droplet_manager(name)

    def done(droplet):
        click.echo(f"Toggled '{name}'. New status: {dm.get_status()}")

    dm.toggle_power(on_complete=done if wait else None, timeout=timeout, poll_interval=poll_interval)

@cli.command()
@click.argument('name')
@click.option('--wait', is_flag=True, help="Wait for the action to complete.")
@click.option('--timeout', default=300, help="Timeout in seconds.")
@click.option('--poll-interval', default=5, help="Polling interval in seconds.")
def power_on(name, wait, timeout, poll_interval):
    dm = dogs.get_droplet_manager(name)

    def done(droplet):
        click.echo(f"Power on completed for '{name}'.")

    dm.power_on(on_complete=done if wait else None, timeout=timeout, poll_interval=poll_interval)

@cli.command()
@click.argument('name')
@click.option('--wait', is_flag=True, help="Wait for the action to complete.")
@click.option('--timeout', default=300, help="Timeout in seconds.")
@click.option('--poll-interval', default=5, help="Polling interval in seconds.")
def power_off(name, wait, timeout, poll_interval):
    dm = dogs.get_droplet_manager(name)

    def done(droplet):
        click.echo(f"Power off completed for '{name}'.")

    dm.power_off(on_complete=done if wait else None, timeout=timeout, poll_interval=poll_interval)

if __name__ == "__main__":
    cli()
    