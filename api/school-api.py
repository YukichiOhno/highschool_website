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
@app.route("/api/student_guide", methods=["POST", "PUT"])
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
    
    # setting up query: call insert_query_looper_values module for either PUT or POST methods
    if request.method == "POST":
        query = insert_query("student_guide", user_attributes_names, user_attributes_values)
        print(f"{query}")
        execute_query(connection, query)
        print("post student_guide success")
        return "post student_guide success"
    else:
        query = update_query("student_guide", user_attributes_names, user_attributes_values, "STUD_ID", stud_id, iscomposite=True, pk_name_2="GUID_ID", entity_id_2=guid_id)
        print(f"{query}")
        execute_query(connection, query)
        print("put student_guide success")
        return "put student_guide success"
    

# delete an existing student_guide relationship table row
@app.route("/api/student_guide", methods=["DELETE"])
def delete_student_guide():
    # get data and required debugging statements
    failed_data_entry_statement = "delete_student_guide error. check terminal"
    terminal_error_statement = "delete_student_guide error:"

    print("\nprocessing delete_student_guide...")
    stud_id = request.args.get("STUD_ID", type=int)
    guid_id = request.args.get("GUID_ID", type=int)
    sql = "SELECT * FROM STUDENT_GUIDE;"
    student_guide_table = execute_read_query(connection, sql)

    for i in range(len(student_guide_table) - 1, -1, -1):  # start, stop, step size
        stud_id_to_delete = student_guide_table[i]["STUD_ID"]
        guid_id_to_delete = student_guide_table[i]["GUID_ID"]
        if (guid_id == guid_id_to_delete) and (stud_id == stud_id_to_delete):
            pass
            delete_query = f"DELETE FROM STUDENT_GUIDE WHERE STUD_ID = {stud_id} AND GUID_ID = {guid_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM STUDENT_GUIDE WHERE STUD_ID = {stud_id} AND GUID_ID = {guid_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete student_guide: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete student_guide success")
            return "delete student_guide success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


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


# SUPPLIER
# retrieve supplier table information
@app.route("/api/supplier", methods=["GET"])
def get_supplier():
    query = "SELECT * FROM SUPPLIER"
    supplier_table = execute_read_query(connection, query)
    return jsonify(supplier_table)


# add a supplier to the supplier table
@app.route("/api/supplier", methods=["POST"])
def post_supplier():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_supplier error. check terminal"
    terminal_error_statement = "post_supplier error:"
    
    print("\nprocessing post_supplier...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("supplier", "SUPP_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("supplier")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("SUPP_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("SUPP_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("SUPP_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("supp_type"))
        validate_attribute("SUPP_CONT_START", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("SUPP_CONT_END", request_data, user_attributes_names, user_attributes_values, isdate=True)
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("supplier", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post supplier success")
    return "post supplier success"


# update an existing supplier table row
@app.route("/api/supplier/<int:supp_id>", methods=["PUT"])
def put_supplier(supp_id):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_supplier error. check terminal"
    terminal_error_statement = "put_supplier error:"

    print("\nprocessing put_supplier...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("supplier", "SUPP_ID", user_data, terminal_error_statement, update_entity=True, pk_value=supp_id)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("supplier")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("SUPP_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_PHONE", request_data, user_attributes_names, user_attributes_values, isphone=True, max=10)
        validate_attribute("SUPP_EMAIL", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_ADDRESS", request_data, user_attributes_names, user_attributes_values, max=150)
        validate_attribute("SUPP_CITY", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("SUPP_TYPE", request_data, user_attributes_names, user_attributes_values, isarray=True, array=attribute_options("supp_type"))
        validate_attribute("SUPP_CONT_START", request_data, user_attributes_names, user_attributes_values, isdate=True)
        validate_attribute("SUPP_CONT_END", request_data, user_attributes_names, user_attributes_values, isdate=True)

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("supplier", user_attributes_names, user_attributes_values, "SUPP_ID", supp_id)
    print(f"{query}")
    execute_query(connection, query)
    print("put supplier success")
    return "put supplier success"


# delete an existing supplier table row
@app.route("/api/supplier/<int:supp_id>", methods=["DELETE"])
def delete_supplier(supp_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_supplier error. check terminal"
    terminal_error_statement = "delete_supplier error:"

    print("\nprocessing delete_supplier...")
    sql = "SELECT * FROM SUPPLIER;"
    supplier_table = execute_read_query(connection, sql)  

    for i in range(len(supplier_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = supplier_table[i]["SUPP_ID"]
        if supp_id == id_to_delete:
            delete_query = f"DELETE FROM SUPPLIER WHERE SUPP_ID = {supp_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM SUPPLIER WHERE SUPP_ID = {supp_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete supplier: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete supplier success")
            return "delete supplier success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


# DEPARTMENT
# retrieve course table information
@app.route("/api/department", methods=["GET"])
def get_department():
    query = "SELECT * FROM DEPARTMENT"
    department_table = execute_read_query(connection, query)
    return jsonify(department_table)


# add a department to the department table
@app.route("/api/department", methods=["POST"])
def post_department():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_department error. check terminal"
    terminal_error_statement = "post_department error:"
    
    print("\nprocessing post_department...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("department", "DEPT_CODE", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("department")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("DEPT_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("DEPT_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("EMP_ID", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="department", foreign_key_name="EMP_ID")
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("department", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post department success")
    return "post department success"


# update an existing department table row
@app.route("/api/department/<int:dept_code>", methods=["PUT"])
def put_department(dept_code):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_department error. check terminal"
    terminal_error_statement = "put_department error:"

    print("\nprocessing put_department...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("department", "DEPT_CODE", user_data, terminal_error_statement, update_entity=True, pk_value=dept_code)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("department")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("DEPT_NAME", request_data, user_attributes_names, user_attributes_values, max=50)
        validate_attribute("DEPT_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("EMP_ID", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="employee", foreign_key_name="EMP_ID")

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("department", user_attributes_names, user_attributes_values, "DEPT_CODE", dept_code)
    print(f"{query}")
    execute_query(connection, query)
    print("put department success")
    return "put department success"


# delete an existing department table row
@app.route("/api/department/<int:dept_code>", methods=["DELETE"])
def delete_department(dept_code):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_department error. check terminal"
    terminal_error_statement = "delete_department error:"

    print("\nprocessing delete_department...")
    sql = "SELECT * FROM DEPARTMENT;"
    department_table = execute_read_query(connection, sql)  

    for i in range(len(department_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = department_table[i]["DEPT_CODE"]
        if dept_code == id_to_delete:
            delete_query = f"DELETE FROM DEPARTMENT WHERE DEPT_CODE = {dept_code}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM DEPARTMENT WHERE DEPT_CODE = {dept_code}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete department: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete department success")
            return "delete department success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


# JOB POSITION
# retrieve course table information
@app.route("/api/job_position", methods=["GET"])
def get_job_position():
    query = "SELECT * FROM JOB_POSITION"
    job_position_table = execute_read_query(connection, query)
    return jsonify(job_position_table)


# add a job position to the job position table
@app.route("/api/job_position", methods=["POST"])
def post_job_position():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_job_position error. check terminal"
    terminal_error_statement = "post_job_position error:"
    
    print("\nprocessing post_job_position...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("job_position", "POS_CODE", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("job_position")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("POS_TITLE", request_data, user_attributes_names, user_attributes_values, max=25)
        validate_attribute("POS_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("POS_SALARY", request_data, user_attributes_names, user_attributes_values, vartype=float, max=999999.99, hasminmax=True)
        validate_attribute("POS_REQ", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("DEPT_CODE", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="department", foreign_key_name="DEPT_CODE")
        
    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("job_position", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post job_position success")
    return "post job_position success"


# update an existing job position table row
@app.route("/api/job_position/<int:pos_code>", methods=["PUT"])
def put_job_position(pos_code):
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "put_job_position error. check terminal"
    terminal_error_statement = "put_job_position error:"

    print("\nprocessing put_job_position...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("job_position", "POS_CODE", user_data, terminal_error_statement, update_entity=True, pk_value=pos_code)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("job_position")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement)
    print(verify_attributes)
    if verify_attributes != "validation of user provided data success":
        return failed_data_entry_statement
    
    # validate and manipulate entered user attributes
    try:
        user_attributes_names = []
        user_attributes_values = []

        validate_attribute("POS_TITLE", request_data, user_attributes_names, user_attributes_values, max=25)
        validate_attribute("POS_DESC", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("POS_SALARY", request_data, user_attributes_names, user_attributes_values, vartype=float, max=999999.99, hasminmax=True)
        validate_attribute("POS_REQ", request_data, user_attributes_names, user_attributes_values, max=65535)
        validate_attribute("DEPT_CODE", request_data, user_attributes_names, user_attributes_values, vartype=int, isforeignkey=True, foreign_entity_name="department", foreign_key_name="DEPT_CODE")

    except ValueError as e:
        print(f"{terminal_error_statement} {e}")
        return failed_data_entry_statement
    
    # setting up query: call update_query_looper_values module
    query = update_query("job_position", user_attributes_names, user_attributes_values, "POS_CODE", pos_code)
    print(f"{query}")
    execute_query(connection, query)
    print("put job_position success")
    return "put job_position success"


# delete an existing job_position table row
@app.route("/api/job_position/<int:pos_code>", methods=["DELETE"])
def delete_job_position(pos_code):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_job_position error. check terminal"
    terminal_error_statement = "delete_job_position error:"

    print("\nprocessing delete_job_position...")
    sql = "SELECT * FROM JOB_POSITION;"
    job_position_table = execute_read_query(connection, sql)  

    for i in range(len(job_position_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = job_position_table[i]["POS_CODE"]
        if pos_code == id_to_delete:
            delete_query = f"DELETE FROM JOB_POSITION WHERE POS_CODE = {pos_code}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM JOB_POSITION WHERE POS_CODE = {pos_code}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete job_position: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete job_position success")
            return "delete job_position success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


# EMPLOYEE
# retrieve course table information
@app.route("/api/employee", methods=["GET"])
def get_employee():
    query = "SELECT * FROM EMPLOYEE"
    employee_table = execute_read_query(connection, query)
    return jsonify(employee_table)


# add an employee to the employee table
@app.route("/api/employee", methods=["POST"])
def post_employee():
    # get data and required debugging statements
    request_data = request.get_json()
    user_data = request_data.keys()
    failed_data_entry_statement = "post_employee error. check terminal"
    terminal_error_statement = "post_employee error:"
    
    print("\nprocessing post_employee...")
    # If no keys and values are provided in the body in POSTMAN and throw error if PK is provided
    verify_user_data = verify_initial_data("employee", "EMP_ID", user_data, terminal_error_statement)
    print(verify_user_data)
    if verify_user_data != "validation of initial user data success":
        return failed_data_entry_statement
    
    # acquire necessary attributes for the table
    required_attributes, allowed_attributes = entity_attributes_provider("employee")
    
    # retrieve attributes provided by the user and perform validation
    verify_attributes = verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=True)
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
    
    # setting up query: call insert_query_looper_values module
    query = insert_query("employee", user_attributes_names, user_attributes_values)
    print(f"{query}")
    execute_query(connection, query)
    print("post employee success")
    return "post employee success"


# update an existing employee table row
@app.route("/api/employee/<int:emp_id>", methods=["PUT"])
def put_employee(emp_id):
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
    execute_query(connection, query)
    print("put employee success")
    return "put employee success"


# delete an existing employee table row
@app.route("/api/employee/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    # get data and required debugging statements
    failed_data_entry_statement = "delete_employee error. check terminal"
    terminal_error_statement = "delete_employee error:"

    print("\nprocessing delete_employee...")
    sql = "SELECT * FROM EMPLOYEE;"
    employee_table = execute_read_query(connection, sql)  

    for i in range(len(employee_table) - 1, -1, -1):  # start, stop, step size
        id_to_delete = employee_table[i]["EMP_ID"]
        if emp_id == id_to_delete:
            delete_query = f"DELETE FROM EMPLOYEE WHERE EMP_ID = {emp_id}"
            execute_query(connection, delete_query)
            check_sql = f"SELECT * FROM EMPLOYEE WHERE EMP_ID = {emp_id}"
            check = execute_read_query(connection, check_sql)
            print(check)
            if check:
                print(f"{terminal_error_statement} cannot delete employee: referenced by other entities in other table")
                return failed_data_entry_statement
            print("delete employee success")
            return "delete employee success"

    print(f"{terminal_error_statement} invalid id")
    return failed_data_entry_statement


app.run(threaded=True, port=5001)