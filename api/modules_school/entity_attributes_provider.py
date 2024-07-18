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
                               "COURSE_GRADE_LVL"]

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
        
    return acceptable_values

