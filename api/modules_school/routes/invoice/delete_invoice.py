import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table

# can only delete pending invoices; completed ones cannot
# delete an existing invoice entity
def delete_invoice(connection, inv_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_invoice error. check terminal"
    terminal_error_statement = "delete_invoice error:"

    print("\nprocessing delete_invoice...")
    sql = "SELECT * FROM INVOICE;"
    invoice_table = execute_read_query(connection, sql)

    for i in range(len(invoice_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = invoice_table[i]["INV_ID"]
        if inv_id == id_to_delete:
            # disallows the deletion of data if inv_pay_status is completed
            sql = f"SELECT INV_PAY_STATUS FROM INVOICE WHERE INV_ID = {inv_id}"
            inv_pay_status = execute_read_query(connection, sql)[0]["INV_PAY_STATUS"]
            if inv_pay_status == "completed":
                print(f"{terminal_error_statement}: cannot delete an already paid invoice")
                
            else:
                delete_query = f"DELETE FROM INVOICE WHERE INV_ID = {inv_id}"
                execute_query(connection, delete_query)
                check_sql = f"SELECT * FROM INVOICE WHERE INV_ID = {inv_id}"
                check = execute_read_query(connection, check_sql)
                print(check)
                if check:
                    print(f"{terminal_error_statement} cannot delete invoice: referenced by other entities in other table")
                    return failed_data_entry_statement
                print("delete invoice success")
                return "delete invoice success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement