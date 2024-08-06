import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# add a relationship between a student and a class
def post_enrollment(connection):
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_enrollment error. check terminal"
    terminal_error_statement = "post_enrollment error:"

    print("\nprocessing post_enrollment...")
    stud_id = request.args.get("STUD_ID", type=int)
    class_id = request.args.get("CLASS_ID", type=int)

    check_stud_id = validate_associative_table("student", "STUD_ID", stud_id, terminal_error_statement)
    check_class_id = validate_associative_table("class", "CLASS_ID", class_id, terminal_error_statement)
    print(f"student: {check_stud_id}; guide: {check_class_id}")
    if (check_stud_id != "pk found") or (check_class_id != "pk found"):
        return failed_data_entry_statement

    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    # student validation
    verify_user_data = verify_initial_data("student", "STUD_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # guide validation
    verify_user_data = verify_initial_data("class", "CLASS_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("enrollment")

    # retrieve attributes provided by the user and perform validation
    if request.method == "POST":
        verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    else:
        verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement

    # validate and manipulate entered user attributes
    try:
        user_attributes_names = ["STUD_ID", "CLASS_ID"]
        user_attributes_values = [stud_id, class_id]
        validate_attribute("ENROLL_STATUS", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("enroll_status"))
        validate_attribute("ENROLL_SCORE", request_data, user_attributes_names, user_attributes_values, vartype=float, max=4)
        validate_attribute("ENROLL_DATE", request_data, user_attributes_names, user_attributes_values, isdate=True)
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module for either PUT or POST methods
    if request.method == "POST":
        sql = f"SELECT COUNT(*) AS 'num_of_students' FROM STUDENT S JOIN ENROLLMENT E ON S.STUD_ID = E.STUD_ID WHERE ENROLL_STATUS = 'enrolled' AND CLASS_ID = {class_id};"
        num_of_students = execute_read_query(connection, sql)[0]["num_of_students"]
        print(f"number of students: {num_of_students}")

        # count the enrollment capacity in the given class
        sql = f"SELECT CLASS_CAPACITY FROM CLASS WHERE CLASS_ID = {class_id};"
        enrollment_capacity = execute_read_query(connection, sql)[0]["CLASS_CAPACITY"]
        print(f"class capacity: {enrollment_capacity}")

        if num_of_students < enrollment_capacity:
            query = insert_query("enrollment", user_attributes_names, user_attributes_values)
            print(f"{query}")
            
            try:
                execute_query(connection, query)
            except Exception as e:
                return f"value occured during executing the query: {e}"
            
            print("post enrollment success")
            return "post enrollment success"
        else:
            print("class capacity reached: cannot add this student to the class or the student may be enrolled in this class already")
            return failed_data_entry_statement
    else:
        if "ENROLL_STATUS" in request_data:
            enroll_status = request_data["ENROLL_STATUS"]
            print(enroll_status)

            if enroll_status == "enrolled":
                print("put enrollment failed: cannot switch student to enrolled")
                return "put enrollment failed"
            else:
                query = update_query("enrollment", user_attributes_names, user_attributes_values, "STUD_ID", stud_id, iscomposite=True, pk_name_2="CLASS_ID", entity_id_2=class_id)
                print(f"{query}")
                
                try:
                    execute_query(connection, query)
                except Exception as e:
                    return f"value occured during executing the query: {e}"
        
                print("put enrollment success")
                return "put enrollment success"
        else:
            query = update_query("enrollment", user_attributes_names, user_attributes_values, "STUD_ID", stud_id, iscomposite=True, pk_name_2="CLASS_ID", entity_id_2=class_id)
            print(f"{query}")

            try:
                execute_query(connection, query)
            except Exception as e:
                return f"value occured during executing the query: {e}"
            
            print("put enrollment success")
            return "put enrollment success"
        