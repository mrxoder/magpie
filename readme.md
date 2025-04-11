# 🐦 Magpie

**Magpie** is a simple command-line tool for storing and organizing OSINT (Open-Source Intelligence) data and leaked information related to a target. Whether you're tracking digital footprints or building up intelligence for research, Magpie lets you store everything in one searchable, structured place.

---

## ✨ Features

- 📁 Manage multiple targets (people, organizations, entities).
- 🗃️ Store various types of data per target: plain text, files, or images.
- 🔍 Search, list, count, and dump data about any target.
- 🧠 Build your own OSINT intelligence database.
- ⚡ Fully CLI-based for fast and simple integration into any workflow.

---

## 🛠️ Installation

### 🔁 Clone the repository

```bash
git clone https://github.com/mrxoder/magpie.git
cd magpie
```
### 🚀 Make it executable from anywhere (optional)

If you'd like to use `magpie` as a global command on your system (without needing to type `python magpie.py` each time), follow these steps:

1. Make the script executable:

    ```bash
    chmod +x magpie.py
    ```

2. Create a symbolic link to a directory in your `PATH` (e.g., `/usr/local/bin`):

    ```bash
    sudo ln -s $(pwd)/magpie.py /usr/local/bin/magpie
    ```

Now, you can simply run `magpie` from anywhere on your system:

```bash
magpie --help
```