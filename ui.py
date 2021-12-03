import sys
import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from database import Connection

class Login(QDialog):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)

        self.view = None
        self.setWindowTitle("User Login")

        layout = QHBoxLayout(self)

        self.create_login_tab()

        tab_widget = QTabWidget()
        tab_widget.addTab(self.login_tab, "Log in")
        layout.addWidget(tab_widget)

    def create_login_tab(self):
        self.account_type = QComboBox()
        self.account_type.addItems(["Patient", "Doctor", "Admin"])
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        layout = QFormLayout()
        layout.addRow("Account type:", self.account_type)
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addRow(self.login_button)

        self.login_tab = QGroupBox()
        self.login_tab.setLayout(layout)

    def login(self):
        self.connection = None
        # try:
        #     conn = Connection(self.username.text(), self.password.text())
        # except psycopg2.OperationalError:
        #     QMessageBox.warning(self, 'Error', 'Failed password authentication')
        #     return
        # except Exception as e:
        #     print(e)
        #     QMessageBox.warning(self, 'Error', str(e))
        #     return

        self.accept()
        # self.connection = conn
        self.view = self.account_type.currentText()

    def sign_up(self):
        account = self.account_drop.currentText()
        user = self.n_username.text()
        password = self.n_password.text()
        print(f"Create new user: {account} / {user} / {password}")

class UI(QMainWindow):
    def __init__(self, view):
        super(UI, self).__init__(None)

        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        self.tabs = [(self.create_query_tab, 'ADP'),
                    (self.create_report_tab, 'AD'),
                    (self.create_donation_tab, 'AD'),
                    (self.create_admin_tab, 'A'), ]

        self.view = view
        self.setWindowTitle("Hospital Database")
        self.setGeometry(600, 100, 500, 800)
        self.setFixedSize(self.size())

        content = QWidget(self)
        self.setCentralWidget(content)

        layout = QHBoxLayout()

        self.tab_widget = QTabWidget()

        for tab in self.tabs:
            if self.view[0] in tab[1]:
                tab[0]()

        layout.addWidget(self.tab_widget)
        content.setLayout(layout)

        content.show()

    def create_query_tab(self):
        query_list = ['None', 'Organ Donor List', 'Blood Donor List', 'Donor Match List']
        
        combo_box = QComboBox()
        combo_box.addItems(query_list)
        combo_box.currentIndexChanged.connect(self.add_options)

        query_options = QGroupBox("Options")
        self.form_layout = QFormLayout()
        query_options.setLayout(self.form_layout)

        layout = QVBoxLayout()
        layout.addWidget(combo_box)
        layout.addWidget(query_options)
        layout.addStretch()

        self.query_tab = QGroupBox()
        self.query_tab.setLayout(layout)
        self.tab_widget.addTab(self.query_tab, "Donor Lists")

    def create_report_tab(self):
        report_list = ['None', 'Income Report', 'Operations Report']

        combo_box = QComboBox()
        combo_box.addItems(report_list)
        combo_box.currentIndexChanged.connect(self.create_report)

        layout = QVBoxLayout()
        layout.addWidget(combo_box)
        layout.addStretch()

        self.report_tab = QGroupBox()
        self.report_tab.setLayout(layout)
        self.tab_widget.addTab(self.report_tab, "Reports")

    def create_admin_tab(self):
        label = QLabel("Add new Patient/Doctor:")
        self.account_drop = QComboBox()
        self.account_drop.addItems(["Patient", "Doctor"])
        self.n_username = QLineEdit()
        self.n_password = QLineEdit()
        self.sign_up_button = QPushButton('Create User')
        self.sign_up_button.clicked.connect(self.create_user)

        layout = QFormLayout()
        layout.addWidget(label)
        layout.addRow("Account:", self.account_drop)
        layout.addRow("Username:", self.n_username)
        layout.addRow("Password:", self.n_password)
        layout.addRow(self.sign_up_button)

        self.admin_tab = QGroupBox()
        self.admin_tab.setLayout(layout)
        self.tab_widget.addTab(self.admin_tab, "Admin")

    def create_donation_tab(self):
        # blood type, name, DOB, city, state
        label = QLabel("Create new donor:")
        self.n_donor_name = QLineEdit()
        self.n_donor_DOB = QDateEdit()
        self.n_donor_blood = QComboBox()
        self.n_donor_blood.addItems(self.blood_types)
        self.n_donor_city = QLineEdit()
        self.n_donor_state = QLineEdit()
        self.sign_up_button = QPushButton('Create Donor', self)
        self.sign_up_button.clicked.connect(self.create_donor)

        layout = QFormLayout()
        layout.addWidget(label)
        layout.addRow("Name:", self.n_donor_name)
        layout.addRow("DOB:", self.n_donor_DOB)
        layout.addRow("Blood Type:", self.n_donor_blood)
        layout.addRow("City:", self.n_donor_city)
        layout.addRow("State:", self.n_donor_state)
        layout.addRow(self.sign_up_button)

        self.admin_tab = QGroupBox()
        self.admin_tab.setLayout(layout)
        self.tab_widget.addTab(self.admin_tab, "New Donations")

    def create_user(self):
        account = self.account_drop.currentText()
        user = self.n_username.text()
        password = self.n_password.text()
        print(f"Create new user: {account} / {user} / {password}")

    def add_options(self, idx):
        options_list = [[], 
                        [('State', 'text', 'IL'), ('Organ', 'text', ''), ('Doctor', 'text', '')], 
                        [('State', 'text', 'IL'), ('Blood Type', 'drop-down', self.blood_types), ('Availability', 'text', ''), ('Age Group', 'drop-down', ['0-15','16-64','65+'])],
                        [('State', 'text', 'IL'), ('Blood Type', 'drop-down', self.blood_types), ('Organ', 'text', '')]]

        for i in reversed(range(self.form_layout.count())): 
            self.form_layout.itemAt(i).widget().setParent(None)

        self.query_option = idx
        if(idx == 0):
            return
        
        for option in options_list[idx]:
            if(option[1] == 'text'):
                widget = QLineEdit()
            elif(option[1] == 'drop-down'):
                widget = QComboBox()
                widget.addItems(option[2])

            if(widget):
                self.form_layout.addRow(QLabel(option[0]), widget)

        submit_button = QPushButton()
        submit_button.setText("Run Query")
        submit_button.clicked.connect(self.run_query)

        self.form_layout.addWidget(submit_button)

    def run_query(self):
        parameters = []

        for i in range(self.form_layout.count()): 
            if(i % 2 == 0):
                continue

            if(type(self.form_layout.itemAt(i).widget()) is QLineEdit):            
                text = self.form_layout.itemAt(i).widget().text()
            else:
                text = self.form_layout.itemAt(i).widget().currentText()

            parameters.append(text)

    def create_donor(self):
        name = self.n_donor_name.text()
        DOB = self.n_donor_DOB.date()
        blood_type = self.n_donor_blood.currentText()
        city = self.n_donor_city.text()
        state = self.n_donor_state.text()

        print(f"{name} / {DOB.month()}-{DOB.day()}-{DOB.year()} / {blood_type} / {city} / {state}")

    def create_report(self, i):
        if(i == 0):
            return

        print(self.report_list[i])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = Login()

    if(login.exec_() == QDialog.Accepted):
        ui = UI(login.view)
        ui.show()
        sys.exit(app.exec_())
