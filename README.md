# Simple Inventory System

## Project Summary

This project is a command-line interface (CLI) application for a simple inventory management system. It allows users to track products, manage stock levels, and identify low-stock items. The system supports data persistence by importing and exporting product information using CSV files.


## Features

* **Add Products**: Easily add new products with a SKU, name, quantity, and supplier ID.
* **Adjust Stock**: Increase or decrease the stock quantity for existing products.
* **Low-Stock Alerts**: View a list of all products with a quantity at or below a predefined low-stock threshold.
* **CSV Import/Export**: Load inventory data from a CSV file and save the current state back to a CSV.


## Technologies Used

* **Python 3.10+**: The core programming language.
* **pipenv**: For dependency management.
* **pytest**: For unit testing.
* **GitHub Actions**: For Continuous Integration (CI).


## Setup and Run Instructions

### 1. Clone the Repository
```bash
git clone [https://github.com/Katsayal/simple-inventory-system.git](https://github.com/Katsayal/simple-inventory-system.git)
cd simple-inventory-system


2. Install Dependencies
This project uses pipenv to manage dependencies. Ensure pipenv is installed on your system.

Bash
# If pipenv is not installed
pip install pipenv

# Install project dependencies
pipenv install --dev
3. Run the Application
The application can be run with a single command from the project root.

Bash
pipenv run python src/main.py
4. Run the Tests
To ensure everything is working correctly, you can run the unit tests.

Bash
pipenv run pytest
Repository Structure
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── inventory.csv
├── src/
│   ├── __init__.py
│   ├── inventory.py
│   └── main.py
├── tests/
│   └── test_core.py
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── pytest.ini
└── README.md
