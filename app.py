from PySide6 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

from shopping import*


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setWindowTitle("pyShoppingList")
        self.setFixedHeight(600)
        apply_stylesheet(app, 'light_teal.xml')

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.css()
        self.setup_connections()
        
    def css(self):                         
        self.lw_files.setStyleSheet("font-weight: bold;")

    def create_widgets(self):
        self.lw_files = QtWidgets.QListWidget()
        self.lw_content = QtWidgets.QListWidget()
        self.btn_delete_list = self.MyPushButton("resources/trash.png")
        self.btn_delete_item = self.MyPushButton("resources/trash.png")
        self.btn_add_list = self.MyPushButton("resources/add.png")
        self.btn_add_item = self.MyPushButton("resources/additem.png")
       
    def modify_widgets(self):
        for item in load_lists():
            lw_item = QtWidgets.QListWidgetItem(item)
            lw_item.text = item
            self.lw_files.addItem(lw_item)
        
        self.lw_content.setFixedWidth(400)
        self.lw_files.setFixedWidth(200)
             
    def create_layouts(self):
        self.layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.layout.addWidget(self.lw_files, 0, 0, 1, 3)
        self.layout.addWidget(self.lw_content, 0, 4, 1, 3)
        self.layout.addWidget(self.btn_delete_list, 1, 0, 1, 1)
        self.layout.addWidget(self.btn_add_list, 1, 1, 1, 1)
        self.layout.addWidget(self.btn_delete_item, 1, 4, 1, 1)
        self.layout.addWidget(self.btn_add_item, 1, 5, 1, 1)

    def setup_connections(self):
        self.lw_files.itemClicked.connect(self.populate_lw_content)
        self.btn_delete_list.clicked.connect(self.delete_list)
        self.btn_delete_item.clicked.connect(self.delete_item)
        self.btn_add_list.clicked.connect(self.get_name_for_add_list)
        self.btn_add_item.clicked.connect(self.get_item_for_add_list)

    def populate_lw_content(self):
        self.lw_content.clear()
        selected = self._get_selected_item(self.lw_files)
        self.obj = load_shopping_list_object(selected)
        for item in self.obj:
            lw_item = QtWidgets.QListWidgetItem(item)
            lw_item.text = item
            self.lw_content.addItem(lw_item)

    def delete_list(self):
        selected = self._get_selected_item(self.lw_files)
        remove_file(selected)
        self.clear_and_reload()

    def delete_item(self):
        selected = self._get_selected_item(self.lw_content)
        self.obj.remove_item_to_list(selected)
        self.lw_content.clear()
        self.populate_lw_content()

    def _get_selected_item(self, list_widget):
        selected_items = list_widget.selectedItems()
        if selected_items:
            return selected_items[0].text

    def get_name_for_add_list(self):
        text = self.inputdial("Add new list", "List name:")
        self.obj = ShoppingList(text)
        self.clear_and_reload()

    def get_item_for_add_list(self):
        text = self.inputdial("Add new item", "Item name:")
        self.obj.add_item_to_list(text)
        self.lw_content.clear()
        self.populate_lw_content()

    def inputdial(self, window_title, text):
        text, ok = QtWidgets.QInputDialog().getText(self, window_title,
                                     text, QtWidgets.QLineEdit.Normal)
        if ok and text: return text
            
    def clear_and_reload(self):
        self.lw_files.clear()
        self.lw_content.clear()
        self.modify_widgets()

    class MyPushButton(QtWidgets.QPushButton):
        def __init__(self, image):
            super().__init__()
            self.setIcon(QtGui.QIcon(image))
            self.setIconSize(QtCore.QSize(30, 30))
            self.setFixedSize(40, 30)
            self.setStyleSheet("MyPushButton {border: none;}"
                                "MyPushButton::hover {background-color: #1ed19c;};")


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
