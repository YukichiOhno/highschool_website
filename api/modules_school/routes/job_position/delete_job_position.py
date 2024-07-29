import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# delete an existing job_position table row
def delete_job_position(connection, pos_code):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_job_position error. check terminal"
    terminal_error_statement = "delete_job_position error:"

    print("\nprocessing delete_job_position...")
    sql = "SELECT * FROM JOB_POSITION;"
    job_position_table = execute_read_query(connection, sql)  

    for i in range(len(job_position_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = job_position_table[i]["POS_CODE"]
        if pos_code == id_to_delete:
            delete_query = f"DELETE FROM JOB_POSITION WHERE POS_CODE = {pos_code}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM JOB_POSITION WHERE POS_CODE = {pos_code}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete job_position: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete job_position success")
            return "delete job_position success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement