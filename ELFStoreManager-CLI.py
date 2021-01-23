import sys, os
import argparse

from elvenfire import ELFError
from storemanager.locations.town import Town

# Define help text
parser = argparse.ArgumentParser(
    prog="elfsm",
    formatter_class=argparse.RawTextHelpFormatter,
    description="Create and manage Elven Fire locations",
    epilog="""
Usage Examples:

Create a new town:
> elfsm --create
> elfsm --create --town Foosville
> elfsm --create --town Foosville --size 5
> elfsm -ct Foosville -z 5

Create a standalone store or university:
> elfsm --create --store "Mike's Treasure Stop"
> elfsm --create --university "Guildmasters"
> elfsm -cs "Mike's Treasure Stop"
> elfsm -cv "Guildmasters"

Mark an item purchased:
> elfsm --town Foosville --purchase --item "Rod of Fireball 3 - 12 charges"
> elfsm --town Foosville --purchase --item "Healing Potion" --quantity 3
> elfsm -t Foosville -pi "Healing Potion" -q 3

Perform a weekly update:
> elfsm --update
> elfsm --update --town Foosville
> elfsm --update --town Foosville --weeks 52
> elfsm -ut Foosville
""")

# Top-level command-line arguments
parser.add_argument('-t', "--town", type=str, help="the name of the town under management")
parser.add_argument('-s', "--store", type=str, help="name of specific store")
parser.add_argument('-v', "--university", type=str, help="name of specific university")
cmd_group = parser.add_mutually_exclusive_group(required=False)

# Subcommand: create new
cmd_group.add_argument('-c', "--create", action='store_true', help="create a new location")
parser.add_argument('-z', "--size", type=int, default=2, help="size of the location to create")

# Subcommand: purchase item(s)
cmd_group.add_argument('-p', "--purchase", action='store_true', help="item to purchase from a location")
parser.add_argument('-i', "--item", type=str, help="exact item name")
parser.add_argument('-q', "--quantity", type=int, default=1, help="number of identical items to purchase")

# Subcommand: weekly update
cmd_group.add_argument('-u', "--update", action='store_true', help="perform a weekly update")
parser.add_argument('-w', "--weeks", type=int, default=1, help="Number of weeks to update consecutively")

args = parser.parse_args()
print(args)
