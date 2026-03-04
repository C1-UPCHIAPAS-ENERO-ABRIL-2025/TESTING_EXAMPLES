"""Command-line interface for inventory management system.

Provides CLI commands for authentication, backup, state management,
and discount calculation.
"""

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
@click.option("--season", default="normal")
@click.option("--region", default="US")
def discount(
    category: str,
    user_level: str,
    purchase_count: int,
    holiday: bool,
    season: str,
    region: str,
) -> None:
    """Calculate discount for a purchase.

    Args:
        category: Product category (electronics, books, clothing, furniture)
        user_level: Customer tier (platinum, gold, silver, bronze, or other)
        purchase_count: Number of past purchases
        holiday: Whether to apply holiday bonus
        season: Seasonal context (normal, black_friday, clearance, summer)
        region: Geographic region (US, EU, ASIA)
    """
    discount_amount = calculate_discount(
        item_category=category,
        user_level=user_level,
        purchase_history_count=purchase_count,
        is_holiday=holiday,
        season=season,
        region=region,
    )
    discount_pct = discount_amount * 100
    click.echo(f"Discount: {discount_pct:.1f}% ({category}, {user_level})")


if __name__ == "__main__":
    cli()
