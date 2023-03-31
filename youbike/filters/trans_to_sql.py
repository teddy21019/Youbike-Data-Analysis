from pathlib import Path
import csv
import sqlite3

# define paths to relevant folders
parent_folder = Path("../")
data_folder = parent_folder / "DATA"
sql_folder = parent_folder / "SQL"

# search for csv files in data folder
csv_files = list(data_folder.glob("*.csv"))

# iterate through csv files and check for corresponding db files in sql folder
for csv_file in csv_files:
    db_file = sql_folder / f"{csv_file.stem}.db"
    if not db_file.exists():
        # create a new database file based on the csv file
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        with open(csv_file, "r") as f:
            csv_reader = csv.reader(f)
            headers = next(csv_reader)
            headers_str = ",".join(headers)
            placeholders = ",".join(["?" for _ in headers])
            create_table_query = f"CREATE TABLE data ({headers_str})"
            cursor.execute(create_table_query)

            for row in csv_reader:
                insert_query = f"INSERT INTO data VALUES ({placeholders})"
                cursor.execute(insert_query, row)

        conn.commit()
        conn.close()
