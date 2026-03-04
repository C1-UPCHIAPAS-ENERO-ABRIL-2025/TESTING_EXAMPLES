import click

from inventory_system.auth import is_admin
from inventory_system.logic.discount_calculator import calculate_discount
from inventory_system.persistence import state_manager
from inventory_system.utils.backup_manager import create_backup


@click.group()
def cli() -> None:
    """Secure inventory management system CLI."""


@cli.command()
@click.argument("username")
@click.argument("password")
def login(username: str, password: str) -> None:
    """Authenticate admin user with environment-backed credentials."""
    if is_admin(username, password):
        click.echo("Login successful! Welcome, admin.")
    else:
        click.echo("Login failed.")


@cli.command()
@click.argument("destination")
def backup(destination: str) -> None:
    """Create a file backup without shell command execution."""
    try:
        target = create_backup(destination)
        click.echo(f"Backup created at: {target}")
    except FileNotFoundError as error:
        click.echo(str(error))


@cli.command()
def save() -> None:
    """Save a sample state in JSON format."""
    dummy_data = {"items": ["laptop", "mouse"], "user": "test"}
    saved_path = state_manager.save_state(dummy_data)
    click.echo(f"State saved to {saved_path}")


@cli.command()
def load() -> None:
    """Load state from JSON file."""
    data = state_manager.load_state()
    if data:
        click.echo(f"Loaded data: {data}")
    else:
        click.echo("No state file found.")


@cli.command()
@click.argument("category")
@click.argument("user_level")
@click.argument("purchase_count", type=int)
@click.option("--holiday", is_flag=True, default=False)
def discount(category: str, user_level: str, purchase_count: int, holiday: bool) -> None:
    """Calculate discount for a purchase."""
    discount_amount = calculate_discount(category, user_level, purchase_count, holiday)
    click.echo(f"Discount for {category}: {discount_amount * 100:.1f}%")


if __name__ == "__main__":
    cli()
