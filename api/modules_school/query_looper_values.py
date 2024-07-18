def insert_query_looper_values_1_table(table_name, required_array_names, required_array_values):
    query = f"INSERT INTO {table_name.upper()}({', '.join(required_array_names)})\n" \
            f"VALUES ("

    for i, value in enumerate(required_array_values):
        if isinstance(value, (int, float)):
            query += f"{value}"
        else:
            query += f"'{value}'"
        
        if i < len(required_array_values) - 1:
            query += ", "

    query += ")"

    return query


def update_query_looper_values_1_table(table_name, required_array_names, required_array_values, pk_name, entity_id): 
    query = f"UPDATE {table_name.upper()}\n" \
            f"SET "

    for i in range(len(required_array_names)):
        query += f"{required_array_names[i]} = "

        if isinstance(required_array_values[i], (int, float)):
            query += f"{required_array_values[i]}"
        else:
            query += f"'{required_array_values[i]}'"
        
        if i < len(required_array_values) - 1:
            query += ", "

    query += f"\nWHERE {pk_name} = {entity_id}"

    return query