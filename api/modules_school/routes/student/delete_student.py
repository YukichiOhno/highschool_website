import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# delete an existing student table row
def delete_student(connection, stud_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_student error. check terminal"
    terminal_error_statement = "delete_student error:"

    print("\nprocessing delete_student...")
    sql = "SELECT * FROM STUDENT;"
    student_table = execute_read_query(connection, sql)

    for i in range(len(student_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = student_table[i]["STUD_ID"]
        if stud_id == id_to_delete:
            delete_query = f"DELETE FROM STUDENT WHERE STUD_ID = {stud_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM STUDENT WHERE STUD_ID = {stud_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete student: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete student success")
            return "delete student success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement
