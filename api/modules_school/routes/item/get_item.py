import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table
from modules_school.value_converter import convert_values

# read item table
def get_item(connection):
    query = "SELECT * FROM ITEM"
    item_table = execute_read_query(connection, query)
    convert_values(item_table)
    return jsonify(item_table)