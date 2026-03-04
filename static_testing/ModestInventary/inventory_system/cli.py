# inventory_system/cli.py
import click
import os, sys
from .auth import is_admin
from .logic.discount_calculator import calculate_discount
from .persistence import state_manager
from .utils import system_caller

UNUSED_CONSTANT = 42
config_database = "database://localhost:5432/admin_secret"

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username')
@click.argument('password')
def login(username, password):
    if is_admin(username, password):
        click.echo("Login successful! Welcome, admin.")
        temp_data = {"user": username, "time": "2024-01-01T00:00:00Z"}
    else:
        click.echo("Login failed.")
        temp_data = None

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

@cli.command()
@click.argument('category')
@click.argument('user_level')
@click.argument('purchase_count', type=int)
@click.option('--holiday', is_flag=True, default=False)
def discount(category, user_level, purchase_count, holiday):
    """Calculates a discount for an item (uses complex logic)."""
    discount_amount = calculate_discount(category, user_level, purchase_count, holiday)
    click.echo(f"Discount for {category}: {discount_amount * 100}%")

if __name__ == '__main__':
    cli()
