def verify_initial_data(entity_name, entity_primary_key, user_data, terminal_error_statement, update_entity=False, pk_value=0):
    from modules_school.credentials_school import Creds
    from modules_school.sql_helper_school import create_connection, execute_read_query

    # If no keys and values are provided in the body in POSTMAN
    if not user_data:
        return f"{terminal_error_statement} no {entity_name} information added"

    if entity_primary_key in user_data:
        return f"{terminal_error_statement} not allowed to enter a(n) {entity_name} id"
    
    # checking in the database if the entity exists in the records
    if update_entity == True:
        my_creds = Creds
        connection = create_connection(my_creds.connection_string,
                                       my_creds.user_name,
                                       my_creds.password,
                                       my_creds.database_name)
        
        # Check if the table entry exists exists
        sql = f"SELECT * FROM {entity_name.upper()} WHERE {entity_primary_key.upper()} = {pk_value};"
        print(sql)
        current_entity = execute_read_query(connection, sql)
        if not current_entity:
            return f"{entity_name} #{pk_value} does not exist in the records"
    
    return "validation of initial user data success"


def verify_user_attributes(allowed_attributes, required_attributes, user_data, terminal_error_statement, post=False):
    # retrieve the attributes that have entry provided by the user
    retrieved_attributes = [key for key in user_data]

    # report an error if an attribute not in allowed_attributes is provided
    illegal_attributes = []
    for key in retrieved_attributes:
        if key not in allowed_attributes:
            illegal_attributes.append(key)

    if len(illegal_attributes) >= 1:
        return f"{terminal_error_statement} illegal attributes detected: {", ".join(illegal_attributes)}"
    
    # report an error if retrieved attributes are missing the required attributes
    if post == True:
        missing_attributes = []
        for key in required_attributes:
            if key not in retrieved_attributes:
                missing_attributes.append(key)

        if len(missing_attributes) >= 1:
            return f"{terminal_error_statement} missing attributes: {", ".join(missing_attributes)}"
    
    return "validation of user provided data success"


# validate each attributes and their data types
def validate_attribute(attribute_name, request_data, array_attribute_names, array_attribute_values, min=0, max=0, isinitial=False, isphone=False, isdate=False, vartype=str, hasminmax=False, isarray=False, array=[], isforeignkey=False, foreign_entity_name="", foreign_key_name="", isonetoone=False, entity_name=""):
    from modules_school.verify_date import is_valid_date

    if attribute_name in request_data:
        if (vartype == int) or (vartype == float):
            attribute_value = vartype(request_data[attribute_name])
        else: 
            attribute_value = vartype(request_data[attribute_name].lower().strip())

        if isinstance(attribute_value, (int, float)):
            if isinstance(attribute_value, float):
                attribute_value = round(attribute_value, 2)

            if hasminmax:
                if (attribute_value < min) or (attribute_value > max):
                    raise ValueError(f"{attribute_name} must be between {min} and {max}")
                
            if isforeignkey:
                from modules_school.credentials_school import Creds
                from modules_school.sql_helper_school import create_connection, execute_read_query

                foreign_entity_name = foreign_entity_name.upper().strip()
                foreign_key_name = foreign_key_name.upper().strip()

                my_creds = Creds
                connection = create_connection(my_creds.connection_string, my_creds.user_name, my_creds.password, my_creds.database_name)

                sql = f"SELECT * FROM {foreign_entity_name} WHERE {foreign_key_name} = {attribute_value}"
                print(sql) 
                table_row = execute_read_query(connection, sql)
                print(table_row)

                if not table_row:
                    raise ValueError(f"{foreign_entity_name} with the value {foreign_key_name} of {attribute_value} does not exist")
                
                if isonetoone:
                    entity_name = entity_name.upper().strip()

                    sql = f"SELECT * FROM {entity_name} WHERE {foreign_key_name} = {attribute_value}"
                    print(sql) 
                    table_row = execute_read_query(connection, sql)
                    print(table_row)

                    if len(table_row) >= 1:
                        raise ValueError(f"this {entity_name} already has formed one (maximum) relationship")
                    
            array_attribute_names.append(attribute_name)
            array_attribute_values.append(attribute_value)

            return attribute_name, attribute_value
            
        else:
            # value validation
            if isinitial == True:
                if (len(attribute_value) != max) or not(attribute_value.isalpha()):
                    raise ValueError(f"{attribute_name} must only be a letter")
            elif isphone == True:
                if (len(attribute_value) != max) or not(attribute_value.isdigit()):
                    raise ValueError(f"{attribute_name} must all be numeric and 10 digits")
            elif isdate == True:
                if is_valid_date(attribute_value) == False:
                    raise ValueError(f"{attribute_name} does not follow the correct format")
            elif isarray == True:
                if attribute_value not in array:
                    raise ValueError(f"{attribute_name} must only be: {", ".join(array)}")
            else:
                if len(attribute_value) > max:
                    raise ValueError(f"{attribute_name} must be less than {max} characters long")
                
            array_attribute_names.append(attribute_name)
            array_attribute_values.append(attribute_value)

            return attribute_name, attribute_value   
    else:
        pass

        # note: return statements for this function is only necessary when the values are sought to be stored in a varaible; otherwise, ignore


# validating associative tables based on their PK/FK
def validate_associative_table(entity_name, primary_key_name, primary_key_value, terminal_error_statement):
    from modules_school.credentials_school import Creds
    from modules_school.sql_helper_school import create_connection, execute_read_query

    entity_name = entity_name.upper().strip()
    primary_key_name = primary_key_name.upper().strip()

    if primary_key_value is None:
        return f"{terminal_error_statement} {primary_key_name} must appear"
    
    my_creds = Creds
    connection = create_connection(my_creds.connection_string, my_creds.user_name, my_creds.password, my_creds.database_name)

    sql = f"SELECT * FROM {entity_name} WHERE {primary_key_name.upper()} = {primary_key_value}" 
    table_row = execute_read_query(connection, sql)

    if table_row:
        pass
    else:
        return f"{terminal_error_statement} {primary_key_name}: {primary_key_value} does not exists"
    
    return "pk found"
