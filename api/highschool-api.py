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
@app.route("/api/student", methods=["GET"])
def get_student_route():
    from modules_school.routes.student.get_student import get_student
    return get_student(connection)

@app.route("/api/student", methods=["POST"])
def post_student_route():
    from modules_school.routes.student.post_student import post_student
    return post_student(connection)

@app.route("/api/student/<int:stud_id>", methods=["PUT"])
def put_student_route(stud_id):
    from modules_school.routes.student.put_student import put_student
    return put_student(connection, stud_id)

@app.route("/api/student/<int:stud_id>", methods=["DELETE"])
def delete_student_route(stud_id):
    from modules_school.routes.student.delete_student import delete_student
    return delete_student(connection, stud_id)


# GUIDE
@app.route("/api/guide", methods=["GET"])
def get_guide_route():
    from modules_school.routes.guide.get_guide import get_guide
    return get_guide(connection)

@app.route("/api/guide", methods=["POST"])
def post_guide_route():
    from modules_school.routes.guide.post_guide import post_guide
    return post_guide(connection)

@app.route("/api/guide/<int:guid_id>", methods=["PUT"])
def put_guide_route(guid_id):
    from modules_school.routes.guide.put_guide import put_guide
    return put_guide(connection, guid_id)

@app.route("/api/guide/<int:guid_id>", methods=["DELETE"])
def delete_guide_route(guid_id):
    from modules_school.routes.guide.delete_guide import delete_guide
    return delete_guide(connection, guid_id)


# STUDENT GUIDE
@app.route("/api/student_guide", methods=["POST", "PUT"])
def post_student_guide_route():
    from modules_school.routes.student_guide.post_student_guide import post_student_guide
    return post_student_guide(connection)

@app.route("/api/student_guide", methods=["DELETE"])
def delete_student_guide_route():
    from modules_school.routes.student_guide.delete_student_guide import delete_student_guide
    return delete_student_guide(connection)


# COURSE
@app.route("/api/course", methods=["GET"])
def get_course_route():
    from modules_school.routes.course.get_course import get_course
    return get_course(connection)

@app.route("/api/course", methods=["POST"])
def post_course_route():
    from modules_school.routes.course.post_course import post_course
    return post_course(connection)

@app.route("/api/course/<int:course_id>", methods=["PUT"])
def put_course_route(course_id):
    from modules_school.routes.course.put_course import put_course
    return put_course(connection, course_id)

@app.route("/api/course/<int:course_id>", methods=["DELETE"])
def delete_course_route(course_id):
    from modules_school.routes.course.delete_course import delete_course
    return delete_course(connection, course_id)


# SUPPLIER
@app.route("/api/supplier", methods=["GET"])
def get_supplier_route():
    from modules_school.routes.supplier.get_supplier import get_supplier
    return get_supplier(connection)

@app.route("/api/supplier", methods=["POST"])
def post_supplier_route():
    from modules_school.routes.supplier.post_supplier import post_supplier
    return post_supplier(connection)

@app.route("/api/supplier/<int:supp_id>", methods=["PUT"])
def put_supplier_route(supp_id):
    from modules_school.routes.supplier.put_supplier import put_supplier
    return put_supplier(connection, supp_id)

@app.route("/api/supplier/<int:supp_id>", methods=["DELETE"])
def delete_supplier_route(supp_id):
    from modules_school.routes.supplier.delete_supplier import delete_supplier
    return delete_supplier(connection, supp_id)


# DEPARTMENT
@app.route("/api/department", methods=["GET"])
def get_department_route():
    from modules_school.routes.department.get_department import get_department
    return get_department(connection)

@app.route("/api/department", methods=["POST"])
def post_department_route():
    from modules_school.routes.department.post_department import post_department
    return post_department(connection)

@app.route("/api/department/<int:dept_code>", methods=["PUT"])
def put_department_route(dept_code):
    from modules_school.routes.department.put_department import put_department
    return put_department(connection, dept_code)

@app.route("/api/department/<int:dept_code>", methods=["DELETE"])
def delete_department_route(dept_code):
    from modules_school.routes.department.delete_department import delete_department
    return delete_department(connection, dept_code)


# JOB POSITION
@app.route("/api/job_position", methods=["GET"])
def get_job_position_route():
    from modules_school.routes.job_position.get_job_position import get_job_position
    return get_job_position(connection)

@app.route("/api/job_position", methods=["POST"])
def post_job_position_route():
    from modules_school.routes.job_position.post_job_position import post_job_position
    return post_job_position(connection)

@app.route("/api/job_position/<int:pos_code>", methods=["PUT"])
def put_job_position_route(pos_code):
    from modules_school.routes.job_position.put_job_position import put_job_position
    return put_job_position(connection, pos_code)

@app.route("/api/job_position/<int:pos_code>", methods=["DELETE"])
def delete_job_position_route(pos_code):
    from modules_school.routes.job_position.delete_job_position import delete_job_position
    return delete_job_position(connection, pos_code)


# EMPLOYEE
@app.route("/api/employee", methods=["GET"])
def get_employee_route():
    from modules_school.routes.employee.get_employee import get_employee
    return get_employee(connection)

@app.route("/api/employee", methods=["POST"])
def post_employee_route():
    from modules_school.routes.employee.post_employee import post_employee
    return post_employee(connection)

@app.route("/api/employee/<int:emp_id>", methods=["PUT"])
def put_employee_route(emp_id):
    from modules_school.routes.employee.put_employee import put_employee
    return put_employee(connection, emp_id)

@app.route("/api/employee/<int:emp_id>", methods=["DELETE"])
def delete_employee_route(emp_id):
    from modules_school.routes.employee.delete_employee import delete_employee
    return delete_employee(connection, emp_id)


# CLASS
@app.route("/api/class", methods=["GET"])
def get_class_route():
    from modules_school.routes.classroom.get_class import get_class
    return get_class(connection)

@app.route("/api/class", methods=["POST"])
def post_class_route():
    from modules_school.routes.classroom.post_class import post_class
    return post_class(connection)

@app.route("/api/class/<int:class_id>", methods=["PUT"])
def put_class_route(class_id):
    from modules_school.routes.classroom.put_class import put_class
    return put_class(connection, class_id)

@app.route("/api/class/<int:class_id>", methods=["DELETE"])
def delete_class_route(class_id):
    from modules_school.routes.classroom.delete_class import delete_class
    return delete_class(connection, class_id)


# ENROLLMENT
@app.route("/api/enrollment", methods=["POST", "PUT"])
def post_enrollment_route():
    from modules_school.routes.enrollment.post_enrollment import post_enrollment
    return post_enrollment(connection)

@app.route("/api/enrollment", methods=["DELETE"])
def delete_enrollment_route():
    from modules_school.routes.enrollment.delete_enrollment import delete_enrollment
    return delete_enrollment(connection)


# BUDGET
@app.route("/api/budget", methods=["GET"])
def get_budget_route():
    from modules_school.routes.budget.get_budget import get_budget
    return get_budget(connection)

@app.route("/api/budget", methods=["POST"])
def post_budget_route():
    from modules_school.routes.budget.post_budget import post_budget
    return post_budget(connection)

@app.route("/api/budget/<int:bud_id>", methods=["PUT"])
def put_budget_route(bud_id):
    from modules_school.routes.budget.put_budget import put_budget
    return put_budget(connection, bud_id)

@app.route("/api/budget/<int:bud_id>", methods=["DELETE"])
def delete_budget_route(bud_id):
    from modules_school.routes.budget.delete_budget import delete_budget
    return delete_budget(connection, bud_id)


# INVENTORY
@app.route("/api/inventory", methods=["GET"])
def get_inventory_route():
    from modules_school.routes.inventory.get_inventory import get_inventory
    return get_inventory(connection)

@app.route("/api/inventory", methods=["POST"])
def post_inventory_route():
    from modules_school.routes.inventory.post_inventory import post_inventory
    return post_inventory(connection)

@app.route("/api/inventory/<int:invt_code>", methods=["PUT"])
def put_inventory_route(invt_code):
    from modules_school.routes.inventory.put_inventory import put_inventory
    return put_inventory(connection, invt_code)

@app.route("/api/inventory/<int:invt_code>", methods=["DELETE"])
def delete_inventory_route(invt_code):
    from modules_school.routes.inventory.delete_inventory import delete_inventory
    return delete_inventory(connection, invt_code)


# ITEM
@app.route("/api/item", methods=["GET"])
def get_item_route():
    from modules_school.routes.item.get_item import get_item
    return get_item(connection)

@app.route("/api/item", methods=["POST"])
def post_item_route():
    from modules_school.routes.item.post_item import post_item
    return post_item(connection)

@app.route("/api/item/<int:item_id>", methods=["PUT"])
def put_item_route(item_id):
    from modules_school.routes.item.put_item import put_item
    return put_item(connection, item_id)

@app.route("/api/item/<int:item_id>", methods=["DELETE"])
def delete_item_route(item_id):
    from modules_school.routes.item.delete_item import delete_item
    return delete_item(connection, item_id)

app.run(threaded=True, port=5002)