import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table
from modules_school.value_converter import convert_values


# pay a pending invoice
def pay_invoice(connection, inv_id):
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "pay_invoice error. check terminal"
    terminal_error_statement = "pay_invoice error:"

    print("\nprocessing pay_invoice...")
    # allow INV_PAY_STATUS and BUD_ID only
    if ("INV_PAY_STATUS" not in user_data) or ("BUD_ID" not in user_data):
        print(f"{terminal_error_statement} must only INV_PAY_STATUS and BUD_ID eligible for the process to continue")
        return failed_data_entry_statement
    
    try:
        user_attributes_names = []
        user_attributes_values = []

        pay_name, pay_status = validate_attribute("INV_PAY_STATUS", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("inv_pay_status"))
        budget_name, budget_id = validate_attribute("BUD_ID", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="budget", foreign_key_name="BUD_ID")
    except Exception as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # find the selected invoice
    sql = f"SELECT * FROM INVOICE WHERE INV_ID = {inv_id}"
    invoice_entity = execute_read_query(connection, sql)
    convert_values(invoice_entity)

    invoice_total_amt = invoice_entity[0]["INV_TOTAL_AMT"]
    invoice_department = invoice_entity[0]["DEPT_CODE"]
    print(invoice_entity)
    print(invoice_total_amt)

    # find budgets tied to the department this invoice is from
    sql = f"SELECT * FROM BUDGET WHERE DEPT_CODE = {invoice_department} AND BUD_ID = {budget_id}"
    check_budget_eligibility = execute_read_query(connection, sql)
    convert_values(check_budget_eligibility)
    print(check_budget_eligibility)
    if not(check_budget_eligibility):
        print(f"{terminal_error_statement} this department must have an eligible budget")
        return failed_data_entry_statement
    
    # store to a variable the remaining_budget in this entity instance
    remaining_budget = check_budget_eligibility[0]["BUD_REMAIN"]
    print(remaining_budget)

    try:
        new_remaining_budget = remaining_budget - invoice_total_amt

        sql = f"SELECT * FROM INVOICE_LINE WHERE INV_ID = {inv_id}"
        invoice_line_table = execute_read_query(connection, sql)
        convert_values(invoice_line_table)
        print("\ninvoice line table")
        print(invoice_line_table)

        print("\nprocessing invoice line table")
        for entity_row in invoice_line_table:
            inner_sql = f"SELECT * FROM INVENTORY WHERE INVT_CODE = {entity_row["INVT_CODE"]}"
            inventory_table = execute_read_query(connection, inner_sql)
            print(inventory_table)

            item_qty = inventory_table[0]["INVT_QTY"]
            print(f"item qty: {item_qty}")

            invoice_qty = entity_row["QTY"]
            print(f"invoice qty: {invoice_qty}")

            new_qty = invoice_qty + item_qty
            sql = f"UPDATE INVENTORY SET INVT_QTY = {new_qty} WHERE INVT_CODE = {inventory_table[0]["INVT_CODE"]}"
            print(sql)
            execute_query(connection, sql)

        print(f"\nprocessing budget table")
        sql = f"UPDATE BUDGET SET BUD_REMAIN = {new_remaining_budget} WHERE BUD_ID = {budget_id}"
        print(sql)
        execute_query(connection, sql)

        print(f"\nprocessing invoice table")
        sql = f"UPDATE INVOICE SET INV_PAY_STATUS = 'completed' WHERE INV_ID = {inv_id}"
        print(sql)
        execute_query(connection, sql)
    except Exception as e:
        print(f"{terminal_error_statement} value occurred during executing the query: {e}")
        return failed_data_entry_statement
    

    print("success")
    return "success"
