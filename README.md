# Simple Inventory System

### Project Summary

This project is a desktop application built with Python and CustomTkinter, designed to help small businesses manage their product inventory. It allows users to track products, monitor stock levels, and receive reorder alerts. The application also supports the import and export of inventory data, providing a robust solution for managing product information.

### Features

  * **Product Management**: Add new products to the inventory.
  * **Stock Control**: Adjust stock levels for existing products.
  * **Low Stock Alerts**: Visually alets for items that fall below a predefined stock threshold.
  * **Data Persistence**: Seamlessly import and export inventory data from `.csv` and `.xlsx` files.
  * **User-Friendly Interface**: A clean and intuitive GUI to view and manage all products.

### Setup and Installation

To get the application up and running, follow these steps.

#### Prerequisites

  * Python 3.10 or higher
  * pipenv

#### Installation Steps

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/Katsayal/simple-inventory-system
    cd groupXX-projectname
    ```


2.  **Install Dependencies**:
    The project uses `pipenv` for dependency management. Run the following command to install all required packages:

    ```bash
    pipenv install
    ```

3.  **Run the Application**:
    Once the dependencies are installed, you can launch the application with a single command:

    ```bash
    pipenv run python -m src.main
    ```

4.  **VS Code Users**: If you are using VS Code, you can also run the application directly from the editor using the `launch.json` file provided in the `.vscode` directory. This will handle the correct module path.

### How to Use the Application

  * **View Products**: The main window displays a table with all products. Low-stock items are highlighted with a `⚠️`.
  * **Add Product**: Click the "Add Product" button to open a dialog and add a new item to your inventory.
  * **Adjust Stock**: Click the "Adjust Stock" button to change the quantity of an existing product.
  * **View Low Stock**: Click the "View Low Stock" button to filter the table and see only the products that need to be reordered.
  * **Open File**: Click "Open File" to import an existing inventory from a `.csv` or `.xlsx` file.
  * **Save File**: Click "Save File" to export your current inventory to a `.csv` or `.xlsx` file.

### Roles and Contributions

This project was a collaborative effort to demonstrate proficiency in Python development, dependency management, and GUI creation.

  * **Group Member Name 1 (Your Name)**: [Your role, e.g., "Lead Developer", "GUI Designer"]
  * **Group Member Name 2**: [Their role]
  * **...and so on.**

The project's commit history showcases a detailed record of each member's contributions, with meaningful commit messages that reflect the progress and features implemented throughout development.

### Application Demonstration

A short demo video of the application in action can be found at this link:


### Repository Structure
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
