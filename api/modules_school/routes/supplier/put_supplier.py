import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# update an existing supplier table row
def put_supplier(connection, supp_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_supplier error. check terminal"
    terminal_error_statement = "put_supplier error:"

    print("\nprocessing put_supplier...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("supplier", "SUPP_ID", user_data, terminal_error_statement, update_entity=True, pk_value=supp_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("supplier")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("SUPP_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("SUPP_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("SUPP_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("supp_type"))
        validate_attribute("SUPP_CONT_START", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("SUPP_CONT_END", request_data, user_attributes_names, user_attributes_values, isdate=True)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("supplier", user_attributes_names, user_attributes_values, "SUPP_ID", supp_id)
    print(f"{query}")
    execute_query(connection, query)
    print("put supplier success")
    return "put supplier success"