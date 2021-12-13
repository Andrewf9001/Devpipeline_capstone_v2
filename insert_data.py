import sqlite3
from datetime import datetime

def create_tables(cursor):

    with open('sql_tables.sql') as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)

    connection.commit()             


def create_competency(cursor):
    count_competency = '''
        SELECT count(comp_id) FROM Competency;
    '''

    count = cursor.execute(count_competency)

    for row in count:
        if row[0] == 0:
            insert_compentencies(cursor)



def create_assessments(cursor):
    count_assessments = '''
        SELECT count(assessment_id) FROM Assessments;
    '''

    count = cursor.execute(count_assessments)

    for row in count:
        if row[0] == 0:
            insert_assessments(cursor)


def insert_compentencies(cursor):
    new_date = datetime.now()
    date_time_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
    comp_list = [
        "Data Types",
        "Variables",
        "Functions",
        "Boolean Logic",
        "Conditionals",
        "Loops",
        "Data Structures",
        "Lists",
        "Dictionaries",
        "Working with Files",
        "Exception Handling",
        "Quality Assurance (QA)",
        "Object-Oriented Programming",
        "Recursion",
        "Databases"
    ]

    for item in comp_list:
        insert_sql = '''
        INSERT INTO Competency
            (name, date_created)
        VALUES 
            (?, ?)
        ;'''

        cursor.execute(insert_sql, (item, date_time_str))
    cursor.connection.commit()


def insert_assessments(cursor):
    new_date = datetime.now()
    date_time_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
    comp_list = [
        [1, "Data Types Compentency Measure"],
        [1, "Data Types Best Practices"],
        [2, "Variables Compentency Measure"],
        [2, "Variables Best Practices"],
        [3, "Functions Compentency Measure"],
        [3, "Functions Best Practices"],
        [4, "Boolean Logic Compentency Measure"],
        [4, "Boolean Logic Best Practices"],
        [5, "Conditionals Compentency Measure"],
        [5, "Conditionals Best Practices"],
        [6, "Loops Compentency Measure"],
        [6, "Loops Best Practices"],
        [7, "Data Structures Compentency Measure"],
        [7, "Data Structures Best Practices"],
        [8, "Lists Compentency Measure"],
        [8, "Lists Best Practices"],
        [9, "Dictionaries Compentency Measure"],
        [9, "Dictionaries Best Practices"],
        [10, "Working with Files Compentency Measure"],
        [10, "Working with Files Best Practices"],
        [11, "Exception Handling Compentency Measure"],
        [11, "Exception Handling Best Practices"],
        [12, "Quality Assurance (QA) Compentency Measure"],
        [12, "Quality Assurance (QA) Best Practices"],
        [13, "Object-Oriented Programming Compentency Measure"],
        [13, "Object-Oriented Programming Best Practices"],
        [14, "Recursion Compentency Measure"],
        [14, "Recursion Best Practices"],
        [15, "Databases Compentency Measure"],
        [15, "Databases Best Practices"]
    ]

    for item in comp_list:
        insert_sql = '''
        INSERT INTO Assessments
            (comp_id, name, date_created)
        VALUES 
            (?, ?, ?)
        ;'''

        cursor.execute(insert_sql, (item[0], item[1], date_time_str))
    cursor.connection.commit()

connection = sqlite3.connect('competency.db')
cursor = connection.cursor()

create_tables(cursor)
create_competency(cursor)
create_assessments(cursor)