import os
import sys
from datetime import datetime
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtWidgets import QMessageBox
from dataAnalyzer import *

class Home_page(QMainWindow):
    def __init__(self):
        super(Home_page, self).__init__()
        loadUi("app.ui", self)
        self.datetime_checked = False
        self.textTodetails = None
        self.Selected_itemToadd = ''
        self.Selected_itemToremove = ''
        self.variable_list = {}
        self.dateTime_From.setDateTime(QDateTime.currentDateTime())
        self.dateTime_To.setDateTime(QDateTime.currentDateTime())
        
        self.B_add.clicked.connect(self.addRequirement)
        self.B_clear.clicked.connect(self.clearList)
        self.search_B.clicked.connect(self.browsefiles)
        self.B_clearAll.clicked.connect(self.clearpreferences)
        
        self.check_DatenTime.stateChanged.connect(self.addDataTime)
        self.dateTime_From.dateTimeChanged.connect(self.dateTime_From_changed)
        self.dateTime_To.dateTimeChanged.connect(self.dateTime_To_changed)
        

        self.B_addTolist.clicked.connect(self.addItem)
        self.B_removeFromlist.clicked.connect(self.removeItem)
        
        self.clearDetails()
    
    def dateTime_From_changed(self, datetime):
        selected_Fromdate = datetime.date()
        selected_Fromtime = datetime.time()
        
        self.from_date = selected_Fromdate.toString("dd-MM-yyyy")
        self.from_time = selected_Fromtime.toString("hh:mm:ss")
        #print((f"Selected From_Date: {self.from_date},\nSelected From_Time: {self.from_time}\n"))
        
    def dateTime_To_changed(self, datetime):
        selected_Todate = datetime.date()
        selected_Totime = datetime.time()
        
        self.To_date = selected_Todate.toString("dd-MM-yyyy")
        self.To_time = selected_Totime.toString("hh:mm:ss")
        #print((f"Selected To_Date: {self.To_date},\nSelected To_Time: {self.To_time}\n"))
    
    def clearDetails(self):
        clearTxtFile(path = "detail.txt")
        
    
    def clearpreferences(self):
        clearTxtFile()
        self.list_Req.clear()
            
      
    def load_preferences(self):
        available_preferences = readtxt()
        
        for preferences in available_preferences:
            self.list_Req.addItem(preferences)
            

    def browsefiles(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'F:/Python Projects/Report Generator')
        file_path = fname
        file_name = os.path.basename(file_path)
        
        if file_name:
            self.textTodetails = f"File Name: {file_name}"
            writeTotxt(self.textTodetails, 'detail.txt')
                   
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"File Name: {file_name}\nCreation Date: {creation_date}")
            self.textTodetails = f"Date & Time (created): {creation_date}"
            writeTotxt(self.textTodetails, 'detail.txt')

            self.Dir.setText(file_name)
            self.Dir_date.setText(creation_date)
            self.DisplayDetails(file_path) 
            
            self.load_preferences()
            
            self.list_ToSelect.itemClicked.connect(self.itemToadd)
            self.list_Selected.itemClicked.connect(self.itemToremove)
    
    def DisplayDetails(self, file_path):
        try:
            file_details, message = get_excel_file_details(file_path)
            
            if file_details is not None:                
                self.list_Details.addItem(f'Number of Rows: {file_details["NumRows"]}')
                print(f'Number of Rows: {file_details["NumRows"]}\n')
                
                self.list_Details.addItem(f'Number of Columns: {file_details["NumColumns"]}')
                print(f'Number of Columns: {file_details["NumColumns"]}\n')
                
                self.list_Details.addItem(f'Number of N/A Values: {file_details["NumNAValues"]}')
                print(f'Number of N/A Values: {file_details["NumNAValues"]}\n')
                
                print(f'Number of N/A Values: {file_details["ColumnNames"]}\n')
                for col_name in file_details['ColumnNames']:
                    self.list_ToSelect.addItem(col_name)
                    
            else:
                print(f'Error: {message}')
                QMessageBox.warning(self, 'Error', 'No details about the Excel file.')
                return
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
    
    
    def itemToadd(self, item_1):
        self.Selected_itemToadd = item_1.text()
        print(f'to add, {self.Selected_itemToadd} is selected\n')
       
        
    def itemToremove(self, item_2):
        self.Selected_itemToremove = item_2.text()
        print(f'to add, {self.Selected_itemToremove} is selected\n')


    def addItem(self):
        self.list_Selected.addItem(self.Selected_itemToadd)
        print(f"{self.list_Selected} is added\n")

    def removeItem(self):
        if self.Selected_itemToremove:
            self.list_Selected.takeItem(self.list_Selected.row(self.list_Selected.selectedItems()[0]))
            print(f"{self.Selected_itemToremove} is removed\n")
        else:
            print("No item selected for removal\n")
    
    
    def clearList(self):
        self.list_Selected.clear()
        print("List cleared\n")
    
    
    def addRequirement(self):
        requirement = self.comboBox_Req.currentText()
        self.variable_list["requirement"] = requirement
        
        if self.datetime_checked:
            self.variable_list["From_Date"] = self.from_date
            self.variable_list["From_Time"] = self.from_time
            self.variable_list["To_Date"] = self.To_date
            self.variable_list["To_Date"] = self.To_date

        for index in range(self.list_Selected.count()): 
            item = self.list_Selected.item(index)            
            key = f"variable {index}"
            value = item.text()
            self.variable_list[key] = value
        
        writeTotxt(self.variable_list)
        self.list_Req.addItem(str( self.variable_list))
    
    def addDataTime(self, state):
        if state == 2:
            self.datetime_checked = True
        else: 
            self.datetime_checked = False
                    
                    
                              
if __name__ == "__main__":
    app = QApplication(sys.argv)
    home = Home_page()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(home)
    
    width = 1000
    height = 700
    widget.setFixedHeight(height)
    widget.setFixedWidth(width)
    widget.setWindowTitle("Report Generator App")
    
    widget.show()
    
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("An error occurred:", e)
