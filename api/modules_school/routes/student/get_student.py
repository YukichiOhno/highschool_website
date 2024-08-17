import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table
from modules_school.value_converter import convert_values

# retrieve student table information
def get_student(connection):
    query = "SELECT * FROM STUDENT"
    student_table = execute_read_query(connection, query)
    convert_values(student_table)
    
    # return jsonify(student_table)

    for student in student_table:
        stud_id = student["STUD_ID"]
        sql = f"SELECT G.*, GUID_IDENTITY\n" \
              f"FROM STUDENT S\n" \
              f"JOIN STUDENT_GUIDE SG ON S.STUD_ID = SG.STUD_ID\n" \
              f"JOIN GUIDE G ON SG.GUID_ID = G.GUID_ID\n" \
              f"WHERE S.STUD_ID = {stud_id};"
        
        stud_guidances = execute_read_query(connection, sql)
        convert_values(stud_guidances)
        stud_guidances = stud_guidances
        student["STUD_GUIDES"] = stud_guidances

    return jsonify(student_table)
