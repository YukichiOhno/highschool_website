import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table
from modules_school.value_converter import convert_values

# retrieve invoice table information
def get_invoice(connection):
    query = "SELECT * FROM INVOICE"
    invoice_table = execute_read_query(connection, query)
    convert_values(invoice_table)
    # return jsonify(invoice_table)

    for invoice in invoice_table:
        inv_id = invoice["INV_ID"]
        sql = f"SELECT S.SUPP_ID, SUPP_NAME, IT.INVT_CODE, INVT_NAME, QTY, UNIT_PRICE\n" \
              f"FROM INVOICE IV\n" \
              f"JOIN INVOICE_LINE IL ON IV.INV_ID = IL.INV_ID\n" \
              f"JOIN DEPARTMENT D ON IV.DEPT_CODE = D.DEPT_CODE\n" \
              f"JOIN SUPPLIER S ON IV.SUPP_ID = S.SUPP_ID\n" \
              f"JOIN INVENTORY IT ON IT.INVT_CODE = IL.INVT_CODE\n" \
              f"WHERE IV.INV_ID = {inv_id};"
        
        items = execute_read_query(connection, sql)
        convert_values(items)
        items = items
        invoice["ITEMS"] = items

    return jsonify(invoice_table)