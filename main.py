from os.path import exists
import sqlite3
import time
from datetime import datetime
import csv

import insert_data
from Users import *
from Competency import *
from Assessments import *

connection = sqlite3.connect('competency.db')
cursor = connection.cursor()

def main(cursor):
    manager_create(cursor)


# USERS VIEWS
def view_users_table(cursor):
    users_sql = '''
        SELECT user_id, first_name, last_name, email, date_created, user_type
        FROM Users
        WHERE active = 1
        ORDER BY user_type;
    '''

    rows = cursor.execute(users_sql).fetchall()

    if not rows:
        print("\nNo Users\n")
        return

    print(f'\n{"ID":>3} {"First":<8} {"Last":<10} {"Email":<20} {"Date Created":<22} {"User Type"}')
    print(f"{'-'*77}")
    for row in rows:
        print(f'{row[0]:>2}. {row[1]:<8} {row[2]:<10} {row[3]:<20} {row[4]:<22} {row[5]}')


def view_users_and_types(cursor):
    users_sql = '''
        SELECT user_id, first_name, last_name
        FROM Users
        WHERE user_type = 'User' AND active = 1;
    '''

    rows = cursor.execute(users_sql).fetchall()

    if not rows:
        print("No Users")
        return

    print(f'\n{"ID":>3}  {"First":<8} {"Last"}')
    print(f'{"-"*18}')

    for row in rows:
        print(f'{row[0]:>3}. {row[1]:<8} {row[2]}')


def view_managers_and_types(cursor):
    users_sql = '''
        SELECT user_id, first_name, last_name
        FROM Users
        WHERE user_type = 'Manager' AND active = 1;
    '''

    rows = cursor.execute(users_sql).fetchall()

    if not rows:
        print("No Managers")
        return

    print(f'\n{"ID":>3}  {"First":<8} {"Last"}')
    print(f'{"-"*18}')

    for row in rows:
        print(f'{row[0]:>3}. {row[1]:<8} {row[2]}')


def search_users(cursor):
    search_sql = '''
        SELECT user_id, first_name, last_name, email, user_type
        FROM Users
        WHERE first_name = ? OR last_name = ?;
    '''
    print("\nSearch user by First or Last name")

    search_input = input('\nEnter Search: ').title()

    row = cursor.execute(search_sql, (search_input, search_input)).fetchone()

    if not row:
        print("\nNo Results\n")
        return
    else:
        print(f'\n{"ID":>3}  {"First":<8} {"Last":<10} {"Email":<15} {"User Type"}')
        print(f'{"-"*50}')
        print(f"{row[0]:>3}. {row[1]:<8} {row[2]:<10} {row[3]:<15} {row[4]}\n")


def view_user_name(u_id, cursor):
    select_sql = '''
        SELECT first_name, last_name
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    print(f'\n{row[0]}, {row[1]}')


def view_user_information(u_id, cursor):
    select_sql = '''
        SELECT user_id, first_name, last_name, phone, email, date_created, user_type, hire_date
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()
    # print(row)

    print(f'\n{"ID":>2}  {"First":<8} {"Last":<10} {"Phone":<12} {"Email":<20} {"Date Created":<21} {"User Type":<10} {"Hire Date":<5}')
    print(f'{"-"*100}')
    print(f'{row[0]:>2}. {row[1]:<8} {row[2]:<10} {row[3]:<12} {row[4]:<20} {row[5]:<21} {row[6]:^10} {row[7]}')


def get_first_name(u_id, cursor):
    select_sql = '''
        SELECT first_name
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def get_last_name(u_id, cursor):
    select_sql = '''
        SELECT last_name
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def get_phone(u_id, cursor):
    select_sql = '''
        SELECT phone
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def get_email(u_id, cursor):
    select_sql = '''
        SELECT email
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def get_single_user_type(u_id, cursor):
    select_sql = '''
        SELECT user_type
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def get_hire_date(u_id, cursor):
    select_sql = '''
        SELECT hire_date
        FROM Users
        WHERE user_id = ?;
    '''

    row = cursor.execute(select_sql, (u_id,)).fetchone()

    return row[0]


def edit_user_information(cursor):
    print("\n-*- Edit User -*-")
    view_users_table(cursor)

    print("\nPlease select the ID of the user to edit")
    edit_user_input = int(input())

    view_user_information(edit_user_input, cursor)
    print("\nBeginning edit, please follow the prompts")
    print("Press (enter) to skip field\n")

    first_name_check = get_first_name(edit_user_input, cursor)
    first_name_input = input("First Name: ").title()
    if first_name_input == '':
        first_name_input = first_name_check

    last_name_check = get_last_name(edit_user_input, cursor)
    last_name_input = input("Last Name: ").title()
    if last_name_input == '':
        last_name_input = last_name_check

    phone_check = get_phone(edit_user_input, cursor)
    phone_input = input("Phone: ")
    if phone_input == '':
        phone_input = phone_check

    email_check = get_email(edit_user_input, cursor)
    email_input = input("Email: ").title()
    if email_input == '':
        email_input = email_check

    user_type_check = get_single_user_type(edit_user_input, cursor)
    user_type_input = input("User Type: ").title()
    if user_type_input == '':
        user_type_input = user_type_check

    print("\nIs the User going to be hired? [(Y)es, (N)o]")
    hiring = input().lower()
    new_hire = None

    if hiring == 'n':
        pass
    elif hiring == 'y':
        new_hire = get_date()

    update_user_sql = '''
        UPDATE Users
        SET first_name = ?, last_name = ?, phone = ?, email = ?, user_type = ?, hire_date = ?
        WHERE user_id = ?;
    '''

    cursor.execute(update_user_sql, (first_name_input, last_name_input, phone_input, email_input, user_type_input, new_hire, edit_user_input))
    connection.commit()


def exporting_users(cursor):
    users_sql = '''
        SELECT user_id, first_name, last_name, email, date_created, user_type
        FROM Users
        WHERE active = 1
        ORDER BY user_type DESC;
    '''

    rows = cursor.execute(users_sql).fetchall()

    if not rows:
        print("\nNo Users\n")
        return

    return rows

# COMPETENCY VIEWS
def view_competency_table(cursor):
    comp_sql = '''
        SELECT comp_id, name, date_created
        FROM Competency
        WHERE active = 1;
    '''

    rows = cursor.execute(comp_sql).fetchall()

    if not rows:
        print("\nNo Competencies\n")
        return

    print(f'\n{"ID":<5} {"Name":<28} {"Date Created"}')
    print(f"{'-'*54}")
    for row in rows:
        print(f'{row[0]:>2}. {row[1]:<30} {row[2]}')


def exporting_competency(cursor):
    comp_sql = '''
        SELECT comp_id, name, date_created
        FROM Competency
        WHERE active = 1;
    '''

    rows = cursor.execute(comp_sql).fetchall()

    if not rows:
        print("\nNo Competencies\n")
        return
    return rows


def view_single_comp(c_id, cursor):
    comp_sql = '''
        SELECT name
        FROM Competency
        WHERE comp_id = ?;
    '''

    row = cursor.execute(comp_sql, (c_id, )).fetchone()

    print(f'\n{row[0]}\n')


def comp_report_all_users(cursor):
    print("\n-*- Users Competency Report -*-\n")
    view_competency_table(cursor)
    print("\nPlease choose a competency ID to view\n")

    competency_input = int(input())
    print()
    
    comp_report_sql = '''
        SELECT u.first_name, u.last_name, a.name, ar.score
        FROM AssessmentResults ar
        JOIN Users u
        ON u.user_id = ar.user_id
        JOIN Assessments a
        ON a.assessment_id = ar.assessment_id
        JOIN Competency c
        ON c.comp_id = a.comp_id
        WHERE c.comp_id = ?
        ORDER BY u.first_name;
    '''
    
    rows = cursor.execute(comp_report_sql, (competency_input, )).fetchall()

    if not rows:
        print("\nNo users to report\n")
        return
    else:
        view_single_comp(competency_input, cursor)
        print(f'{"First":<10} {"Last":<10} {"Assessment":<35} {"Score"}')
        print(f'{"-"*63}')
        for row in rows:
            print(f'{row[0]:<10} {row[1]:<10} {row[2]:<35} {row[3]:^5}')
        print()


def view_all_comps_by_user(cursor):
    print("\n-*- All User Competencies -*-\n")
    view_users_and_types(cursor)
    print("\nPlease select the ID of the user you'd like to look up")

    user_input = int(input())
    print()

    user_comp_sql = '''
        SELECT u.first_name, c.name, a.name, ar.score
        FROM AssessmentResults ar
        JOIN Users u
        ON u.user_id = ar.user_id
        JOIN Assessments a
        ON a.assessment_id = ar.assessment_id
        JOIN Competency c
        ON c.comp_id = a.comp_id
        WHERE u.user_id = ?
        ORDER BY c.name;
    '''

    rows = cursor.execute(user_comp_sql, (user_input, )).fetchall()

    if not rows:
        print("No results\n")
        return
    else:
        view_single_comp(user_input, cursor)
        print(f'{"First":<10} {"Competency":<20} {"Assessment":<35} {"Score"}')
        print(f'{"-"*73}')
        for row in rows:
            print(f'{row[0]:<10} {row[1]:<20} {row[2]:<35} {row[3]:^5}')
        print()


def view_competency_of_user(u_id, cursor):
    print("\n-*- Your Competencies and Assessments -*-\n")

    user_comp_sql = '''
        SELECT u.first_name, c.name, a.name, ar.score
        FROM AssessmentResults ar
        JOIN Users u
        ON u.user_id = ar.user_id
        JOIN Assessments a
        ON a.assessment_id = ar.assessment_id
        JOIN Competency c
        ON c.comp_id = a.comp_id
        WHERE u.user_id = ?
        ORDER BY c.name;
    '''

    rows = cursor.execute(user_comp_sql, (u_id, )).fetchall()

    if not rows:
        print("No results\n")
        return
    else:
        print(f'{"Competency":<20} {"Assessment":<35} {"Score"}')
        print(f'{"-"*73}')
        for row in rows:
            print(f'{row[1]:<20} {row[2]:<35} {row[3]:^5}')
        print()


def comp_level_report(cursor):
    print("\n-*- Competency Average -*-\n")

    view_users_and_types(cursor)
    print("\nPlease select a User ID")
    user_id_input = int(input())
    print()

    view_competency_table(cursor)
    print("\nPlease select a Competency ID")
    comp_id_input = int(input())
    print()

    average_comp_sql = '''
        SELECT u.first_name, u.last_name, AVG(ar.score), c.name
        FROM AssessmentResults ar
        JOIN Assessments a
        ON a.assessment_id = ar.assessment_id
        JOIN Competency c
        ON c.comp_id = a.comp_id
        JOIN Users u
        ON u.user_id = ar.user_id
        WHERE c.comp_id = ? AND ar.user_id = ?;
    '''

    rows = cursor.execute(average_comp_sql, (comp_id_input, user_id_input)).fetchone()

    if not rows:
        print("\nNo Results\n")
    else:
        print(f'\n{"First":<8} {"Last":<10} {"Score Average":<16} {"Competency"}')
        print(f'{"-"*47}')
        print(f'{rows[0]:<8} {rows[1]:<10} {rows[2]:^16} {rows[3]}\n')


def edit_competency(cursor):
    print("\n-*- Edit Competency -*-")
    view_competency_table(cursor)
    print("\nPlease choose a competency ID to edit")

    edit_comp_input = int(input())
    print()
    print("Enter the new name for the competency\n")
    edit_comp_name = input("Competency Name: ")
    print()

    edit_comp_sql = '''
        UPDATE Competency
        SET name = ?
        WHERE comp_id = ?;
    '''

    cursor.execute(edit_comp_sql, (edit_comp_name, edit_comp_input))
    connection.commit()

    print(f'Competency Edit Complete\n')


# ASSESSMENT VIEWS
def view_assessments_table(cursor):
    assessment_sql = '''
        SELECT assessment_id, comp_id, name, date_created
        FROM Assessments
        WHERE active = 1;
    '''

    rows = cursor.execute(assessment_sql).fetchall()

    if not rows:
        print("\nNo Assessments\n")
        return

    print(f'\n{"ID":<5} {"Name":<50} {"Date Created":<22} {"Competency ID"}')
    print(f"{'-'*93}")
    for row in rows:
        print(f'{row[0]:>2}. {row[2]:<50} {row[3]:<22} {row[1]:^15}')


def view_specific_assessments(cursor):
    print("-*- View User Assessments -*-")
    view_users_and_types(cursor)
    print("\nPlease choose the ID of the user you would like to view")
    view_assessment_input = int(input())
    print()

    view_user_a_sql = '''
        SELECT a.name, ar.score
        FROM AssessmentResults ar
        JOIN Assessments a
        ON a.assessment_id = ar.assessment_id
        WHERE ar.user_id = ?
        ORDER BY ar.score;
    '''

    rows = cursor.execute(view_user_a_sql, (view_assessment_input,)).fetchall()

    if not rows:
        print("\nNo Results\n")
    else:
        view_user_name(view_assessment_input, cursor)
        print(f'\n{"Assessment":<35} {"Score"}')
        print(f'{"-"*41}')
        for row in rows:
            print(f'{row[0]:<35} {row[1]:^5}')


def edit_assessment(cursor):
    print("\n-*- Edit Assessments -*-\n")
    view_assessments_table(cursor)
    print("\nPlease select the ID of the assessment to edit")

    assessment_input = int(input())

    print("Enter the new name for the assessment\n")
    edit_comp_name = input("Assessment Name: ")
    print()

    assessment_edit_sql = '''
        UPDATE Assessments
        SET name = ?
        WHERE assessment_id = ?;
    '''

    cursor.execute(assessment_edit_sql, (edit_comp_name, assessment_input))
    connection.commit()

    print("Assessment Edit Complete\n")


def view_single_assessment(a_id, cursor):
    assessment_sql = '''
        SELECT a.name, ar.score
        FROM Assessments a
        JOIN AssessmentResults ar
        ON ar.assessment_id = a.assessment_id
        WHERE a.assessment_id = ?;
    '''

    row = cursor.execute(assessment_sql, (a_id, )).fetchone()

    print(f'{row[0]}\n')


def exporting_assessments(cursor):
    assessment_sql = '''
        SELECT assessment_id, comp_id, name, date_created
        FROM Assessments
        WHERE active = 1;
    '''

    rows = cursor.execute(assessment_sql).fetchall()

    if not rows:
        print("\nNo Assessments\n")
        return

    return rows

# ASSESSMENT RESULTS VIEWS
def view_assessments_results_table(cursor):
    ar_sql = '''
        SELECT user_id, assessment_id, score, date_taken, manager
        FROM AssessmentResults
        WHERE active = 1
        ORDER BY date_taken;
    '''

    rows = cursor.execute(ar_sql).fetchall()

    if not rows:
        print("\nNo Assessment Results\n")
        return

    print(f'\n{"U ID":<5} {"Score":<10} {"Date Created":<22} {"A ID":<10} {"Manager"}')
    print(f"{'-'*58}")
    for row in rows:
        print(f'{row[0]:>2}. {row[2]:^10} {row[3]:<22} {row[1]:^9}       {row[4]}')


def edit_assessment_results(cursor):
    print("\n-*- Edit Assessment Results -*-")
    view_assessments_results_table(cursor)
    print("\nPlease select the ID of the user first")
    user_id_input = int(input())

    print("Please select the ID of the assessment now")
    assessment_id_input = int(input())

    view_user_name(user_id_input, cursor)
    view_single_assessment(assessment_id_input, cursor)

    print("Now that we have our User selected, enter your update information\n")
    new_score = int(input("(0 - 4)\n"))
    new_date = get_date()

    edit_ar_sql = '''
        UPDATE AssessmentResults
        SET score = ?, date_taken = ?
        WHERE user_id = ? AND assessment_id = ?;
    '''

    cursor.execute(edit_ar_sql, (new_score, new_date, user_id_input, assessment_id_input))
    connection.commit()

    print("\nEdit Assessment Results Complete\n")


def exporting_ar(cursor):
    ar_sql = '''
        SELECT user_id, assessment_id, score, date_taken, manager
        FROM AssessmentResults
        WHERE active = 1
        ORDER BY date_taken;
    '''

    rows = cursor.execute(ar_sql).fetchall()

    if not rows:
        print("\nNo Assessment Results\n")
        return

    return rows


def view_table_data(table_type, cursor):
    if table_type == 'Users':
        view_users_table(cursor)
    elif table_type == 'Competency':
        view_competency_table(cursor)
    elif table_type == 'Assessments':
        view_assessments_table(cursor)
    elif table_type == 'AssessmentResults':
        view_assessments_results_table(cursor)


def continue_func():
  print()
  print("Press <enter> to continue")
  print("-"*25)
  input()


def get_date():
    new_date = datetime.now()
    date_time_str = new_date.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_str


def data_initialization():
    print("Hello, and Welcome\n")
    print("Would you like to initilize the database?")
    print("\n(Y)es\n(N)o")
    user_input = input()

    if user_input == 'n':
        pass
    else:
        print("\nInitilization In Progress...")
        time.sleep(1.5)
        print("Database Created...")
        time.sleep(1)
        print("Inserting Competencies...")
        time.sleep(1.5)
        print("Competencies Added...")
        time.sleep(1)
        print("Inserting Assessments...")
        time.sleep(1.5)
        print("Assessments Added...\n")
        time.sleep(1)


def deactivate_entry(table, d_id, cursor):
    if table == 'Users':
        deactivate_sql = '''
            UPDATE Users
            SET active = 0
            WHERE user_id = ?;
        '''

        cursor.execute(deactivate_sql, (d_id,))
        connection.commit()

    elif table == 'Competency':
        deactivate_sql = '''
            UPDATE Competency
            SET active = 0
            WHERE comp_id = ?;
        '''

        cursor.execute(deactivate_sql, (d_id,))
        connection.commit()

    elif table == 'Assessments':
        deactivate_sql = '''
            UPDATE Assessments
            SET active = 0
            WHERE assessment_id = ?;
        '''

        cursor.execute(deactivate_sql, (d_id,))
        connection.commit()

    elif table == 'AssessmentResults':
        deactivate_sql = '''
            UPDATE AssessmentResults
            SET active = 0
            WHERE user_id = ?;
        '''

        cursor.execute(deactivate_sql, (d_id,))
        connection.commit()


def reactivate_entry(table, r_id, cursor):
    if table.title() == 'Users':
        reactivate_sql = '''
            UPDATE Users
            SET active = 1
            WHERE user_id = ?;
        '''

        cursor.execute(reactivate_sql, (r_id,))
        connection.commit()

    elif table.title() == 'Competency':
        reactivate_sql = '''
            UPDATE Competency
            SET active = 1
            WHERE comp_id = ?;
        '''

        cursor.execute(reactivate_sql, (r_id,))
        connection.commit()

    elif table.title() == 'Assessments':
        reactivate_sql = '''
            UPDATE Assessments
            SET active = 1
            WHERE assessment_id = ?;
        '''

        cursor.execute(reactivate_sql, (r_id,))
        connection.commit()

    elif table.title() == 'AssessmentResults':
        reactivate_sql = '''
            UPDATE AssessmentResults
            SET active = 1
            WHERE user_id = ?;
        '''

        cursor.execute(reactivate_sql, (r_id,))
        connection.commit()


def manager_create(cursor):
    date = get_date()
    count_users = '''
        SELECT count(user_id) FROM Users;
    '''

    count = cursor.execute(count_users)

    for row in count:
        if row[0] == 0:
            data_initialization()
            continue_func()
            new_manager = Users()
            print("You are the first manager we have! Please create an account\n")
            first_name = input("First Name: ").title()
            last_name = input("Last Name: ").title()
            phone = input("Phone: ")
            email = input("Email: ")
            password = input("Password: ")

            new_manager.set_all(first_name, last_name, phone, email, password, date, "Manager", date)
            new_manager.save_user(cursor)
            print()
            new_manager.print_me()

            print("\nNow that your set up, let's log in")
            print("Please enter your Email and Password\n")

            manager_or_user(cursor)
        else:
            manager_or_user(cursor)


def login_user_exist(cursor):
    existing_user_login = Users()

    while True:
        user_login_email = login_email()
        user_login_password = login_password()

        existing_user_login.load(user_login_email, cursor)
        check_credentials = existing_user_login.check_password(user_login_email, user_login_password, cursor)
        
        if check_credentials == True:
            time.sleep(2)
            print(f"\nWelcome {existing_user_login.first_name} {existing_user_login.last_name}\n")
            return existing_user_login.email
        else:
            print("Unsuccessful Login, please try again")


def user_type_check(user_e, cursor):
    logged_in_user_type = Users()
    logged_in_user_type.load(user_e, cursor)
    type_of_user = logged_in_user_type.get_user_type(cursor)

    return type_of_user


def create_user(cursor):
    print("\n-*- Create New User -*-\n")
    print("Please fill out the following fields")

    new_user = Users()

    first = input("First Name: ").title()
    last = input("Last Name: ").title()
    phone_num = input("Phone: ")
    valid_email = input("Email: ")
    valid_password = input("Password: ")

    print("\nIs this going to be a New User or Manager?\n")
    print("(M)anager\n(U)ser")
    new_user_type = input().lower()

    if new_user_type == 'm':
        new_hire_date = get_date()
        new_created_date = get_date()
        new_user.set_all(first, last, phone_num, valid_email, valid_password, new_created_date, 'Manager', new_hire_date)
        new_user.save_user(cursor)
    elif new_user_type == 'u':
        new_created_date = get_date()
        new_user.set_all(first, last, phone_num, valid_email, valid_password, new_created_date)
        new_user.save_user(cursor)


def manager_menu(cursor):
    date = get_date()
    print("Here is a list of sections you have access to")
    print('''
        (A)dd
        (E)dit
        (V)iew
        (I)mport CSV
        (Ex)port CSV
        (D)eactivate
        (R)eactivate
        (L)ogout
        (Q)uit
    ''')

    manager_menu = input().lower()

    if manager_menu == 'q':
        print("Exiting Program...")
        time.sleep(1)
        print("Goodbye")
        quit()

    elif manager_menu == 'a':
        print("Please select from the following options")
        print("")
        print('''
    -*- Add Options -*-

        (A)ssessment
        (C)ompetency
        (N)ew Assessment Result
        (U)ser
        ''')
        add_input = input().lower()

        if add_input == 'a':
            new_assessment = Assessments()
            print("\nTo add a new Assessment to a competency")
            print("you will need to choose which competency this relates to\n")
            print("Please choose the ID that matches the competency of the assessment\n")
            view_table_data('Competency', cursor)
            
            competency_id = int(input())
            assessment_name = input('Name of Assessment: ').title()

            new_assessment.set_all(competency_id, assessment_name, date)
            new_assessment.save_assessment(cursor)

            print("Adding Assessment...")
            time.sleep(1)
            print("Process complete")

        elif add_input == 'c':
            new_comp = Compentency()
            print("\n-*- Add Competency -*-")
            print("\nPlease enter the name of the new competency\n")

            comp_name = input("Competency Name: ")

            new_comp.set_all(comp_name, date)
            new_comp.save_comp(cursor)

            print("Adding Competency...")
            time.sleep(1)
            print("Process complete")

        elif add_input == 'n':
            new_assessment_result = AssessmentResults()
            print("\nTo add a new assessment result, we will need")
            print("the user ID along with the assessment ID.")
            print("Please follow the prompts and instructions moving forward\n")
            print("-*- Users List -*-")
            view_users_and_types(cursor)
            print("\nChoose ID of user who is awaiting the assessment results")
            user_id_input = int(input("User ID: "))

            print("\n-*- Assessments List -*-")
            view_assessments_table(cursor)
            print("\nChoose ID of the assessment taken")
            assessment_id_input = int(input("Assessment ID: "))

            print("\nWhat is the score of the given assessment? (0 - 4)")
            score_results = int(input("Score: "))

            print("\nWas there a specific manager who assigned this assessment?")
            had_manager = input("\n(Y)es\n(N)o\n").lower()

            if had_manager == 'y':
                print("\n-*- Managers List -*-")
                view_managers_and_types(cursor)
                print("\nChoose manager ID that assigned the assessment\n")

                manager_input = int(input("Manager ID: "))
                new_assessment_result.set_all(user_id_input, assessment_id_input, score_results, date, manager_input)
                new_assessment_result.save_a_result(cursor)
            else:
                new_assessment_result.set_all(user_id_input, assessment_id_input, score_results, date)
                new_assessment_result.save_a_result(cursor)

            print("Adding Assessment Results...")
            time.sleep(1)
            print("Process complete")

        elif add_input == 'u':
            create_user(cursor)

            print("Adding User...")
            time.sleep(1)
            print("Process complete")
        else:
            print("\nSorry, I could not find that option. Please try again\n")
            manager_menu(cursor)

    elif manager_menu == 'v':
        print("\n-*- View Options -*-")
        print("Please select an option")
        print("\n(A)ll Users\n(R)eport Competencies\n(C)ompetencies by User\n(L)evels of Competency\n(As)sessments for a User\n(S)earch User by Name\n(Q)uit")

        view_input = input().lower()

        if view_input == 'q':
            pass
        elif view_input == 'a':
            view_users_table(cursor)
            continue_func()
        elif view_input == 'r':
            comp_report_all_users(cursor)
            continue_func()
        elif view_input == 'c':
            view_all_comps_by_user(cursor)
            continue_func()
        elif view_input == 'l':
            comp_level_report(cursor)
            continue_func()
        elif view_input == 'as':
            view_specific_assessments(cursor)
            continue_func()
        elif view_input == 's':
            search_users(cursor)
            continue_func()

    elif manager_menu == 'e':
        print("\nPlease select from the following options\n")
        print('''
    -*- Edit Options -*-

        (A)ssessment
        (C)ompetency
        (R) Assessment Result
        (U)ser
        ''')

        edit_input = input().lower()

        if edit_input == 'a':
            edit_assessment(cursor)
            continue_func()
        elif edit_input == 'c':
            edit_competency(cursor)
            continue_func()
        elif edit_input == 'r':
            edit_assessment_results(cursor)
            continue_func()
        elif edit_input == 'u':
            edit_user_information(cursor)
            continue_func()
        else:
            print("Sorry I didn't get that, please try again later")
    elif manager_menu == 'ex':
        export_csv(cursor)
        continue_func()
    elif manager_menu == 'i':
        import_csv()
        continue_func()
    elif manager_menu == 'd':
        print("\n-*- Deactivate -*-")
        print("Enter table you would like to access\n")
        print("(A)ssessments\n(As)sessment Results\n(C)ompetency\n(U)sers\n(Q)uit")
        table_input = input().lower()

        if table_input == 'q':
            pass

        elif table_input == 'a':
            view_assessments_table(cursor)
            print("\nPlease choose the ID of the assessment to deactivate")
            assessment_input = int(input())
            deactivate_entry('Assessments', assessment_input, cursor)

        elif table_input == 'as':
            view_assessments_results_table(cursor)
            print("\nPlease choose the ID of the assessment to deactivate")
            ar_input = int(input())
            deactivate_entry('Assessments', ar_input, cursor)

        elif table_input == 'c':
            view_competency_table(cursor)
            print("\nPlease choose the ID of the assessment to deactivate")
            competency_input = int(input())
            deactivate_entry('Assessments', competency_input, cursor)

        elif table_input == 'u':
            view_assessments_table(cursor)
            print("\nPlease choose the ID of the assessment to deactivate")
            users_input = int(input())
            deactivate_entry('Users', users_input, cursor)

    elif manager_menu == 'r':
        print("\n-*- Reactivate -*-")
        print("Enter table you would like to access\n")
        print("(A)ssessments\n(As)sessment Results\n(C)ompetency\n(U)sers\n(Q)uit")
        table_input = input().lower()

        if table_input == 'q':
            pass
            
        elif table_input == 'a':
            view_assessments_table(cursor)
            print("\nPlease choose the ID of the assessment to reactivate")
            assessment_input = int(input())
            reactivate_entry('Assessments', assessment_input, cursor)

        elif table_input == 'as':
            view_assessments_results_table(cursor)
            print("\nPlease choose the ID of the assessment to reactivate")
            ar_input = int(input())
            reactivate_entry('Assessments', ar_input, cursor)

        elif table_input == 'c':
            view_competency_table(cursor)
            print("\nPlease choose the ID of the assessment to reactivate")
            competency_input = int(input())
            reactivate_entry('Assessments', competency_input, cursor)

        elif table_input == 'u':
            view_assessments_table(cursor)
            print("\nPlease choose the ID of the assessment to reactivate")
            users_input = int(input())
            reactivate_entry('Users', users_input, cursor)

    elif manager_menu == 'l':
        print("Logging out...")
        time.sleep(1.5)
        continue_func()
        time.sleep(1)
        manager_or_user(cursor)
    else:
        print("\nSorry, I could not find that option. Please try again\n")
        manager_menu(cursor)


# manager_menu(cursor)

def user_menu(user_email, cursor):
    logged_in_user = Users()
    logged_in_user.load(user_email, cursor)
    print("\nHere is a list of sections you have access to")
    print('''
        (E)dit
        (V)iew
        (L)ogout
        (Q)uit
    ''')

    user_menu = input().lower()

    if user_menu == 'q':
        print("Exiting Program...")
        time.sleep(1)
        print("Goodbye")
        quit()
    elif user_menu == 'l':
        print("Logging out...")
        time.sleep(1.5)
        continue_func()
        time.sleep(1)
        manager_or_user(cursor)
    elif user_menu == 'e':
        print("\n-*- Edit Options -*-")
        print("\n(N)ame\n(P)assword")
        edit_input = input().lower()

        if edit_input == 'n':
            print("\n-*- Edit Name -*-")
            first_name_input = input("First Name: ").title()
            if first_name_input == '':
                first_name_input = logged_in_user.first_name

            last_name_input = input("Last Name: ").title()
            if last_name_input == '':
                last_name_input = logged_in_user.last_name

            update_user_name_sql = '''
                UPDATE Users
                SET first_name = ?, last_name = ?
                WHERE user_id = ?;
            '''

            cursor.execute(update_user_name_sql, (first_name_input, last_name_input, logged_in_user.user_id))
            connection.commit()
            
        elif edit_input == 'p':
            print("\n-*- Edit Password -*-")
            new_user_password = input("Password: ")
            logged_in_user.change_password(new_user_password)
            cursor.execute("UPDATE Users SET password = ? WHERE email = ?", (logged_in_user.get_password(), logged_in_user.email))
            connection.commit()
        else:
            print("Invalid Option, please try again later")
    elif user_menu == 'v':
        view_competency_of_user(logged_in_user.user_id, cursor)


def login_email():
    user_email = input("   Enter Email: ")
    return user_email


def login_password():
    user_password = input("Enter Password: ")
    return user_password


def import_csv():
    print("\n-*- Import Data -*-")
    print("Which table would you like to import?")
    print("\n(C)ompetencies\n(A)ssessments\n(As)sessment Results\n(U)sers")
    export_input = input().lower()
    print()

    if export_input == 'c':
        comp_exists = exists('csv_files/competencies.csv')

        if comp_exists:
            with open("csv_files/competencies.csv", 'r', newline='') as comp_file:
                results = []

                for line in comp_file:
                    words = line.split(',')
                    results.append((words[0], words[1:]))

            for result in results:
                strip_newline = result[1][-1].strip('\n')
                print(f'{result[0]:>2}. {result[1][0]:<30} {strip_newline}')
            print()

    elif export_input == 'a':
        assessment_exists = exists('csv_files/assessments.csv')

        if assessment_exists:
            with open("csv_files/assessments.csv", 'r', newline='') as assessment_file:
                results = []

                for line in assessment_file:
                    words = line.split(',')
                    results.append((words[0], words[1:]))

            for result in results:
                strip_newline = result[1][-1].strip('\n')
                print(f'{result[0]:>2}. {result[1][1]:<50} {strip_newline}')
            print()

    elif export_input == 'as':
        ar_exists = exists('csv_files/assessment_results.csv')

        if ar_exists:
            with open("csv_files/assessment_results.csv", 'r', newline='') as ar_file:
                results = []

                for line in ar_file:
                    words = line.split(',')
                    results.append((words[0], words[1:]))

            for result in results:
                strip_newline = result[1][-1].strip('\n')
                print(f'{result[0]:^10} {result[1][0]:^15} {result[1][1]:^10} {result[1][2]:<22} {strip_newline}')
            print()

    elif export_input == 'u':
        user_exists = exists('csv_files/users.csv')

        if user_exists:
            with open("csv_files/users.csv", 'r', newline='') as user_file:
                results = []

                for line in user_file:
                    words = line.split(',')
                    results.append((words[0], words[1:]))

            for result in results:
                strip_newline = result[1][-1].strip('\n')
                print(f'{result[0]:>2}. {result[1][0]:<10} {result[1][1]:<10} {result[1][2]:<20} {result[1][3]:<22} {strip_newline}')
            print()

    else:
        print("Invalid Option, please try again later")


def export_csv(cursor):
    print("\n-*- Export Data -*-\n")
    print("Which table would you like to export?")
    print("\n(C)ompetencies\n(A)ssessments\n(As)sessment Results\n(U)sers")
    export_input = input().lower()

    if export_input == 'c':
        comp_list = exporting_competency(cursor)
        comp_headers = ["ID", "Name", "Date Created"]

        with open("csv_files/competencies.csv", 'w') as comp_file:
            wrt = csv.writer(comp_file)
            wrt.writerow(comp_headers)
            wrt.writerows(comp_list)

    elif export_input == 'a':
        assessment_list = exporting_assessments(cursor)
        assessment_headers = ["ID", "Competency ID", "Name", "Date Created"]

        with open("csv_files/assessments.csv", 'w') as assessment_file:
            wrt = csv.writer(assessment_file)
            wrt.writerow(assessment_headers)
            wrt.writerows(assessment_list)

    elif export_input == 'as':
        ar_list = exporting_ar(cursor)
        ar_headers = ["User ID", "Assessment ID", "Score", "Date Taken", "Manager"]

        with open("csv_files/assessment_results.csv", 'w') as ar_file:
            wrt = csv.writer(ar_file)
            wrt.writerow(ar_headers)
            wrt.writerows(ar_list)

    elif export_input == 'u':
        user_list = exporting_users(cursor)
        user_headers = ["ID", "First", "Last", "Email", "Date Created", "User Type"]

        with open("csv_files/users.csv", 'w') as user_file:
            wrt = csv.writer(user_file)
            wrt.writerow(user_headers)
            wrt.writerows(user_list)
    else:
        print("Invalid Option, please try again later")


def manager_or_user(cursor):
    print("\nLogin\n")
    user_type_email = login_user_exist(cursor)
    type_check = user_type_check(user_type_email, cursor)

    while True:
        if type_check.lower() == 'manager':
            manager_menu(cursor)

        elif type_check.lower() == 'user':
            user_menu(user_type_email, cursor)

main(cursor)