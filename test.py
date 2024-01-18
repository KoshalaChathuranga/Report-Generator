import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QPushButton, QListWidget, QCheckBox
import pandas as pd

class FileBrowserApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV File Browser')

        # Create widgets
        self.file_list = QListWidget()
        self.open_button = QPushButton('Open CSV File')
        self.display_button = QPushButton('Display Column Titles')

        # Connect signals
        self.open_button.clicked.connect(self.showDialog)
        self.display_button.clicked.connect(self.displayColumnTitles)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.file_list)
        layout.addWidget(self.open_button)
        layout.addWidget(self.display_button)
        self.setLayout(layout)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV files (*.csv);;All files (*)')[0]
        if fname:
            self.file_list.addItem(fname)

    def displayColumnTitles(self):
        if self.file_list.count() > 0:
            selected_file = self.file_list.item(0).text()
            df = pd.read_csv(selected_file)
            column_titles = df.columns.tolist()

            title_checkbox_widgets = []
            for title in column_titles:
                checkbox = QCheckBox(title)
                title_checkbox_widgets.append(checkbox)

            # Show the checkable buttons in a dialog
            self.showCheckableButtonsDialog(title_checkbox_widgets)

    def showCheckableButtonsDialog(self, title_checkbox_widgets):
        dialog = QWidget()
        dialog.setWindowTitle('Column Titles')
        dialog.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        for checkbox in title_checkbox_widgets:
            layout.addWidget(checkbox)

        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowserApp()
    file_browser.show()
    sys.exit(app.exec_())
