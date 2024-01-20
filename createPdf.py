import pandas as pd
from fpdf import FPDF
import plotly.express as px
from PIL import Image
from io import BytesIO


class CreatePDF:
    def __init__(self, DB_path):
        super(CreatePDF, self).__init__()
        
        self.pdf = FPDF()
        
        self.DB_path = DB_path
        self.df = pd.read_excel(self.DB_path)

        self.file_path = 'preferences.txt'
        self.preferences = []

    def readPreference(self):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    line = eval(line)
                    self.preferences.append(line)

        except FileNotFoundError:
            print("Error: File 'preferences.txt' not found.")

        except Exception as e:
            print(f"An error occurred: {e}")

        self.executePreference()

    def executePreference(self):
        requirement_functions = {
            'Table': self.process_table,
            'Bar chart': self.process_bar_chart,
            'Pie chart': self.process_pie_chart,
            'Line chart': self.process_line_chart,
            'Scatter plot': self.process_scatter_plot,
        }

        for preference in self.preferences:
            self.requirement = preference.get('requirement', '')
            self.variables = [value for key, value in preference.items() if key.startswith('variable')]

            print(f"self.requirement: {self.requirement}")
            print(f"self.variables: {self.variables}")

            if self.requirement in requirement_functions:
                requirement_functions[self.requirement](self.df, self.variables)
            else:
                print("Unsupported requirement:", self.requirement)
                
        self.outputPdf()
    
    def process_table(self, df, variables_df):
        if variables_df:
            try:
                selected_df = df[variables_df]  # No need to use pd.read_excel again, just select the columns
            except Exception as e:
                print(f"An error occurred: {e}")
                return

        if selected_df is not None:
            selected_df = selected_df.applymap(str)
            columns = [list(selected_df)]  # Get list of dataframe columns
            rows = selected_df.values.tolist()  # Get list of dataframe rows
            data = columns + rows  # Combine columns and rows in one list
            
            self.pdf.add_page()
            self.pdf.set_font("Times", size=10)
            with self.pdf.table(borders_layout="MINIMAL",
                        cell_fill_color=200,  # grey
                        cell_fill_mode="ROWS",
                        line_height=self.pdf.font_size * 1,
                        text_align="CENTER",
                        width=160) as table:
                
                for data_row in data:
                    row = table.row()
                    for datum in data_row:
                        row.cell(datum)
                        
        else:
            print("No data selected.")

        print("Processing Table with variables:")
        print(variables_df)
    
    
    def process_bar_chart(self, df, variables_df):
            
        print("Processing Bar chart with variables:")
        print(variables_df)


    def process_pie_chart(self, df, variables_df):
        # Your logic for processing Pie chart
        print("Processing Pie chart with variables:")
        print(variables_df)


    def process_line_chart(self, df, variables_df):
        # Your logic for processing Line chart
        print("Processing Line chart with variables:")
        print(variables_df)


    def process_scatter_plot(self, df, variables_df):
        # Your logic for processing Scatter plot
        print("Processing Scatter plot with variables:")
        print(variables_df)
    
    
    def outputPdf(self):
        self.pdf.output("table_from_pandas.pdf")
    

pdf_creator = CreatePDF("ProductionDataLog.xlsx")
pdf_creator.readPreference()
