from src.database.setup import setup_database
from src.pages.app import App

if __name__ == "__main__":
    setup_database()
    
    App()