import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# add a relationship between a student and a guide
def post_student_guide(connection):
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_student_guide error. check terminal"
    terminal_error_statement = "post_student_guide error:"

    print("\nprocessing post_student_guide...")
    stud_id = request.args.get("STUD_ID", type=int)
    guid_id = request.args.get("GUID_ID", type=int)

    check_stud_id = validate_associative_table("student", "STUD_ID", stud_id, terminal_error_statement)
    check_guid_id = validate_associative_table("guide", "GUID_ID", guid_id, terminal_error_statement)
    print(f"student: {check_stud_id}; guide: {check_guid_id}")
    if (check_stud_id != "pk found") or (check_guid_id != "pk found"):
        return failed_data_entry_statement

    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    # student validation
    verify_user_data = verify_initial_data("student", "STUD_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # guide validation
    verify_user_data = verify_initial_data("guide", "GUID_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("student_guide")

    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement

    # validate and manipulate entered user attributes
    try:
        user_attributes_names = ["STUD_ID", "GUID_ID"]
        user_attributes_values = [stud_id, guid_id]
        validate_attribute("GUID_IDENTITY", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("guid_identity"))
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module for either PUT or POST methods
    if request.method == "POST":
        query = insert_query("student_guide", user_attributes_names, user_attributes_values)
        print(f"{query}")

        try:
            execute_query(connection, query)
        except Exception as e:
            return f"value occured during executing the query: {e}"
        
        print("post student_guide success")
        return "post student_guide success"
    else:
        query = update_query("student_guide", user_attributes_names, user_attributes_values, "STUD_ID", stud_id, iscomposite=True, pk_name_2="GUID_ID", entity_id_2=guid_id)
        print(f"{query}")

        try:
            execute_query(connection, query)
        except Exception as e:
            return f"value occured during executing the query: {e}"

        print("put student_guide success")
        return "put student_guide success"