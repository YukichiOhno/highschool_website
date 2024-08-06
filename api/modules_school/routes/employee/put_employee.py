import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# update an existing employee table row
def put_employee(connection, emp_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_employee error. check terminal"
    terminal_error_statement = "put_employee error:"

    print("\nprocessing put_employee...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("employee", "EMP_ID", user_data, terminal_error_statement, update_entity=True, pk_value=emp_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("employee")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("EMP_FNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("EMP_LNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("EMP_INITIAL", request_data, user_attributes_names, user_attributes_values, isinitial=True, max=1)
        validate_attribute("EMP_DOB", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("EMP_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("EMP_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("EMP_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("EMP_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("EMP_EMPLOY_DATE", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("POS_CODE", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="job_position", foreign_key_name="POS_CODE")
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("employee", user_attributes_names, user_attributes_values, "EMP_ID", emp_id)
    print(f"{query}")
    
    try:
        execute_query(connection, query)
    except Exception as e:
        return f"value occured during executing the query: {e}"
    
    print("put employee success")
    return "put employee success"