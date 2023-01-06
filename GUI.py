import sys
from PyQt5.QtWidgets import QApplication
from GridWidget import GridDialog

# run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = GridDialog()
    dialog.show()
    dialog.setFixedSize(dialog.size())
    app.exec()

