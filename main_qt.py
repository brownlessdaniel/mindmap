import sys
from PyQt5.QtWidgets import QApplication
from application.qtwindow import MyWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
