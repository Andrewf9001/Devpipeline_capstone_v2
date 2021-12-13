import sqlite3
from datetime import datetime

class Assessments:
    def __init__(self):
        assessment_id = None
        comp_id = None
        name = None
        date_created = None


    def set_all(self, comp_id, name, date_created):
        self.comp_id = comp_id
        self.name = name
        self.date_created = date_created


    def save_assessment(self, cursor):
        insert_sql = '''
            INSERT INTO Assessments 
                (comp_id, name, date_created)
            VALUES
                (?, ?, ?)
        ;'''

        cursor.execute(insert_sql, (self.comp_id, self.name, self.date_created))
        cursor.connection.commit()

        new_assessment = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.assessment_id = new_assessment[0]


    def load_assessment(self, cursor):
        select_sql = '''
            SELECT assessment_id, comp_id, name, date_created 
            FROM Assessments
            WHERE assessment_id = ?;
        '''

        row = cursor.execute(select_sql, (self.assessment_id,)).fetchone()

        if not row:
            print("No Results")
            return
        
        self.comp_id = row[1]
        self.name = row[2]
        self.date_created = row[3]

    
    def print_me(self):
        print(f'{self.comp_id} {self.name}, {self.date_created}')
        print(f'{self.assessment_id}')


    # def load_comp_assessment(self, cursor):
    #     join_sql = '''
    #         SELECT co.comp_id, co.name
    #         FROM Assessments ast
    #         JOIN Competency co
    #         ON co.comp_id = ast.assessment_id
    #         WHERE ast.assessment_id = ?
    #         ORDER BY co.comp_id;
    #     '''

    #     row = cursor.execute(join_sql).fetchone()


class AssessmentResults:
    def __init__(self):
        user_id = None
        assessment_id = None
        score = None
        date_taken = None
        manager = None

    def set_all(self, user_id, assessment_id, score, date_taken, manager = None):
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.score = score
        self.date_taken = date_taken
        self.manager = manager

    def save_a_result(self, cursor):
        insert_sql = '''
            INSERT INTO AssessmentResults 
                (user_id, assessment_id, score, date_taken, manager)
            VALUES
                (?, ?, ?, ?, ?)
        ;'''

        cursor.execute(insert_sql, (self.user_id, self.assessment_id, self.score, self.date_taken, self.manager))
        cursor.connection.commit()

        new_assessment_result = cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.assessment_id = new_assessment_result[0]

    def load_assessment(self, u_id, cursor):
        select_sql = '''
            SELECT user_id, assessment_id, score, date_taken, manager 
            FROM AssessmentResults
            WHERE user_id = ?;
        '''

        row = cursor.execute(select_sql, (u_id,)).fetchone()

        if not row:
            print("No Results")
            return
        
        self.user_id = row[0]
        self.assessment_id = row[1]
        self.score = row[2]
        self.date_taken = row[3]
        self.manager = row[4]

    
    def print_me(self):
        print(f'{self.user_id} {self.assessment_id}, {self.score}')
        print(f'{self.date_taken} {self.manager}')

# connection = sqlite3.connect('competency.db')
# cursor = connection.cursor()

# new_results = AssessmentResults()
# new_results.set_all(2, 11, 2, "12-11-2021 02:00:00", "1")
# new_results.save_a_result(cursor)
# new_results.print_me()