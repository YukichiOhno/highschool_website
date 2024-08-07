def entity_attributes_provider(entity):
    entity = entity.lower()
    allowed_attributes = []
    required_attributes = []
    optional_attributes = []

    if entity == "student":
        required_attributes = ["STUD_FNAME", 
                               "STUD_LNAME", 
                               "STUD_DOB", 
                               "STUD_ADDRESS", 
                               "STUD_CITY", 
                               "STUD_ENROLL_DATE", 
                               "STUD_GRADE_LVL"]

        optional_attributes = ["STUD_INITIAL",
                               "STUD_EMAIL",
                               "STUD_PHONE",
                               "STUD_GPA"]
    
    elif entity == "guide":
        required_attributes = ["GUID_FNAME",
                               "GUID_LNAME",
                               "GUID_ADDRESS",
                               "GUID_CITY",
                               "GUID_PHONE"]
        
        optional_attributes = ["GUID_INITIAL",
                               "GUID_EMAIL"]
        
    elif entity == "student_guide":
        required_attributes = ["GUID_IDENTITY"]
        
    elif entity == "course":
        required_attributes = ["COURSE_NAME",
                               "COURSE_DESC",
                               "COURSE_TYPE",
                               "COURSE_HRS",
                               "COURSE_GRADE_LVL"]
        
    elif entity == "supplier":
        required_attributes = ["SUPP_NAME",
                               "SUPP_PHONE",
                               "SUPP_EMAIL",
                               "SUPP_ADDRESS",
                               "SUPP_CITY",
                               "SUPP_TYPE",
                               "SUPP_CONT_START",
                               "SUPP_CONT_END"]
        
    elif entity == "department":
        required_attributes = ["DEPT_NAME",
                               "DEPT_DESC"]
        
        optional_attributes = ["EMP_ID"]

    elif entity == "job_position":
        required_attributes = ["POS_TITLE",
                               "POS_DESC",
                               "POS_SALARY",
                               "DEPT_CODE"]
    
        optional_attributes = ["POS_REQ"]

    elif entity == "employee":
        required_attributes = ["EMP_FNAME",
                               "EMP_LNAME",
                               "EMP_DOB",
                               "EMP_ADDRESS",
                               "EMP_CITY",
                               "EMP_PHONE",
                               "EMP_EMAIL",
                               "EMP_EMPLOY_DATE"]
        
        optional_attributes = ["EMP_INITIAL",
                               "POS_CODE"]
    
    elif entity == "class":
        required_attributes = ["CLASS_CAPACITY",
                               "COURSE_ID"]
        
        optional_attributes = ["CLASS_ROOM",
                               "CLASS_BLDG_ROOM",
                               "EMP_ID"]
        
    elif entity == "enrollment":
        required_attributes = ["ENROLL_STATUS",
                               "ENROLL_DATE"]
        
        optional_attributes = ["ENROLL_SCORE"]

    elif entity == "budget":
        required_attributes = ["BUD_TYPE",
                               "BUD_DESC",
                               "BUD_ALLOCATED",
                               "BUD_APPROVAL_DATE",
                               "BUD_EXP_DATE",
                               "DEPT_CODE"]
        
    elif entity == "inventory":
        required_attributes = ["INVT_NAME",
                               "INVT_DESC",
                               "INVT_CATEGORY"]
        
        optional_attributes = ["INVT_EXP_DATE",
                               "INVT_QTY"]

    elif entity == "item":
        required_attributes = ["ITEM_QTY",
                               "ROOM_NUM",
                               "DEPT_CODE",
                               "INVT_CODE"]
        
    elif entity == "invoice":
        required_attributes = ["INV_ISSUE_DATE",
                               "INV_DUE_DATE",
                               "DEPT_CODE",
                               "SUPP_ID"]
        

    allowed_attributes = required_attributes + optional_attributes
    return required_attributes, allowed_attributes


def attribute_options(attribute_name):
    attribute_name = attribute_name.lower().strip()

    if attribute_name == "course_type":
        acceptable_values = ["lecture",
                             "lab",
                             "seminar",
                             "workshop",
                             "online",
                             "hybrid",
                             "tutorial",
                             "practicum",
                             "fieldwork",
                             "independent study"]
        
    elif attribute_name == "guid_identity":
        acceptable_values = ["mother",
                             "father",
                             "sister",
                             "brother",
                             "grandparent",
                             "uncle",
                             "aunt",
                             "cousin",
                             "godparent"]
        
    elif attribute_name == "supp_type":
        acceptable_values = ["stationery",
                             "electronics",
                             "furniture",
                             "books",
                             "cleaning supplies",
                             "meal"]
        
    elif attribute_name == "enroll_status":
        acceptable_values = ["enrolled",
                             "pending",
                             "dropped"]
        
    elif attribute_name == "bud_type":
        acceptable_values = ["academic",
                             "extracurricular activities",
                             "facilities and maintenance",
                             "administrative",
                             "student services",
                             "transportation",
                             "special programs",
                             "events and activities"]
        
    elif attribute_name == "invt_category":
        acceptable_values = ["office supply",
                             "classroom supply",
                             "art supply",
                             "science equipment",
                             "sports equipment",
                             "technology",
                             "furniture",
                             "educational material",
                             "cleaning supply",
                             "cafeteria supply",
                             "maintenance equipment",
                             "first aid and safety equipment",
                             "event supply",
                             "musical instrument",
                             "miscellaneous"]
        
    elif attribute_name == "inv_pay_status":
        acceptable_values = ["completed"]
        
    return acceptable_values

