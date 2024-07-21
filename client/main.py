from PyQt5.QtWidgets import QApplication
import sys
from login_window import LoginWindow

app = QApplication(sys.argv)
mainwindow = LoginWindow()

try:
    sys.exit(app.exec_())
except:
    print("Exiting Astra AI")
    
