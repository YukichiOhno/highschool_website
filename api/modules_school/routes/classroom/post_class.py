import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# add a class to the class table
def post_class(connection):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_class error. check terminal"
    terminal_error_statement = "post_class error:"
    
    print("\nprocessing post_class...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("class", "CLASS_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("class")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("CLASS_CAPACITY", request_data, user_attributes_names, user_attributes_values, vartype=int, max=200)
        validate_attribute("CLASS_ROOM", request_data, user_attributes_names, user_attributes_values, vartype=int, max=3)
        validate_attribute("CLASS_BLDG_ROOM", request_data, user_attributes_names, user_attributes_values, vartype=int, max=1)
        validate_attribute("EMP_ID", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="employee", foreign_key_name="EMP_ID")
        validate_attribute("COURSE_ID", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="course", foreign_key_name="COURSE_ID")
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("class", user_attributes_names, user_attributes_values)
    print(f"{query}")
    
    try:
        execute_query(connection, query)
    except Exception as e:
        return f"value occured during executing the query: {e}"
    
    print("post class success")
    return "post class success"