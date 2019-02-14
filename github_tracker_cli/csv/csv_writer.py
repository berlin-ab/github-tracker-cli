from backports import csv


class CsvWriter():
    def __init__(self, stdout):
        self.header_columns = []
        self.row_columns = []
        self.stdout = stdout
        
    def write_header(self, header_columns):
        self.internal_writer = csv.DictWriter(
            self.stdout,
            fieldnames=header_columns,
            quoting=csv.QUOTE_ALL
        )
        self.internal_writer.writeheader()

    def write_row(self, row_columns):
        self.internal_writer.writerow(row_columns)

    
