import sqlite3
from datetime import datetime

class Compentency:
    def __init__(self):
        self.comp_id = None
        self.name = None
        self.date_created = None
    

    def set_all(self, name, date_created):
        self.name = name
        self.date_created = date_created


    def save_comp(self, cursor):
        insert_sql = '''
            INSERT INTO Competency
                (name, date_created)
            VALUES
                (?, ?);
        '''

        cursor.execute(insert_sql, (self.name, self.date_created))
        cursor.connection.commit()

        new_comp = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.comp_id = new_comp[0]


    def load_comp(self, c_id, cursor):
        select_sql = '''
            SELECT comp_id, name, date_created, active
            FROM Competency
            WHERE comp_id = ?;
        '''

        row = cursor.execute(select_sql, (c_id, )).fetchone()
        if not row:
            print("No Results")
        self.name = row[1]
        self.date_created = row[2]