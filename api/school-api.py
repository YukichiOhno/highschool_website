import flask
from flask import jsonify, request
from flask_cors import CORS
from modules_school.sql_helper_school import create_connection, execute_read_query, execute_query
from modules_school.credentials_school import Creds
from modules_school.query_looper_values import insert_query_looper_values_1_table as insert_query, update_query_looper_values_1_table as update_query
from modules_school.entity_attributes_provider import entity_attributes_provider, attribute_options
from modules_school.verify_user_attributes import verify_user_attributes, verify_initial_data, validate_attribute, validate_associative_table

app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show errors in browser

# disables CORS blocking API calls from this port to webserver Fetch API calls
CORS(app)

my_creds = Creds()
connection = create_connection(my_creds.connection_string,
                                my_creds.user_name,
                                my_creds.password,
                                my_creds.database_name)

# STUDENT
# retrieve student table information
@app.route("/api/student", methods=["GET"])
def get_student():
    query = "SELECT * FROM STUDENT"
    student_table = execute_read_query(connection, query)
    # return jsonify(student_table)


    for student in student_table:
        stud_id = student["STUD_ID"]
        sql = f"SELECT G.*, GUID_IDENTITY\n" \
              f"FROM STUDENT S\n" \
              f"JOIN STUDENT_GUIDE SG ON S.STUD_ID = SG.STUD_ID\n" \
              f"JOIN GUIDE G ON SG.GUID_ID = G.GUID_ID\n" \
              f"WHERE S.STUD_ID = {stud_id};"
        
        stud_guidances = execute_read_query(connection, sql)
        stud_guidances = stud_guidances
        student["STUD_GUIDES"] = stud_guidances

    return jsonify(student_table)


# add a student to the student table
@app.route("/api/student", methods=["POST"])
def post_student():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_student error. check terminal"
    terminal_error_statement = "post_student error:"
    
    print("\nprocessing post_student...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("student", "STUD_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for student table
    required_attributes, allowed_attributes = entity_attributes_provider("student")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
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
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("student", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post student success")
    return "post student success"


# update an existing student table row
@app.route("/api/student/<int:stud_id>", methods=["PUT"])
def put_student(stud_id):
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


# delete an existing student table row
@app.route("/api/student/<int:stud_id>", methods=["DELETE"])
def delete_student(stud_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_student error. check terminal"
    terminal_error_statement = "delete_student error:"

    print("\nprocessing delete_student...")
    sql = "SELECT * FROM STUDENT;"
    student_table = execute_read_query(connection, sql)

    for i in range(len(student_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = student_table[i]["STUD_ID"]
        if stud_id == id_to_delete:
            delete_query = f"DELETE FROM STUDENT WHERE STUD_ID = {stud_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM STUDENT WHERE STUD_ID = {stud_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete student: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete student success")
            return "delete student success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


# GUIDE
# retrieve guide table information
@app.route("/api/guide", methods=["GET"])
def get_guide():
    query = "SELECT * FROM GUIDE"
    student_table = execute_read_query(connection, query)
    return jsonify(student_table)


# add a guide to the guide table
@app.route("/api/guide", methods=["POST"])
def post_guide():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_guide error. check terminal"
    terminal_error_statement = "post_guide error:"
    
    print("\nprocessing post_guide...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("guide", "GUID_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("guide")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("GUID_FNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("GUID_LNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("GUID_INITIAL", request_data, user_attributes_names, user_attributes_values, isinitial=True, max=1)
        validate_attribute("GUID_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("GUID_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("GUID_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("GUID_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("guide", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post guide success")
    return "post guide success"


# update an existing guide table row
@app.route("/api/guide/<int:guid_id>", methods=["PUT"])
def put_guide(guid_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_guide error. check terminal"
    terminal_error_statement = "put_guide error:"

    print("\nprocessing put_guide...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("guide", "GUID_ID", user_data, terminal_error_statement, update_entity=True, pk_value=guid_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("guide")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("GUID_FNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("GUID_LNAME", request_data, user_attributes_names, user_attributes_values, max=20)
        validate_attribute("GUID_INITIAL", request_data, user_attributes_names, user_attributes_values, isinitial=True, max=1)
        validate_attribute("GUID_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("GUID_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("GUID_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("GUID_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("guide", user_attributes_names, user_attributes_values, "GUID_ID", guid_id)
    print(f"{query}")
    execute_query(connection, query)
    print("put guide success")
    return "put guide success"


# delete an existing guide table row
@app.route("/api/guide/<int:guid_id>", methods=["DELETE"])
def delete_guide(guid_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_guide error. check terminal"
    terminal_error_statement = "delete_guide error:"

    print("\nprocessing delete_guide...")
    sql = "SELECT * FROM GUIDE;"
    guide_table = execute_read_query(connection, sql)

    for i in range(len(guide_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = guide_table[i]["GUID_ID"]
        if guid_id == id_to_delete:
            delete_query = f"DELETE FROM GUIDE WHERE GUID_ID = {guid_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM GUIDE WHERE GUID_ID = {guid_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete guide: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete guide success")
            return "delete guide success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


# STUDENT_GUIDE
# add a relationship between a student and a guide
@app.route("/api/student_guide", methods=["POST"])
def post_student_guide():
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
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("student_guide", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post student_guide success")
    return "post student_guide success"


# COURSE
# retrieve course table information
@app.route("/api/course", methods=["GET"])
def get_course():
    query = "SELECT * FROM COURSE"
    course_table = execute_read_query(connection, query)
    return jsonify(course_table)


# add a course to the course table
@app.route("/api/course", methods=["POST"])
def post_course():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_course error. check terminal"
    terminal_error_statement = "post_course error:"
    
    print("\nprocessing post_course...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("course", "COURSE_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("course")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("COURSE_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("COURSE_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("COURSE_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("course_type"))
        validate_attribute("COURSE_GRADE_LVL", request_data, user_attributes_names, user_attributes_values, min=9, max=12, vartype=int, hasminmax=True)
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("course", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post course success")
    return "post course success"


# update an existing course table row
@app.route("/api/course/<int:course_id>", methods=["PUT"])
def put_course(course_id):
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
        validate_attribute("COURSE_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("course_type"))
        validate_attribute("COURSE_GRADE_LVL", request_data, user_attributes_names, user_attributes_values, min=9, max=12, vartype=int, hasminmax=True)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("course", user_attributes_names, user_attributes_values, "COURSE_ID", course_id)
    print(f"{query}")
    execute_query(connection, query)
    print("put course success")
    return "put course success"


# delete an existing course table row
@app.route("/api/course/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_course error. check terminal"
    terminal_error_statement = "delete_course error:"

    print("\nprocessing delete_course...")
    sql = "SELECT * FROM COURSE;"
    course_table = execute_read_query(connection, sql)  

    for i in range(len(course_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = course_table[i]["COURSE_ID"]
        if course_id == id_to_delete:
            delete_query = f"DELETE FROM COURSE WHERE COURSE_ID = {course_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM COURSE WHERE COURSE_ID = {course_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete guide: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete course success")
            return "delete course success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


app.run(threaded=True, port=5001)