import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# add an entry to the inventory table
def post_inventory(connection):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_inventory error. check terminal"
    terminal_error_statement = "post_inventory error:"
    
    print("\nprocessing post_inventory...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("inventory", "INVT_CODE", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("inventory")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("INVT_NAME", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("INVT_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("INVT_CATEGORY", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("invt_category"))
        validate_attribute("INVT_QTY", request_data, user_attributes_names, user_attributes_values, vartype=int, max=9999)
        validate_attribute("INVT_EXP_DATE", request_data, user_attributes_names, user_attributes_values, isdate=True)
       
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("inventory", user_attributes_names, user_attributes_values)
    print(f"{query}")
    
    try:
        execute_query(connection, query)
    except Exception as e:
        return f"value occured during executing the query: {e}"
        
    print("post inventory success")
    return "post inventory success"