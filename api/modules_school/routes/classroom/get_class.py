import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table


# retrieve class table information
def get_class(connection):
    query = "SELECT * FROM CLASS"
    class_table = execute_read_query(connection, query)
    
    for classroom in class_table:
        class_id = classroom["CLASS_ID"]
        sql = f"SELECT S.* FROM STUDENT S JOIN ENROLLMENT E ON S.STUD_ID = E.STUD_ID WHERE CLASS_ID = {class_id} AND NOT(ENROLL_STATUS = 'dropped');"

        class_students = execute_read_query(connection, sql)
        class_students = class_students
        classroom["STUDENTS"] = class_students

    return jsonify(class_table)