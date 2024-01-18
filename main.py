import os
import sys
from datetime import datetime
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog

class Home_page(QMainWindow):
    def __init__(self):
        super(Home_page, self).__init__()
        loadUi("app.ui", self)
        self.search_B.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'F:\Python Projects\Report Generator')
        file_path = fname[0]
        file_name = os.path.basename(file_path)
        
        creation_time = os.path.getctime(file_path)
        creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"File Name: {file_name}\nCreation Date: {creation_date}")

        self.Dir.setText(file_name)
        self.Dir_date.setText(creation_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    home = Home_page()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(home)
    
    width = 1000
    height = 700
    widget.setGeometry(100, 100, width, height)
    widget.setWindowTitle(" Report Generator App")
    
    widget.show()
    
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred:", e)
