import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# delete an existing item entity
def delete_item(connection, item_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_item error. check terminal"
    terminal_error_statement = "delete_item error:"

    print("\nprocessing delete_item...")
    sql = "SELECT * FROM ITEM;"
    item_table = execute_read_query(connection, sql)

    for i in range(len(item_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = item_table[i]["ITEM_ID"]
        if item_id == id_to_delete:
            delete_query = f"DELETE FROM ITEM WHERE ITEM_ID = {item_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM ITEM WHERE ITEM_ID = {item_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete item: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete item success")
            return "delete item success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement