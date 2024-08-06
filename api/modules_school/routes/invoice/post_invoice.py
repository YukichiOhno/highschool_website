import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# add an invoice row to the invoice table 
def post_invoice(connection):
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_invoice error. check terminal"
    terminal_error_statement = "post_invoice error:"

    print("\nprocessing post_invoice...")
    # validate and manipulate entered user attributes
    try:
        invoice_attributes_names = ["INV_PAY_STATUS"]
        invoice_attributes_values = ["pending"]

        validate_attribute("INV_ISSUE_DATE", request_data, invoice_attributes_names, invoice_attributes_values, isdate=True)
        validate_attribute("INV_DUE_DATE", request_data, invoice_attributes_names, invoice_attributes_values, isdate=True)
        validate_attribute("DEPT_CODE", request_data, invoice_attributes_names, invoice_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="department", foreign_key_name="DEPT_CODE")
        validate_attribute("SUPP_ID", request_data, invoice_attributes_names, invoice_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="supplier", foreign_key_name="SUPP_ID")

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # always have NUM_OF_ITEMS in the body
    try:
        num_of_items = int(request_data["NUM_OF_ITEMS"])
    except Exception:
        print(f"{terminal_error_statement} must have NUM_OF_ITEMS")
        return failed_data_entry_statement

    invoice_line_attributes_names = []
    invoice_line_attributes_values = []
    invoice_line_attributes = []
        
    print("\nprocessing post_invoice: invoice_line entries") 
    for row in range(1, num_of_items + 1):
        try:
            name_1, value_1 = validate_attribute(f"QTY_{row}", request_data, invoice_line_attributes_names, invoice_line_attributes_values, vartype=int, max=9999)
            name_1 = "QTY"

            name_2, value_2 = validate_attribute(f"UNIT_PRICE_{row}", request_data, invoice_line_attributes_names, invoice_line_attributes_values, vartype=float, max=9999.99)
            name_2 = "UNIT_PRICE"

            # INVOICE_LINE foreign key
            name_3, value_3 = validate_attribute(f"ITEM_{row}", request_data, invoice_line_attributes_names, invoice_line_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="inventory", foreign_key_name="INVT_CODE")
            name_3 = "INVT_CODE"

            invoice_line_attributes.append({name_1: value_1, name_2: value_2, name_3: value_3})
            print(invoice_line_attributes)
        except ValueError as e:
            print(f"{terminal_error_statement} {e}")
            return failed_data_entry_statement
        
    if not invoice_attributes_names:
        print(f"{terminal_error_statement} No valid invoice attributes found. ")
        return failed_data_entry_statement
    
    if not invoice_line_attributes:
        print(f"{terminal_error_statement} No valid invoice line attributes found. ")
        return failed_data_entry_statement
    
    try:
        # Prepare and execute SQL statements separately
        # Insert into INVOICE
        invoice_sql = f"INSERT INTO INVOICE ({', '.join(invoice_attributes_names)}) VALUES ("
        invoice_sql += ", ".join([f"'{value}'" if not isinstance(value, (int, float)) else str(value) for value in invoice_attributes_values])
        invoice_sql += ");"
        
        execute_query(connection, invoice_sql)
        print(f"\n{invoice_sql}")
        print("Invoice inserted successfully.")

        # Get the last inserted ID
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        last_invoice_id = cursor.fetchone()[0]
        cursor.close()

        # Insert into INVOICE_LINE
        invoice_line_sql = "INSERT INTO INVOICE_LINE (INVT_CODE, INV_ID, QTY, UNIT_PRICE) VALUES "
        invoice_line_values = []
        total_amount = 0.0

        for item in invoice_line_attributes:
            invoice_line_values.append(f"({item['INVT_CODE']}, {last_invoice_id}, {item['QTY']}, {item['UNIT_PRICE']})")
            total_amount += item['QTY'] * item['UNIT_PRICE']

        invoice_line_sql += ", ".join(invoice_line_values) + ";"

        execute_query(connection, invoice_line_sql)
        print(f"\n{invoice_line_sql}")
        print("Invoice lines inserted successfully.")

        # Update INVOICE with total amount
        update_invoice_sql = f"UPDATE INVOICE SET INV_TOTAL_AMT = {total_amount} WHERE INV_ID = {last_invoice_id};"
        execute_query(connection, update_invoice_sql)
        print(f"\n{update_invoice_sql}")
        print("Invoice total amount updated successfully.")

    except Exception as e:
        print(f"{terminal_error_statement} value occurred during executing the query: {e}")
        return failed_data_entry_statement

    print("post_invoice success")
    return "post_invoice success"