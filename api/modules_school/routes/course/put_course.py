import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# update an existing course table row
def put_course(connection, course_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_course error. check terminal"
    terminal_error_statement = "put_course error:"

    print("\nprocessing put_course...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("course", "COURSE_ID", user_data, terminal_error_statement, update_entity=True, pk_value=course_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("course")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("COURSE_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("COURSE_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("COURSE_HRS", request_data, user_attributes_names, user_attributes_values, vartype=int, max=1)
        validate_attribute("COURSE_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("course_type"))
        validate_attribute("COURSE_GRADE_LVL", request_data, user_attributes_names, user_attributes_values, min=9, max=12, vartype=int, hasminmax=True)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("course", user_attributes_names, user_attributes_values, "COURSE_ID", course_id)
    print(f"{query}")
    
    try:
        execute_query(connection, query)
    except Exception as e:
        return f"value occured during executing the query: {e}"
    
    print("put course success")
    return "put course success"


