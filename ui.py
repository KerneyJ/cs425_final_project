import sys
import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from database import Connection

test_results = [ ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fishuyfhcgbhjajlsuydtcasyitdbh'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', 'askuydgavoskucbhaksb2', 'go', 'fish'),
                    ('wow nice', 'oh my gof', '1', '2', 'go', 'fish'),]

class Login(QDialog):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)

        self.view = None
        self.setWindowTitle("User Login")

        layout = QHBoxLayout(self)

        self.create_login_tab()
        self.create_registration_tab()

        tab_widget = QTabWidget()
        tab_widget.addTab(self.login_tab, "Log in")
        tab_widget.addTab(self.registration_tab, "Register")
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
    
    def create_registration_tab(self):
        self.r_account_type = QComboBox()
        self.r_account_type.addItems(["Patient", "Blood Donor", "Organ Donor", "Doctor"])
        self.r_account_type.currentIndexChanged.connect(self.add_registration_info)
        self.r_username = QLineEdit(self)
        self.r_password = QLineEdit(self)
        self.registration_button = QPushButton('Login', self)
        self.registration_button.clicked.connect(self.register)

        self.registration_info = QFormLayout()
        info = QGroupBox("Information")
        info.setLayout(self.registration_info)

        self.add_registration_info(0)

        layout = QFormLayout()
        layout.addRow("Account type:", self.r_account_type)
        layout.addRow("Username:", self.r_username)
        layout.addRow("Password:", self.r_password)
        layout.addRow(info)
        layout.addRow(self.registration_button)

        self.registration_tab = QGroupBox()
        self.registration_tab.setLayout(layout)

    def add_registration_info(self, idx):
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        options_list = [ # Patient blood donor organ donor doctor
            [("Name:", "text"), ("Blood type:", 'drop-down', blood_types), ("DOB:", 'text'), ('Email:', 'text'), ('Phone:', 'text')],
            [("Name:", "text"), ("Blood type:", 'drop-down', blood_types), ("DOB:", 'text'), ('Email:', 'text'), ('Phone:', 'text'), ('City:', 'text'), ('State:', 'text'), ('Drug Usage:', 'text'), ('Medical History:', 'text'), ('Chronic Ilness:', 'text')],
            [("Name:", "text"), ("Blood type:", 'drop-down', blood_types), ("DOB:", 'text'), ('Email:', 'text'), ('Phone:', 'text'), ('City:', 'text'), ('State:', 'text'), ('Drug Usage:', 'text'), ('Medical History:', 'text'), ('Chronic Ilness:', 'text'), ('Organ to Donate:', 'text')],
            [("Name:", "text"), ("DOB:", 'text'), ('Email:', 'text'), ('Phone:', 'text'), ('Organ Specialty', 'text')],
        ]

        self.add_options(self.registration_info, options_list[idx])

    def add_options(self, layout, options):
            for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().setParent(None)

            if(options == []):
                return
            
            for option in options:
                if(option[1] == 'text'):
                    widget = QLineEdit()
                elif(option[1] == 'drop-down'):
                    widget = QComboBox()
                    widget.addItems(option[2])
                elif(option[1] == 'date'):
                    widget = QDateEdit()

                if(widget):
                    layout.addRow(QLabel(option[0]), widget)

    def register(self):
        parameters = []

        for i in range(self.registration_info.count()): 
            if(i % 2 == 0):
                continue

            if(type(self.registration_info.itemAt(i).widget()) is QLineEdit):            
                text = self.registration_info.itemAt(i).widget().text()
            else:
                text = self.registration_info.itemAt(i).widget().currentText()

            parameters.append(text)

        account_type = self.r_account_type.currentText()[0].lower()
        username = self.r_username.text()
        password = self.r_password.text()

        if(account_type == "p"):
            Connection.regist_mreq(account_type, username, password, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
        elif(account_type == "b"):
            Connection.regist_mreq(account_type, username, password, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], parameters[7], parameters[8], parameters[9])
        elif(account_type == "o"):
            Connection.regist_mreq(account_type, username, password, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6], parameters[7], parameters[8], parameters[9], parameters[10])
        elif(account_type == "d"):
            Connection.regist_mreq(account_type, username, password, parameters[0], None, parameters[1], parameters[2], parameters[3], None, None, None, None, None, None, parameters[4])

    def login(self):
        self.connection = None
        try:
            conn = Connection(self.username.text(), self.password.text())
        except psycopg2.OperationalError:
            QMessageBox.warning(self, 'Error', 'Failed password authentication')
            return
        except Exception as e:
            print(e)
            QMessageBox.warning(self, 'Error', str(e))
            return

        self.accept()
        self.connection = conn
        self.view = self.account_type.currentText()

    def sign_up(self):
        account = self.account_drop.currentText()
        user = self.n_username.text()
        password = self.n_password.text()
        print(f"Create new user: {account} / {user} / {password}")

class UI(QMainWindow):
    def __init__(self, view, connection: Connection):
        super(UI, self).__init__(None)

        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        self.connection = connection

        self.tabs = [(self.create_query_tab, 'ADP'),
                     (self.create_report_tab, 'AD'),
                     (self.create_donation_tab, 'AD'),
                     (self.create_admin_tab, 'A'),
                     (self.create_organ_request_tab, 'P'),
                     (self.create_approval_tab, 'A'),
                     (self.create_registration_approval_tab, 'A'),]

        self.view = view
        self.setWindowTitle("Hospital Database")
        self.setGeometry(600, 100, 800, 800)
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

    def create_organ_request_tab(self):
        label = QLabel("Request an Organ:")
        self.organ_request = QLineEdit()
        self.organ_state = QLineEdit()
        submit_button = QPushButton('Submit Request')
        submit_button.clicked.connect(self.request_organ)

        layout = QFormLayout()
        layout.addWidget(label)
        layout.addRow("Organ name:", self.organ_request)
        layout.addRow("State:", self.organ_state)
        layout.addWidget(submit_button)

        self.organ_tab = QGroupBox()
        self.organ_tab.setLayout(layout)
        self.tab_widget.addTab(self.organ_tab, "Request Organ")

    def request_organ(self):
        organ = self.organ_request.text()
        state = self.organ_state.text()
        self.connection.make_request(organ, state)
        self.organ_request.setText('')

    def create_approval_tab(self):
        self.request_id = QLineEdit()
        self.doctor_id = QLineEdit()
        self.approve_button = QPushButton('Approve Request')
        self.approve_button.clicked.connect(self.approve_request)
        self.deny_button = QPushButton('Deny Request')
        self.deny_button.clicked.connect(self.deny_request)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.approve_button)
        button_layout.addWidget(self.deny_button)

        t_layout = QFormLayout()
        t_layout.addRow('Request ID', self.request_id)
        t_layout.addRow('Doctor ID (N/A for denials)', self.doctor_id)
        t_layout.addRow(button_layout)

        top = QGroupBox("Handle Requests")
        top.setLayout(t_layout)

        self.request_results_layout = QVBoxLayout()
        request_display = QGroupBox("View Requests")
        request_display.setLayout(self.request_results_layout)
        scroll = QScrollArea()
        scroll.setWidget(request_display)
        scroll.setWidgetResizable(True)

        self.load_requests()

        layout = QVBoxLayout()
        layout.addWidget(top)
        layout.addWidget(scroll)

        self.approval_tab = QGroupBox()
        self.approval_tab.setLayout(layout)
        self.tab_widget.addTab(self.approval_tab, "Handle Requests")

    def load_requests(self):
        # TODO fetch all pending requests
        results = self.connection.get_request()

        self.display_list(self.request_results_layout, results)

    def approve_request(self):
        request_id = self.request_id.text()
        doctor_id = self.doctor_id.text()

        self.connection.approve_request(request_id, doctor_id)
        self.load_requests()

    def deny_request(self):
        request_id = self.request_id.text()
        
        self.connection.reject_request(request_id)
        self.load_requests()

    def create_query_tab(self):
        query_list = ['None', 'Organ Donor List', 'Blood Donor List', 'Donor Match List']
        
        self.query_type = QComboBox()
        self.query_type.addItems(query_list)
        self.query_type.currentIndexChanged.connect(self.create_query_options)

        self.query_layout = QFormLayout()
        query_options = QGroupBox("Options")
        query_options.setLayout(self.query_layout)

        self.query_results_layout = QVBoxLayout()
        query_display = QGroupBox("Results")
        query_display.setLayout(self.query_results_layout)
        scroll = QScrollArea()
        scroll.setWidget(query_display)
        scroll.setWidgetResizable(True)

        self.query2_results_layout = QVBoxLayout()
        query2_display = QGroupBox("Results")
        query2_display.setLayout(self.query2_results_layout)
        self.scroll2 = QScrollArea()
        self.scroll2.setWidget(query2_display)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.query_type)
        layout.addWidget(query_options)
        layout.addWidget(scroll)
        layout.addWidget(self.scroll2)
        # layout.addStretch()

        self.query_tab = QGroupBox()
        self.query_tab.setLayout(layout)
        self.tab_widget.addTab(self.query_tab, "Donor Lists")

    def create_report_tab(self):
        report_list = ['None', 'Income Report', 'Operations Report']

        report_type = QComboBox()
        report_type.addItems(report_list)
        report_type.currentIndexChanged.connect(self.create_report)

        self.report_results_layout = QVBoxLayout()
        report_display = QGroupBox("Results")
        report_display.setLayout(self.report_results_layout)
        scroll = QScrollArea()
        scroll.setWidget(report_display)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(report_type)
        layout.addWidget(scroll)
        # layout.addStretch()

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
        self.tab_widget.addTab(self.admin_tab, "Add Users")

    def create_donation_tab(self):
        label = QLabel("Create new donor:")
        self.n_donor_name = QLineEdit()
        self.n_donor_DOB = QDateEdit()
        self.n_donor_blood = QComboBox()
        self.n_donor_blood.addItems(self.blood_types)
        self.n_donor_city = QLineEdit()
        self.n_donor_state = QLineEdit()
        self.n_donor_illness = QLineEdit()
        self.n_donor_drug_usage = QLineEdit()
        self.n_donor_email = QLineEdit()
        self.n_donor_phone = QLineEdit()
        self.n_donor_organ = QLineEdit()
        self.n_donor_medhist = QLineEdit()
        self.sign_up_button = QPushButton('Create Donor', self)
        self.sign_up_button.clicked.connect(self.create_donor)

        t_layout = QFormLayout()
        t_layout.addWidget(label)
        t_layout.addRow("Name:", self.n_donor_name)
        t_layout.addRow("DOB:", self.n_donor_DOB)
        t_layout.addRow("Blood type:", self.n_donor_blood)
        t_layout.addRow("City:", self.n_donor_city)
        t_layout.addRow("State:", self.n_donor_state)
        t_layout.addRow("Chronic Ilnesses:", self.n_donor_illness)
        t_layout.addRow("Medical History: ", self.n_donor_medhist)
        t_layout.addRow("Drug usage:", self.n_donor_drug_usage)
        t_layout.addRow("Email:", self.n_donor_email)
        t_layout.addRow("Phone:", self.n_donor_phone)
        t_layout.addRow("Organ (leave empty for blood donors):", self.n_donor_organ)
        t_layout.addRow(self.sign_up_button)

        donation_options = QGroupBox("Options")
        self.donation_layout = QFormLayout()
        donation_options.setLayout(self.donation_layout)
        
        label = QLabel("Create new donation:")
        self.donation_type = QComboBox()
        self.donation_type.addItems(['None', 'Blood', 'Organ'])
        self.donation_type.currentIndexChanged.connect(self.create_donation_options)

        b_layout = QVBoxLayout()
        b_layout.addWidget(label)
        b_layout.addWidget(self.donation_type)
        b_layout.addWidget(donation_options)

        top = QGroupBox()
        top.setLayout(t_layout)

        bottom = QGroupBox()
        bottom.setLayout(b_layout)

        layout = QVBoxLayout()
        layout.addWidget(top)
        layout.addWidget(bottom)
        layout.addStretch()

        self.admin_tab = QGroupBox()
        self.admin_tab.setLayout(layout)
        self.tab_widget.addTab(self.admin_tab, "New Donations")

    def create_user(self):
        account = self.account_drop.currentText()
        user = self.n_username.text()
        password = self.n_password.text()
        print('creating user')
        
        if account == 'Doctor':
            self.connection.create_doc_acc(self.n_username.text(), self.n_password.text())
        else:
            self.connection.create_pat_acc(self.n_username.text(), self.n_password.text())
        # print(f"Create new user: {account} / {user} / {password}")

    def create_query_options(self, idx):
        options_list = [[], 
                        [('State', 'text', 'IL'), ('Organ', 'text', '')],
                        [('State', 'text', 'IL'), ('Blood type', 'drop-down', self.blood_types), ('Availability', 'text', ''), ('Age Group', 'drop-down', ['0-15','16-64','65+'])],
                        [('State', 'text', 'IL'), ('Blood type', 'drop-down', self.blood_types), ('Organ', 'text', '')]]
        
        if(idx == 1):
            self.scroll2.show()
        else:
            self.scroll2.hide()

        self.query_idx = idx
        self.add_options(self.query_layout, options_list[idx], self.run_query)
        
    def create_donation_options(self, idx):
        options_list = [[], 
                        [('Donor name', 'text'), ('Donor DOB', 'text'), ('Blood type', 'drop-down', self.blood_types), ('City', 'text'), ('State', 'text')],
                        [('Organ name', 'text'), ('Donor name', 'text'), ('DOB', 'text'), ('Blood type', 'drop-down', self.blood_types), ('City', 'text'), ('State', 'text')]]
        
        self.add_options(self.donation_layout, options_list[idx], self.create_donation)

    def add_options(self, layout, options, func):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

        if(options == []):
            return
        
        for option in options:
            if(option[1] == 'text'):
                widget = QLineEdit()
            elif(option[1] == 'drop-down'):
                widget = QComboBox()
                widget.addItems(option[2])
            elif(option[1] == 'date'):
                widget = QDateEdit()

            if(widget):
                layout.addRow(QLabel(option[0]), widget)

        submit_button = QPushButton()
        submit_button.setText("Run Query")
        submit_button.clicked.connect(func)

        layout.addWidget(submit_button)

    def run_query(self):
        parameters = []

        for i in range(self.query_layout.count()): 
            if(i % 2 == 0):
                continue

            if(type(self.query_layout.itemAt(i).widget()) is QLineEdit):            
                text = self.query_layout.itemAt(i).widget().text()
            else:
                text = self.query_layout.itemAt(i).widget().currentText()

            parameters.append(text)
        
        if(self.query_idx == 1):
            results = self.connection.organ_donor_list(parameters[0], parameters[1])
            self.display_list(self.query2_results_layout, results[1])
            results = results[0]
        elif(self.query_idx == 2):
            if '-' in parameters[3]:
                parameters[3] = parameters[3].split('-')
            else:
                parameters[3] = (65, 1000)
            results = self.connection.blood_donor_list(parameters[0], parameters[1], parameters[3], parameters[2])
        elif(self.query_idx == 3):
            results = self.connection.donor_match_list(parameters[0], parameters[1], parameters[2])

        self.display_list(self.query_results_layout, results)

    def create_registration_approval_tab(self):
        self.r_request_id = QLineEdit()
        self.r_approve_button = QPushButton('Approve Request')
        self.r_approve_button.clicked.connect(self.approve_registration)
        self.r_deny_button = QPushButton('Deny Request')
        self.r_deny_button.clicked.connect(self.deny_registration)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.r_approve_button)
        button_layout.addWidget(self.r_deny_button)

        t_layout = QFormLayout()
        t_layout.addRow('Request ID', self.r_request_id)
        t_layout.addRow(button_layout)

        top = QGroupBox("Handle Requests")
        top.setLayout(t_layout)

        self.request_r_results_layout = QVBoxLayout()
        request_display = QGroupBox("View Requests")
        request_display.setLayout(self.request_r_results_layout)
        scroll = QScrollArea()
        scroll.setWidget(request_display)
        scroll.setWidgetResizable(True)

        self.load_registration_requests()

        layout = QVBoxLayout()
        layout.addWidget(top)
        layout.addWidget(scroll)

        self.registration_tab = QGroupBox()
        self.registration_tab.setLayout(layout)
        self.tab_widget.addTab(self.registration_tab, "Handle Registrations")

    def load_registration_requests(self):
        # TODO fetch all pending requests
        results = Connection.regist_sreq()

        self.display_list(self.request_r_results_layout, results)

    def approve_registration(self):
        request_id = self.r_request_id.text()
        self.connection.regist_areq(request_id)

    def deny_registration(self):
        request_id = self.r_request_id.text()
        self.connection.regist_rreq(request_id)

    def create_donor(self):
        name = self.n_donor_name.text()
        DOB = self.n_donor_DOB.date()
        blood_type = self.n_donor_blood.currentText()
        city = self.n_donor_city.text()
        state = self.n_donor_state.text()

        print(f"{name} / {DOB.month()}-{DOB.day()}-{DOB.year()} / {blood_type} / {city} / {state}")
        if self.n_donor_organ.text() == '':
            self.connection.add_Bdonor( self.n_donor_name.text(),
                                        self.n_donor_blood.currentText(),
                                        self.n_donor_DOB.text(),
                                        self.n_donor_illness.text(),
                                        self.n_donor_drug_usage.text(),
                                        self.n_donor_medhist.text(),
                                        QDate.currentDate().toString(),
                                        self.n_donor_city.text(),
                                        self.n_donor_state.text(),
                                        self.n_donor_email.text(),
                                        self.n_donor_phone.text())
        else:
            self.connection.add_Odonor( self.n_donor_name.text(),
                                        self.n_donor_blood.currentText(),
                                        self.n_donor_DOB.text(),
                                        self.n_donor_illness.text(),
                                        self.n_donor_drug_usage.text(),
                                        self.n_donor_medhist.text(),
                                        self.n_donor_city.text(),
                                        self.n_donor_state.text(), 
                                        self.n_donor_organ.text(),
                                        self.n_donor_email.text(),
                                        self.n_donor_phone.text())

    def create_donation(self):
        parameters = []

        for i in range(self.donation_layout.count()): 
            if(i % 2 == 0):
                continue

            widget = self.donation_layout.itemAt(i).widget()
            if(type(widget) is QLineEdit):            
                text = widget.text()
            elif(type(widget) is QComboBox):
                text = widget.currentText()
            elif(type(widget) is QDateEdit):
                text = widget.date()

            parameters.append(text)
        
        print(parameters)
        today = QDate.currentDate()
        today_str = str(today.year()) + '-' + str(today.month()) + '-' + str(today.day())

        if len(parameters) == 5:
            print('adding blood')
            self.connection.create_donation(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], today_str)
            print('has added blood')
        else:
            print('adding organ')
            self.connection.create_donation(parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], today_str, parameters[0])
            print('has added organ')

    def create_report(self, i):
        if(i == 0):
            self.display_list(self.report_results_layout, [])
            return
        elif(i==1): # income
            results = self.connection.finacial_report()
        elif(i==2): # operations
            results = self.connection.operations_report()

        # results = test_results

        self.display_list(self.report_results_layout, results)

    def display_list(self, layout, lst):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

        if len(lst) == 0:
            return
        
        max_width = int(100 / (len(lst[0])))

        for row in lst:
            lay = QHBoxLayout()            
            for el in row:
                text = str(el)[:max_width-2] + '..' if len(str(el)) > max_width else str(el)
                label = QLabel(text)
                lay.addWidget(label)
                
            group = QGroupBox()
            group.setLayout(lay)
            layout.addWidget(group)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = Login()

    if(login.exec_() == QDialog.Accepted):
        ui = UI(login.view)
        ui.show()
        sys.exit(app.exec_())
