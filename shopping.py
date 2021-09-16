import logging
import json
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
DATA_DIR = Path(__file__).parent / "DATA"


def load_shopping_list_object(name):
    """returns the ShoppingList object using the name of the list passed as argument"""
    if (DATA_DIR / (name.upper() + ".json")).exists():
        return ShoppingList(name.upper())
    logging.debug(f"La liste {name.upper()} n'est pas présente dans le dossier DATA.")

def load_lists():
    """returns a list containing the names of the json files present in the DATA folder"""
    return [i.stem for i in DATA_DIR.iterdir() if i.suffix == ".json"]
    
def remove_file(name):
    """delete the json file"""
    if (DATA_DIR / (name.upper() + ".json")).exists():
        (DATA_DIR / (name.upper() + ".json")).unlink()


class ShoppingList(list):
    def __init__(self, name: str):
        super().__init__()
        self.name = name.upper()
        self._load_list()
        self.sav_list()

    def add_item_to_list(self, *args):
        """adds the elements passed as arguments to the list"""
        for item in args:
            if item.capitalize() in self:
                logging.debug(f"{item.capitalize()} est déjà présent dans la liste.")
                continue
            self.append(item.capitalize())
        self.sav_list()

    def remove_item_to_list(self, item: str):
        """remove the item using its index if it is present in the list"""
        try:
            index = self.index(item.capitalize())
        except ValueError:
            logging.debug(f"{item.capitalize()} n'est pas présent dans la liste.")
        else:
            self.pop(index)
            logging.debug(f"{item.capitalize()} a été supprimé de la liste {self.name}.")
        self.sav_list()

    def _load_list(self):
        """loads the file if existing"""
        file = DATA_DIR / (self.name + ".json")
        if file.exists():
            with open(file, "r") as f:
                self.extend(json.load(f))
        
    def sav_list(self):
        """save the list in a json file in the DATA directory"""
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True, parents=True)
        with open(DATA_DIR / (self.name + ".json"), "w") as f:
            json.dump(self, f, indent=4)
            
    def show_list(self):
        """displays in list form the elements contained"""
        for i, item in enumerate(self):
            print(i+1, item)


if __name__ == "__main__":
    obj = ShoppingList("SUPER")
    obj.add_item_to_list("crevette", "banane", "pomme")

