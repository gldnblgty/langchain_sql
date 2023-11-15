import pandas as pd
import csv
from sqlite3 import Connection
import os
print("Current working directory:", os.getcwd())

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, "../data/booksummaries.txt")

class DataParser:
    def __init__(self, sqlite_db: Connection) -> None:
        self.sqlite_db = sqlite_db
    
    def parse_txt_to_sqlite(self) -> pd.DataFrame:
        data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f, dialect='excel-tab')
            for row in reader:
                data.append(row)

        # convert data to pandas dataframe
        books = pd.DataFrame.from_records(data, columns=['book_id', 'freebase_id', 'book_title', 'author', 'publication_date', 'genre', 'summary'])
        books.to_sql("books", self.sqlite_db, if_exists="replace", index=False)
        return books