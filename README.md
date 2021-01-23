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

## Usage Examples

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
