# Simple Menu

Generic `python` class for creating simple menus. Provides basic tree-like menu structure with a few types of commonly used elements:
- commands - just "run some function",
- radios,
- checkboxes,
- submenus,
- navigation elements, e.g. "go back".

**Simple Menu** also gives:
- methods for creating and deleting elements,
- methods for "movements": move up, move down, change level in hierarchy.

**Simple Menu** is not a complete solution for creating a menu, it does not provide out-of-the-box GUI elements for any popular graphical framework or customizable text elements for embedded system.

Instead, You can use **Simple Menu** as a base class for Your own implementation of menu, e.g. drop-down menu in desktop app with sophisticated GUI, text-only menu in terminal app, menu displayed on alphanumeric LCD display connected to Raspberry Pi or even little MCU running [Micropython](https://micropython.org/).