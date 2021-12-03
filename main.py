from ui import *

app = QApplication(sys.argv)

login = Login()

if(login.exec_() == QDialog.Accepted):
    ui = UI()
    ui.show()
    sys.exit(app.exec_())