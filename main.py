from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from seconde import *
import sys
import re


class Model(QAbstractTableModel):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def data(self, index, role = ...):
        value = self.rows[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            return f"{value}"

        if role == Qt.ItemDataRole.ForegroundRole:
            return QColor("white")

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

class Form_teacher (QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.resize(1150, 400)
        self.teacher = Form_t()

        self.filter = ""
        self.condition = ""

        main_layout = QGridLayout()
        boxes_layout = QGridLayout()
        buttons_layout = QGridLayout()
        combo_layout = QGridLayout()
        radios_layout = QGridLayout()
        tables_layout = QGridLayout()

        label = QLabel("Name")
        boxes_layout.addWidget(label, 0, 0, 1, 1)
        self.txt_name = QLineEdit()
        self.txt_name.textChanged.connect(self.numbers_and_letters)
        boxes_layout.addWidget(self.txt_name, 1, 0, 1, 1)

        label = QLabel("Family")
        boxes_layout.addWidget(label, 2, 0, 1, 1)
        self.txt_family = QLineEdit()
        self.txt_family.textChanged.connect(self.numbers_and_letters)
        boxes_layout.addWidget(self.txt_family, 3, 0, 1, 1)

        label = QLabel("Math")
        boxes_layout.addWidget(label, 4, 0, 1, 1)
        self.txt_math = QLineEdit()
        self.txt_math.textChanged.connect(self.numbers_and_letters)
        boxes_layout.addWidget(self.txt_math, 5, 0, 1, 1)

        label = QLabel("Geographi")
        boxes_layout.addWidget(label, 6, 0, 1, 1)
        self.txt_geographi = QLineEdit()
        self.txt_geographi.textChanged.connect(self.numbers_and_letters)
        boxes_layout.addWidget(self.txt_geographi, 7, 0, 1, 1)

        label = QLabel("ID")
        boxes_layout.addWidget(label, 8, 0, 1, 1)
        self.txt_id = QLineEdit()
        self.txt_id.textChanged.connect(self.numbers_and_letters)
        boxes_layout.addWidget(self.txt_id, 9, 0, 1, 1)

        button = QPushButton("Add")
        button.clicked.connect(self.add_data)
        buttons_layout.addWidget(button, 0, 0, 1, 1)

        button = QPushButton("Update")
        button.clicked.connect(self.update_data)
        buttons_layout.addWidget(button, 0, 1, 1, 1)

        button = QPushButton("Show data")
        button.clicked.connect(self.show_data)
        buttons_layout.addWidget(button, 1, 0, 1, 1)

        button = QPushButton("Search")
        button.clicked.connect(self.search_data)
        buttons_layout.addWidget(button, 1, 1, 1, 1)

        combo_box = QComboBox()
        combo_box.addItems(["ID", "Name", "Family", "Math", "Geographi"])
        combo_box.setCurrentIndex(-1)
        combo_box.currentTextChanged.connect(self.select_filter)
        combo_layout.addWidget(combo_box)

        self.rdbEndsWith = QRadioButton("Ends With")
        self.rdbEndsWith.toggled.connect(self.select_condition)
        radios_layout.addWidget(self.rdbEndsWith, 0, 0, 1, 1)

        self.rdbStartsWith = QRadioButton("Starts With")
        self.rdbStartsWith.toggled.connect(self.select_condition)
        radios_layout.addWidget(self.rdbStartsWith, 0, 1, 1, 1)

        self.rdbContains = QRadioButton("Contains")
        self.rdbContains.toggled.connect(self.select_condition)
        radios_layout.addWidget(self.rdbContains, 0, 2, 1, 1)

        self.rdbEquals = QRadioButton("Equals")
        self.rdbEquals.toggled.connect(self.select_condition)
        radios_layout.addWidget(self.rdbEquals, 0, 3, 1, 1)

        self.table = QTableView()
        self.table.doubleClicked.connect(self.select_row)
        tables_layout.addWidget(self.table, 0, 0, 1, 1)

        main_layout.addLayout(boxes_layout, 0, 0, 1, 1)
        main_layout.addLayout(buttons_layout, 1, 0, 1, 1)
        main_layout.addLayout(radios_layout, 2, 0 ,1, 1)
        main_layout.addLayout(combo_layout, 3, 0, 1, 1)
        main_layout.addLayout(tables_layout, 0, 1, 4, 1)
        self.setLayout(main_layout)
    
    def add_data (self):
        Name = self.txt_name.text().strip()
        Family = self.txt_family.text().strip()
        Math = self.txt_math.text()
        Geographi = self.txt_geographi.text()
        
        if Name == "" or Family == "":
            self.msg("Name or Family is not cerroct")
        else:
            try:
                message = self.teacher.insert(Name, Family, Math, Geographi, self.cursor)

                self.show_data()
                self.clear()
                self.set_index()
                self.msg(message)
            except:
                self.msg("Math or Geographi is not cerroct")

    def update_data (self):
        Name = self.txt_name.text().strip()
        Family = self.txt_family.text().strip() 
        Math = self.txt_math.text()
        Geographi = self.txt_geographi.text()
        id = self.txt_id.text()

        if Name == "" or Family == "":
            self.msg("Name or Family is not crroct")
        else:
            try:
                message = self.teacher.update(Name, Family, Math, Geographi, id, self.cursor)

                self.show_data()
                self.clear()
                self.set_index()
                self.msg(message)
            except:
                self.msg("Math or Geographi or ID is not cerroct")

    def show_data (self):

        self.rows = self.teacher.select(self.cursor)

        model = Model(self.rows)
        self.table.setModel(model)
    
        width = self.table.width()
        number_of_columns = len(self.rows[0])

        for i in range(number_of_columns):
            self.table.setColumnWidth(i, width // number_of_columns - 7)

    def search_data (self):
        try:
            match self.filter:
                case "Name":
                    value = self.txt_name.text()
                case "Family":
                    value = self.txt_family.text()
                case "ID":
                    value = int(self.txt_id.text())
                case "Math":
                    value = int(self.txt_math.text())
                case "Geographi":
                    value = int(self.txt_geographi.text())

            self.rows = self.teacher.search(self.filter, self.condition, value, self.cursor)
            if self.rows:
                model = Model(self.rows)
                self.table.setModel(model)
            
                width = self.table.width()
                number_of_columns = len(self.rows[0])
            
                for i in range(number_of_columns):
                    self.table.setColumnWidth(i, width // number_of_columns - 7)
            else:
                self.msg("no resault")
        except:
            self.msg("field is not complete")

    def select_condition (self):
        sender:QRadioButton = self.sender()
        if sender.isChecked():
            self.condition = sender.text()

    def select_filter (self, text):
        self.filter = text
        if text in ("ID", "Geographi", "Math"):
            self.rdbStartsWith.setEnabled(False)
            self.rdbEndsWith.setEnabled(False)
            self.rdbContains.setEnabled(False)
            self.rdbEquals.setEnabled(True)
            self.rdbEquals.animateClick()
        else:
            self.rdbStartsWith.setEnabled(True)
            self.rdbEndsWith.setEnabled(True)
            self.rdbContains.setEnabled(True)
            self.rdbEquals.setEnabled(True)


    def set_index (self):
        last_row_index = len(self.rows) - 1
        index: QModelIndex = self.table.model().index(last_row_index, 0)
        self.table.setCurrentIndex(index)

    def msg (self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(" ")
        msg_box.setText(message)
        msg_box.exec()

    def clear (self):
        self.txt_name.setText("")
        self.txt_family.setText("")
        self.txt_id.setText("")
        self.txt_math.setText("")
        self.txt_geographi.setText("")

    def numbers_and_letters (self):
        sender:QLineEdit = self.sender()
        old_text = sender.text()
        if sender in (self.txt_math, self.txt_geographi):
            new_text = re.sub("[^0-9.]", "", old_text)
        
        elif sender == self.txt_id:
            new_text = re.sub("[^0-9]", "", old_text)
        
        elif sender in (self.txt_family, self.txt_name):
            new_text = re.sub("[^A-Za-z ]", "", old_text)

        sender.setText(new_text)

    def select_row(self, index: QModelIndex):
        row_index = index.row()
        self.table.selectRow(row_index)
        list = [self.txt_id, self.txt_name, self.txt_family, self.txt_math, self.txt_geographi]
        for i in range (5):
            list[i].setText(f"{self.rows[row_index][i]}")  

class Form_student (QWidget):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        self.resize(540, 125)
        self.student = Form_s()

        main_layout = QGridLayout()

        buttons_layout = QGridLayout()
        tables_layout = QGridLayout()

        button = QPushButton("show data")
        button.clicked.connect(self.show_data)
        buttons_layout.addWidget(button, 0, 0 , 1, 1)

        self.table = QTableView()
        tables_layout.addWidget(self.table, 0, 0, 1, 1)

        main_layout.addLayout(tables_layout, 0, 0)
        main_layout.addLayout(buttons_layout, 1, 0)

        self.setLayout(main_layout)
    
    def show_data (self):
        ali = self.student.select(self.cursor[0][7], "TBLdata.db")
        self.rows = self.student.select2(ali[0][0][0:-3], self.cursor[0][8], ali[0][0])

        model = Model(self.rows)
        self.table.setModel(model)

        width = self.table.width()
        number_of_columns = len(self.rows[0])

        for i in range(number_of_columns):
            self.table.setColumnWidth(i, width // number_of_columns)

class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(350, 125)
        self.form = Form1()

        main_layout = QGridLayout()
        boxes_layout = QGridLayout()
        buttons_layout = QGridLayout()

        label = QLabel("Username")
        boxes_layout.addWidget(label, 0, 0, 1, 1)
        self.txt_username = QLineEdit()
        boxes_layout.addWidget(self.txt_username, 0, 1, 1, 1)

        label = QLabel("Password")
        boxes_layout.addWidget(label, 1, 0, 1, 1)
        self.txt_password = QLineEdit()
        boxes_layout.addWidget(self.txt_password, 1, 1, 1, 1)

        button = QPushButton("Check")
        button.clicked.connect(self.check_data)
        buttons_layout.addWidget(button, 0, 0, 1, 1)

        main_layout.addLayout(boxes_layout, 0, 0)
        main_layout.addLayout(buttons_layout, 1, 0)
        self.setLayout(main_layout)


    def check_data (self):
        username = self.txt_username.text()    
        password = self.txt_password.text()

        try:
            cursor = self.form.select(username, password, "TBLdata.db")
            if cursor[0][5] == "teacher":
                self.close()
                self.form_teacher = Form_teacher(cursor)
                self.form_teacher.show()
                self.form_teacher.setWindowTitle("teacher panel")
            elif cursor[0][5] == "student":
                self.close()
                self.form_student = Form_student(cursor)
                self.form_student.show()
                self.form_student.setWindowTitle("student panel")
        except:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(" ")
            msg_box.setText("Username or Password not cerroct")
            msg_box.exec()
            self.txt_username.setText("")
            self.txt_password.setText("")

app = QApplication([])
form = Form()
form.show()
form.setWindowTitle("LogIn")
sys.exit(app.exec())