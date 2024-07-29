import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# update an existing student table row
def put_student(connection, stud_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_student error. check terminal"
    terminal_error_statement = "put_student error:"

    print("\nprocessing put_student...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("student", "STUD_ID", user_data, terminal_error_statement, update_entity=True, pk_value=stud_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for student table
    required_attributes, allowed_attributes = entity_attributes_provider("student")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered student attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("STUD_FNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("STUD_LNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("STUD_INITIAL", request_data, user_attributes_names, user_attributes_values, isinitial=True, max=1)
        validate_attribute("STUD_DOB", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("STUD_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("STUD_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("STUD_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("STUD_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("STUD_ENROLL_DATE", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("STUD_GRADE_LVL", request_data, user_attributes_names, user_attributes_values, min=9, max=12, vartype=int, hasminmax=True)
        validate_attribute("STUD_GPA", request_data, user_attributes_names, user_attributes_values, min=0, max=4, vartype=float, hasminmax=True)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("student", user_attributes_names, user_attributes_values, "STUD_ID", stud_id)
    print(f"{query}")
    execute_query(connection, query)
    print("put student success")
    return "put student success"