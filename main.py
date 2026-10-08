from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from seconde import *
import sys

#############################
class Model(QAbstractTableModel):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def data(self, index, role = ...):
        value = self.rows[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            return f"{value}"

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
    
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section == 0:
                    return "ID"
                elif section == 1:
                    return "Name"
                elif section == 2:
                    return "Family"
                elif section == 3:
                    return "Math"
                elif section == 4:
                    return "Geographi"
            else:
                return section + 1
    
    def rowCount(self, parent = ...):
        return len(self.rows)
    
    def columnCount(self, parent = ...):    
        return len(self.rows[0])

#############################
class Login (QWidget):
    def __init__(self):
        super().__init__()
        self.resize(350, 125)
        self.form_login = login()


        main_layout = QGridLayout()

        self.lables_and_boxes_layout = QGridLayout()
        self.buttons_layout = QGridLayout()

        self.txt_username = self.create_lables_and_boxes ("Username", 0)
        self.txt_password = self.create_lables_and_boxes ("Password", 1)

        self.create_button("Check", self.check_data, 0, 0, self.buttons_layout)

        main_layout.addLayout(self.lables_and_boxes_layout, 0, 0, 1, 1)
        main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        self.setLayout(main_layout)

    def create_lables_and_boxes (self, sub_text, row):
        label = QLabel(sub_text)
        self.lables_and_boxes_layout.addWidget(label, row, 0, 1, 1)
        txt = QLineEdit()
        self.lables_and_boxes_layout.addWidget(txt, row, 1, 1, 1)
        return txt

    def check_data (self):
        username = self.txt_username.text().strip()  
        password = self.txt_password.text().strip()

        try:
            user_data = self.form_login.select(username, password, "TBLdata.db")

            if not user_data:
                self.clear()
                self.message_box ("Username or Password is not cerroct")
                return
            
            if user_data[0][5] == "teacher":
                self.close()
                self.form_teacher = Form_teacher(user_data)
                self.form_teacher.show()

            if user_data[0][5] == "student":
                pass
                self.close()
                self.form_student = Form_student(user_data)
                self.form_student.show()

        except:
            self.clear()
            self.message_box ("Login failed, please try again")
            return

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

    def create_button (self, text, function, row, column, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button, row, column, 1, 1)
        return button

    def clear (self):
        self.txt_username.setText("")
        self.txt_password.setText("")

#############################
# region form teacher
class Form_teacher (QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.resize(300, 125)
        self.setWindowTitle("Teacher panel")
        self.user_data = user_data
        main_layout = QGridLayout()
        self.buttons_layout = QGridLayout()


        self.create_button("Add", self.add_data, 0, 0, self.buttons_layout)
        self.create_button("Update", self.update_data, 1, 0, self.buttons_layout)
        self.create_button("Show data", self.show_data, 2, 0, self.buttons_layout)
        self.create_button("Search" , self.search_data, 3, 0, self.buttons_layout)

        main_layout.addLayout(self.buttons_layout, 0, 0, 1, 1)
        self.setLayout(main_layout)

    def add_data (self):
        self.close()
        self.form_add_data = Form_add_data(self.user_data)
        self.form_add_data.show()

    def update_data (self):
        self.close()
        self.form_update_data = Form_update_data(self.user_data)
        self.form_update_data.show()

    def show_data (self):
        self.close()
        self.form_show_data = Form_show_data(self.user_data)
        self.form_show_data.show()

    def search_data (self):
        self.close()
        self.form_search_data = Form_search_data(self.user_data)
        self.form_search_data.show()

    def create_button (self, text, function, row, column, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button, row, column, 1, 1)
        return button

##############
class Form_add_data (QWidget): 
    def __init__(self, user_data):
        super().__init__()
        self.resize(1300, 400)
        self.setWindowTitle("Add data")
        self.user_data = user_data
        self.add = add()
        self.select_data = show()

        main_layout = QGridLayout()

        self.lables_and_boxes_layout = QGridLayout()
        self.buttons_layout = QGridLayout()
        self.tables_layout = QGridLayout()

        self.txt_name = self.create_lables_and_boxes ("Name", 0, 0)
        self.txt_family = self.create_lables_and_boxes ("Family", 1, 0)
        self.txt_math = self.create_lables_and_boxes ("Math", 2, 0)
        self.txt_geographi = self.create_lables_and_boxes ("Geographi", 3, 0)
        self.bt_add = self.create_button("Add", self.add_data, 0, 0)
        self.create_button("Return to menu", self.return_menu, 0, 1)
        self.create_table()

        main_layout.addLayout(self.lables_and_boxes_layout, 0, 0, 1, 1)
        main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        main_layout.addLayout(self.tables_layout, 0, 1, 2, 1)
        self.setLayout(main_layout)

        self.disable_field()
        self.show_data()

    def create_lables_and_boxes (self, sub_text, row, column):
        label = QLabel(sub_text)
        self.lables_and_boxes_layout.addWidget(label, (row * 2), column, 1, 1)
        txt = QLineEdit()
        self.lables_and_boxes_layout.addWidget(txt, (row * 2 + 1), column, 1, 1)
        txt.textChanged.connect(self.enable_field)
        return txt

    def add_data (self):
        Name = self.txt_name.text().strip()
        Family = self.txt_family.text().strip()
        Math = self.txt_math.text().strip()
        Geographi = self.txt_geographi.text().strip()

        if not Name.replace(" ", "").isalpha() or not Family.replace(" ", "").isalpha() or not Math.replace(".","", 1).isnumeric() or not Geographi.replace(".", "", 1).isnumeric():
            message = ""
            if not Name.replace(" ", "").isalpha():
                message += "Name "

            if not Family.replace(" ", "").isalpha():
                message += "Family "

            if not Math.replace(".","", 1).isnumeric():
                message += "Math "

            if not Geographi.replace(".", "", 1).isnumeric():
                message += "Geographi "
            self.clear()
            self.message_box(f"{message}is not cerroct")
        else:
            try:
                message = self.add.insert(Name, Family, Math, Geographi, self.user_data)

                self.show_data()
                self.clear()
                self.message_box(message)
            except:
                self.message_box("Could not add student, please try again")

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

    def show_data (self):
        try:
            self.rows = self.select_data.select(self.user_data)
            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
                width = self.width() // 2 - 16
                number_of_columns = len(self.rows[0])
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.message_box("table is empty")
        except:
            self.message_box("Could not load students list")
            return

    def return_menu (self):
        self.close()
        self.form_teacher = Form_teacher(self.user_data)
        self.form_teacher.show()

    def disable_add_button (self):
        self.bt_add.setEnabled(False)

    def enable_add_button (self): 
        if not self.txt_name.text().strip() == "" and not self.txt_family.text().strip() == "" and not self.txt_math.text().strip() == "" and not self.txt_geographi.text().strip() == "":
            self.bt_add.setEnabled(True)

    def create_button (self, text, function, row, column):
        button = QPushButton(text)
        button.clicked.connect(function)
        self.buttons_layout.addWidget(button, row, column, 1, 1)
        return button
    
    def create_table (self):
        self.table = QTableView()
        self.tables_layout.addWidget(self.table, 0, 0, 1, 1)
        return self.table

    def disable_field (self):
        self.bt_add.setEnabled(False)
    
    def enable_field (self):
        if not self.txt_name.text().strip() == "" and not self.txt_family.text().strip() == "" and not self.txt_math.text().strip() == "" and not self.txt_geographi.text().strip() == "":
            self.enable_add_button()

        else:
            self.disable_field()

    def clear (self):
        self.txt_name.setText("")
        self.txt_family.setText("")
        self.txt_math.setText("")
        self.txt_geographi.setText("")

##############
class Form_update_data (QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.resize(1300, 400)
        self.setWindowTitle("Update data")
        self.user_data = user_data
        self.upd = update()
        self.insert = show()


        main_layout = QGridLayout()

        self.lables_and_boxes_layout = QGridLayout()
        self.buttons_layout = QGridLayout()
        self.tables_layout = QGridLayout()

        self.txt_name = self.create_lables_and_boxes ("Name", 0, 0)
        self.txt_family = self.create_lables_and_boxes ("Family", 1, 0)
        self.txt_math = self.create_lables_and_boxes ("Math", 2, 0)
        self.txt_geographi = self.create_lables_and_boxes ("Geographi", 3, 0)
        self.txt_id = self.create_lables_and_boxes ("ID", 4, 0)
        self.bt_update = self.create_button("Update", self.update_data, 0, 0)
        self.create_button("Return to menu", self.return_menu, 0, 1)
        self.create_table()

        main_layout.addLayout(self.lables_and_boxes_layout, 0, 0, 1, 1)
        main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        main_layout.addLayout(self.tables_layout, 0, 1, 2, 1)
        self.setLayout(main_layout)

        self.show_data()
        self.disable_button()

    def update_data (self):
        Name = self.txt_name.text().strip()
        Family = self.txt_family.text().strip() 
        Math = self.txt_math.text().strip()
        Geographi = self.txt_geographi.text().strip()
        student_id = self.txt_id.text().strip()

        if not Name.replace(" ", "").isalpha() or not Family.replace(" ", "").isalpha() or not Math.replace(".","", 1).isnumeric() or not Geographi.replace(".", "", 1).isnumeric() or not student_id.isnumeric():
            message = ""
            if not Name.replace(" ", "").isalpha():
                message += "Name "

            if not Family.replace(" ", "").isalpha():
                message += "Family "

            if not Math.replace(".","", 1).isnumeric():
                message += "Math "

            if not Geographi.replace(".", "", 1).isnumeric():
                message += "Geographi "

            if not student_id.isnumeric():
                message += "ID "
            self.clear()
            self.message_box(f"{message}is not cerroct")
            
        else:
            try:
                message = self.upd.update(Name, Family, Math, Geographi, student_id, self.user_data)
                self.show_data()
                self.clear()
                self.message_box(message)
            except:
                self.message_box("Could not update student, please try again")

    def return_menu (self):
        self.close()
        self.form_teacher = Form_teacher(self.user_data)
        self.form_teacher.show()

    def create_button (self, text, function, row, column):
        button = QPushButton(text)
        button.clicked.connect(function)
        self.buttons_layout.addWidget(button, row, column, 1, 1)
        return button

    def create_lables_and_boxes (self, sub_text, row, column):
        label = QLabel(sub_text)
        self.lables_and_boxes_layout.addWidget(label, (row * 2), column, 1, 1)
        txt = QLineEdit()
        self.lables_and_boxes_layout.addWidget(txt, (row * 2 + 1), column, 1, 1)
        txt.textChanged.connect(self.enable_button)
        return txt

    def create_table (self):
        self.table = QTableView()
        self.tables_layout.addWidget(self.table, 0, 0, 1, 1)
        return self.table

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

    def show_data (self):
        try:
            self.rows = self.insert.select(self.user_data)
            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
                width = self.width() // 2 - 16
                number_of_columns = len(self.rows[0])
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.message_box("table is empty")
        except:
            self.message_box("Could not load students list")
            return

    def disable_button (self):
        self.bt_update.setEnabled(False)

    def enable_button (self):
        if not self.txt_name.text().strip() == "" and not self.txt_family.text().strip() == "" and not self.txt_math.text().strip() == "" and not self.txt_geographi.text().strip() == "" and not self.txt_id.text().strip() == "":
            self.bt_update.setEnabled(True)

        else:
            self.bt_update.setEnabled(False)

    def clear (self):
        self.txt_name.setText("")
        self.txt_family.setText("")
        self.txt_math.setText("")
        self.txt_geographi.setText("")
        self.txt_id.setText("")

##############
class Form_show_data (QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.resize(1300, 400)
        self.show_data
        self.setWindowTitle("Show data")
        self.user_data = user_data
        self.insert = show()

        main_layout = QGridLayout()

        self.buttons_layout = QGridLayout()
        self.tables_layout = QGridLayout()

        self.create_button("Return to menu", self.return_menu, 0, 0)
        self.table = self.create_table()

        main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        main_layout.addLayout(self.tables_layout, 0, 0, 1, 1)
        self.setLayout(main_layout)

        self.show_data()
    
    def return_menu (self):
        self.close()
        self.form_teacher = Form_teacher(self.user_data)
        self.form_teacher.show()

    def create_table (self):
        self.table = QTableView()
        self.tables_layout.addWidget(self.table, 0, 0, 1, 1)
        return self.table

    def create_button (self, text, function, row, column):
        button = QPushButton(text)
        button.clicked.connect(function)
        self.buttons_layout.addWidget(button, row, column, 1, 1)
        return button

    def show_data (self):
        try:
            self.rows = self.insert.select(self.user_data)
            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
                width = self.width() - 25
                number_of_columns = len(self.rows[0])
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.message_box("table is empty")
        except:
            self.message_box("Could not load students list")
            return

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

##############
class Form_search_data (QWidget): 
    def __init__(self, user_data):
        super().__init__()
        self.resize(1300, 250)
        self.setWindowTitle("Search data")
        self.user_data = user_data
        self.search = search()
        self.select = show()
        self.ComboBox = ""
        self.RadioBox = ""

        main_layout = QGridLayout()

        self.lable_1_layout = QGridLayout()
        self.lable_2_layout = QGridLayout()
        self.radio_buttons_layout = QGridLayout()
        self.combo_box_layout = QGridLayout()
        self.lables_and_boxes_layout = QGridLayout()
        self.buttons_layout = QGridLayout()
        self.tables_layout = QGridLayout()


        self.create_lable("Search by", self.lable_1_layout, 0, 0)

        self.cmb_search = self.create_combo_box()

        self.create_lable("Search Type", self.lable_2_layout, 0, 0)

        self.rb_start = self.create_radio_button("Starts with", 0, 0)
        self.rb_end = self.create_radio_button("Ends with", 0, 1)
        self.rb_contain = self.create_radio_button("Contain", 0, 2)
        self.rb_equal = self.create_radio_button("Equals", 0, 3)

        self.field_txt = self.create_lables_and_boxes("Field", 0, 0)

        self.bt_search = self.create_button("Search", self.search_data, 0, 0)
        self.create_button("Return to menu", self.return_menu, 0, 1)

        self.create_table()

        main_layout.addLayout(self.lable_1_layout, 0, 0, 1, 1)
        main_layout.addLayout(self.combo_box_layout, 1, 0, 1, 1)
        main_layout.addLayout(self.lable_2_layout, 2, 0, 1, 1)
        main_layout.addLayout(self.radio_buttons_layout, 3, 0, 1, 1)
        main_layout.addLayout(self.lables_and_boxes_layout, 4, 0, 1, 1)
        main_layout.addLayout(self.buttons_layout, 5, 0, 1, 1)
        main_layout.addLayout(self.tables_layout, 0, 1, 6, 1)
        self.setLayout(main_layout)  

        self.disable_field()
        self.disable_radio_button()
        self.disable_button()
        self.show_data()

    def create_lable (self, sub_text, layout, row, column):
        label = QLabel(sub_text)
        layout.addWidget(label, row, column, 1, 1)

    def create_combo_box (self):
        combo_box = QComboBox()
        combo_box.addItems(["ID", "Name", "Family", "Math", "Geographi"])
        combo_box.setCurrentIndex(-1)
        combo_box.currentTextChanged.connect(self.change_QComboBox_to_text)
        combo_box.currentTextChanged.connect(self.enable_radio_button)
        self.combo_box_layout.addWidget(combo_box)
        return combo_box
    
    def create_radio_button (self, text, row, column):
        radio = QRadioButton(text)
        radio.toggled.connect(self.change_QRadioButton_to_text)
        radio.toggled.connect(self.enable_field)
        self.radio_buttons_layout.addWidget(radio, row, column, 1, 1)
        return radio

    def search_data (self):
        value = self.field_txt.text().strip()

        if not ((self.ComboBox.strip() == "Name" and value.replace(" ", "").isalpha()) or (self.ComboBox.strip() == "Family" and value.replace(" ", "").isalpha()) or (self.ComboBox.strip() == "Math" and value.replace(".","", 1).isnumeric()) or (self.ComboBox.strip() == "Geographi" and value.replace(".","", 1).isnumeric()) or (self.ComboBox.strip() == "ID" and value.isnumeric())):
            self.clear()
            self.message_box(f"{self.ComboBox.strip()} is not cerroct")
        else:
            try:
                self.rows = self.search.search(self.ComboBox, self.RadioBox, value, self.user_data)
                if self.rows:
                    model = Model(self.rows)
                    self.table.setModel(model)

                    width = self.width() // 2
                    number_of_columns = len(self.rows[0])

                    for i in range(number_of_columns):
                        self.table.setColumnWidth(i, width // number_of_columns - 7)
                else:
                    self.message_box("no resault")
            except:
                self.message_box("Search failed, please try again")

    def change_QComboBox_to_text (self, text):
        self.ComboBox = str(text)

    def change_QRadioButton_to_text (self):
        sender:QRadioButton = self.sender()
        if sender.isChecked():
            self.RadioBox = str(sender.text())

    def enable_field (self):
        if self.RadioBox in ("Starts with", "Ends with", "Contain", "Equals") and self.ComboBox in ("ID", "Name", "Family", "Math", "Geographi"):
            self.field_txt.setEnabled(True)

        else:
            self.field_txt.setEnabled(False)

    def disable_field (self):
        self.field_txt.setEnabled(False)

    def disable_radio_button (self):
        self.rb_start.setEnabled(False)
        self.rb_end.setEnabled(False)
        self.rb_contain.setEnabled(False)
        self.rb_equal.setEnabled(False)

    def disable_button (self):
        self.bt_search.setEnabled(False)

    def enable_button (self):
        if not self.field_txt.text().strip() == "" and self.RadioBox in ("Starts with", "Ends with", "Contain", "Equals") and self.ComboBox in ("ID", "Name", "Family", "Math", "Geographi"):
            self.bt_search.setEnabled(True)

        else:
            self.bt_search.setEnabled(False)

    def enable_radio_button(self):
        if self.ComboBox in ("Name", "Family"):
            self.rb_start.setEnabled(True)
            self.rb_end.setEnabled(True)
            self.rb_contain.setEnabled(True)
            self.rb_equal.setEnabled(True)

        elif self.ComboBox in ("ID", "Math", "Geographi"):
            self.rb_start.setEnabled(False)
            self.rb_end.setEnabled(False)
            self.rb_contain.setEnabled(False)
            self.rb_equal.setEnabled(True)
            self.rb_equal.animateClick()
            self.enable_field()

        else:
            self.rb_start.setEnabled(False)
            self.rb_end.setEnabled(False)
            self.rb_contain.setEnabled(False)
            self.rb_equal.setEnabled(False)
   
    def return_menu (self):
        self.close()
        self.form_teacher = Form_teacher(self.user_data)
        self.form_teacher.show()

    def create_button (self, text, function, row, column):
        button = QPushButton(text)
        button.clicked.connect(function)
        self.buttons_layout.addWidget(button, row, column, 1, 1)
        return button

    def create_lables_and_boxes (self, sub_text, row, column):
        label = QLabel(sub_text)
        self.lables_and_boxes_layout.addWidget(label, (row * 2), column, 1, 1)
        txt = QLineEdit()
        self.lables_and_boxes_layout.addWidget(txt, (row * 2 + 1), column, 1, 1)
        txt.textChanged.connect(self.enable_button)
        return txt

    def create_table (self):
        self.table = QTableView()
        self.tables_layout.addWidget(self.table, 0, 0, 1, 1)
        return self.table

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

    def show_data (self):
        try:
            self.rows = self.select.select(self.user_data)
            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
                width = self.width() // 2 - 16
                number_of_columns = len(self.rows[0])
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.message_box("table is empty")
        except:
            self.message_box("Could not load students list")
            return

    def clear (self):
        self.field_txt.setText("")
# endregion

#############################
# region form student
class Form_student (QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.resize(1300, 100)
        self.setWindowTitle("Student panel")
        self.user_data = user_data
        self.insert = student()

        main_layout = QGridLayout()
        self.tables_layout = QGridLayout()

        self.table = self.create_table()

        main_layout.addLayout(self.tables_layout, 0, 0, 1, 1)
        self.setLayout(main_layout)

        self.show_data()

    def create_table (self):
        self.table = QTableView()
        self.tables_layout.addWidget(self.table, 0, 0, 1, 1)
        return self.table

    def show_data (self):
        try:
            self.rows = self.insert.select(self.user_data[0][0], "TBLdata.db")

            ali = self.insert.select(self.user_data[0][7], "TBLdata.db")
            self.rows = self.insert.select2(ali[0][0][0:-3], self.user_data[0][8], ali[0][0])

            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
                width = self.width() - 25
                number_of_columns = len(self.rows[0])
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.message_box("table is empty")
        except:
            self.message_box("Could not load your information")
            return

    def message_box (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()
# endregion

desk_app = QApplication([])
form = Login()
form.show()
form.setWindowTitle("LogIn")
sys.exit(desk_app.exec())
