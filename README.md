# ARCA
Currently program just in Spanish language but intuitive enough for using whiout understanding the language.
**Arca** is a password-protected folder manager for Windows that I found on an old hard drive at a yard sale.

The original code was corrupted, but I have managed to repair most of it, and it now works surprisingly well.

It allows you to create protected folders that require a password before opening them.

> ⚠️ Arca is currently in development and should not be considered a high-security solution.

## Features

* 🔐 Password-protected folders
* 🖥️ Windows desktop application
* 🔑 Master password

## Requirements

* Windows
* Python 3.x (when running from source)

## Running from source

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Arca.git
cd Arca
```

Then run:

```bash
python Arca_main.py
```

## Building

Arca can be compiled into a standalone Windows executable using PyInstaller.

```bash
python -m PyInstaller --onefile --windowed --icon="Assets\ARCA.ico" --add-data "Assets;Assets" Arca_main.py
```

## Project status

🚧 **In development**

The current goal is to keep reparing the mysterious code and uncover more of its features.

## License

This project is currently not licensed.

