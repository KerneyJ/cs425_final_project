import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Login(QDialog):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)

        self.view = None
        self.setWindowTitle("User Login")

        layout = QHBoxLayout(self)

        self.create_login_tab()
        self.create_sign_up_tab()

        tab_widget = QTabWidget()

        tab_widget.addTab(self.login_tab, "Log in")
        tab_widget.addTab(self.sign_up_tab, "Sign up")

        layout.addWidget(tab_widget)

    def create_login_tab(self):
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        layout = QFormLayout()
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        layout.addRow(self.login_button)

        self.login_tab = QGroupBox()
        self.login_tab.setLayout(layout)
    
    def create_sign_up_tab(self):
        self.account_drop = QComboBox()
        self.account_drop.addItems(["Patient", "Doctor"])
        self.n_username = QLineEdit(self)
        self.n_password = QLineEdit(self)
        self.sign_up_button = QPushButton('Login', self)
        self.sign_up_button.clicked.connect(self.sign_up)

        layout = QFormLayout()
        layout.addRow("Account:", self.account_drop)
        layout.addRow("Username:", self.n_username)
        layout.addRow("Password:", self.n_password)
        layout.addRow(self.sign_up_button)

        self.sign_up_tab = QGroupBox()
        self.sign_up_tab.setLayout(layout)

    def login(self):
        user = self.username.text()
        password = self.password.text()
        print(f"Logging in: {user} / {password}")

        if(True):
            self.view = "Doctor"
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def sign_up(self):
        account = self.account_drop.currentText()
        user = self.n_username.text()
        password = self.n_password.text()
        print(f"Create new user: {account} / {user} / {password}")

class UI(QMainWindow):
    def __init__(self, view):
        super(UI, self).__init__(None)

        self.query_list = ['None', 'Organ Donor List', 'Blood Donor List', 'Donor Match List']
        self.options_list = [[], 
                            [('State', 'text', 'IL'), ('Organ', 'text', ''), ('Doctor', 'text', '')], 
                            [('State', 'text', 'IL'), ('Blood Type', 'drop-down', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']), ('Availability', 'text', ''), ('Age Group', 'drop-down', ['0-15','16-64','65+'])],
                            [('State', 'text', 'IL'), ('Blood Type', 'drop-down', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']), ('Organ', 'text', '')]]

        self.report_list = ['None', 'Income Report', 'Operations Report']

        self.view = view
        self.setWindowTitle("Hospital Database")
        self.setGeometry(600, 300, 500, 800)
        self.setFixedSize(self.size())

        content = QWidget(self)
        self.setCentralWidget(content)

        layout = QHBoxLayout()

        self.create_query_tab()
        self.create_report_tab()

        tab_widget = QTabWidget()

        tab_widget.addTab(self.query_tab, "Donor Lists")
        tab_widget.addTab(self.report_tab, "Reports")
        layout.addWidget(tab_widget)
        content.setLayout(layout)

        content.show()

    def create_query_tab(self):
        self.query_tab = QGroupBox()
        
        layout = QVBoxLayout()

        combo_box = QComboBox()
        combo_box.addItems(self.query_list)
        combo_box.currentIndexChanged.connect(self.add_options)

        query_options = QGroupBox("Options")
        self.form_layout = QFormLayout()
        query_options.setLayout(self.form_layout)

        layout.addWidget(combo_box)
        layout.addWidget(query_options)
        layout.addStretch()

        self.query_tab.setLayout(layout)

    def create_report_tab(self):
        self.report_tab = QGroupBox()
        
        layout = QVBoxLayout()

        combo_box = QComboBox()
        combo_box.addItems(self.report_list)
        combo_box.currentIndexChanged.connect(self.create_report)

        layout.addWidget(combo_box)

        layout.addStretch()

        self.report_tab.setLayout(layout)

    def add_options(self, idx):
        for i in reversed(range(self.form_layout.count())): 
            self.form_layout.itemAt(i).widget().setParent(None)

        self.query_option = idx
        if(idx == 0):
            return
        
        for option in self.options_list[idx]:
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

        print(f"{self.query_list[self.query_option]}: ")
        for i in range(self.form_layout.count()): 
            if(i % 2 == 0):
                continue

            if(type(self.form_layout.itemAt(i).widget()) is QLineEdit):            
                text = self.form_layout.itemAt(i).widget().text()
            else:
                text = self.form_layout.itemAt(i).widget().currentText()

            parameters.append(text)

    def create_report(self, i):
        if(i == 0):
            return

        print(self.report_list[i])

app = QApplication(sys.argv)

login = Login()

if(login.exec_() == QDialog.Accepted):
    view = login.view
    ui = UI(view)
    ui.show()
    sys.exit(app.exec_())