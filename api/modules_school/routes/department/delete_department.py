import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# delete an existing department table row
def delete_department(connection, dept_code):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_department error. check terminal"
    terminal_error_statement = "delete_department error:"

    print("\nprocessing delete_department...")
    sql = "SELECT * FROM DEPARTMENT;"
    department_table = execute_read_query(connection, sql)  

    for i in range(len(department_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = department_table[i]["DEPT_CODE"]
        if dept_code == id_to_delete:
            delete_query = f"DELETE FROM DEPARTMENT WHERE DEPT_CODE = {dept_code}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM DEPARTMENT WHERE DEPT_CODE = {dept_code}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete department: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete department success")
            return "delete department success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement