StoreManager
============

An Elven Fire utility to simplify town usage by automatically generating and maintaining the stores and universities.

## Known Versions

StoreManager is built with:
*  Python 3.3.4
*  PyQt 4.10.4
*  elvenfire 1.1.0

## Prerequisites

The Store Manager requires access to the base elvenfire library. One simple way to accomplish this is to create a symbolic link to the library's location within the StoreManager base directory. For example, if both repos are cloned within the same directory:

```
ln -s ../elvenfire/elvenfire/ elvenfire
```

## Command Line Interface

ELF Store Manager can be used from the command line without the need to install PyQt. Locations will be stored in the current working directory in custom formats (`.town`, `.store`, `.uni`) as well as human-readable versions automatically maintained in the same directory (`.txt`).

## Creating locations

A single location (created outside of a Town structure) can be stored in a `.store` or `.uni` file in the current directory.

```bash
elfsm --create --store "Lonely Roadpost" --size 3
elfsm --create --university "Traveling Mentors" --size 1
```

More commonly, a town can be generated with an appropriate selection of stores and/or universities according to the size selected (1-5, where 3 is a standard large town). A full town will be stored in a `.town` file in the current directory.

```bash
elfsm --create --town "Guilderland" --size 5
```

Once created, these location files are self-contained and can be transferred from computer to computer, backed up online, or otherwise managed like any other file.

### Purchasing items

Purchase an item directly:

```bash
elfsm --town Guilderland --purchase "Rod of Fireball 3 - 8 charges"
elfsm --town Guilderland --purchase 'Healing Potion' --quantity 3
```

You will be asked to confirm the item and price, and then the appropriate `.town` and `.txt` files will be updated with these items removed.

Note that purchasing items will NOT perform a weekly update on the location purchased from. Weekly updates must be performed separately before the next play session (see below).

### Weekly updates

After all purchases have been made for the week, a weekly update should be performed to update stock and prices for the next week of play.

Perform a weekly update:

```bash
elfsm --update --town Guilderland
```

Changes in stock will be displayed on the screen, and the `.town` and `.txt` files will be updated with the new contents of the stores and/or universities.

## Library Usage Examples

A GUI is provided for use with PyQT, or within the Python interpreter, you can access stores directly:
```
>>> from storemanager.locations.store import GeneralStore
>>> store = GeneralStore("Foos For Rent", 1)
>>> print(store.readable())

>>> store.update()
>>> print(store.readable())
```

Or you can create a town full of stores all at once:
```
>>> from storemanager.locations.town import Town
>>> town = Town("Foosville", 1)
>>> print(town.readable())

>>> town.update()
>>> print(town.readable())
```

Universities are also available directly:
```
>>> from storemanager.locations.university import University
>>> uni = University("UFOO", 1)
>>> print(uni.readable())

>>> uni.update()
>>> print(uni.readable())
```

In all cases, the second parameter when creating a new location should be an integer from 1 to 5 representing the size of the location, from small and manageable (1) to quite large (3) to truly gigantic (5). 
