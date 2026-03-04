# inventory_system/cli.py

import click
from .auth import is_admin
from .logic.discount_calculator import calculate_discount
from .persistence import state_manager
from .utils import system_caller

@click.group()
def cli():
    """A vulnerable inventory management system CLI."""
    pass

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    """Attempts to log in as admin (uses hardcoded credentials)."""
    if is_admin(username, password):
        click.echo("Login successful! Welcome, admin.")
    else:
        click.echo("Login failed.")

@cli.command()
@click.argument('destination')
def backup(destination):
    """Creates a backup (vulnerable to command injection)."""
    click.echo(f"Backing up state to '{destination}'...")
    system_caller.create_backup(destination)

@cli.command()
def save():
    """Saves a dummy state (uses insecure pickle)."""
    dummy_data = {"items": ["laptop", "mouse"], "user": "test"}
    state_manager.save_state(dummy_data)

@cli.command()
def load():
    """Loads state from a file (vulnerable to deserialization)."""
    data = state_manager.load_state()
    if data:
        click.echo(f"Loaded data: {data}")
    else:
        click.echo("No state file found.")

if __name__ == '__main__':
    cli()