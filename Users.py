import sqlite3
import bcrypt

class Users:
    def __init__(self):
        self.user_id = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.email = None
        self.active = None
        self.date_created = None
        self.hire_date = None
        self.user_type = None
        self.__password = None


    def set_all(self, first_name, last_name, phone, email, password, date_created, user_type = "User", hire_date = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.date_created = date_created
        self.user_type = user_type
        self.hire_date = hire_date
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    def change_password(self, new_password):
        if new_password:
            self.__password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())


    def get_password(self):
        return self.__password
    
    def change_email(self, new_email):
        self.email = new_email

    
    def check_password(self, email, new_password, cursor):
        row = cursor.execute("SELECT password FROM Users WHERE email = ?",(email,)).fetchone()
            
        hashed_password = row[0]

        valid_password = bcrypt.hashpw(new_password.encode('utf-8'), hashed_password)
        if valid_password == hashed_password:
            select_sql = '''
                SELECT email FROM Users WHERE password = ? AND email = ?;
            '''

            row = cursor.execute(select_sql, (valid_password, email)).fetchone()

            return (row != None)

    
    def save_user(self, cursor):
        insert_sql = '''
            INSERT INTO Users
                (first_name, last_name, phone, email, password, date_created, user_type, hire_date)
            VALUES
                (?, ?, ?, ?, ?, ?, ?, ?);
        '''

        cursor.execute(insert_sql, (self.first_name, self.last_name, self.phone, self.email, self.__password, self.date_created, self.user_type, self.hire_date))
        cursor.connection.commit()

        new_user_id = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.user_id = new_user_id[0]


    def print_me(self):
        print(f'{self.user_id}: {self.last_name}, {self.first_name}')
        print(f'  {self.email} - {self.user_type}')
        print(f'  Created: {self.date_created}')
        print(f'  Hire Date: {self.hire_date}')


    def load(self, email, cursor):
        select_sql = '''
            SELECT user_id, first_name, last_name, phone, email, date_created, hire_date, user_type, active
            FROM Users
            WHERE email = ?;
        '''

        row = cursor.execute(select_sql, (email, )).fetchone()

        if not row:
            return
        self.user_id = row[0]
        self.first_name = row[1]
        self.last_name = row[2]
        self.phone = row[3]
        self.email = row[4]
        self.date_created = row[5]
        self.hire_date = row[6]
        self.user_type = row[7]


    def get_user_type(self, cursor):
        select_sql = '''
            SELECT user_type
            FROM Users
            WHERE user_id = ?;
        '''

        user_row = cursor.execute(select_sql, (self.user_id, )) #.fetchone()

        for row in user_row:
            return row[0]