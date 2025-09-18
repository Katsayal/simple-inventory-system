from .gui import App
from .inventory import Inventory

def main():
    # Initialize the inventory
    inventory = Inventory()
    
    # Load initial data from the CSV file
    try:
        inventory.load_from_csv("data/inventory.csv")
    except FileNotFoundError:
        print("Initial inventory.csv not found, starting with empty inventory.")

    # Launch the GUI application
    app = App(inventory)
    app.mainloop()

if __name__ == "__main__":
    main()