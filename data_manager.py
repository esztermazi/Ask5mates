import connection


def next_id(data_type):
    dictionaries = connection.get_data_from_csv(data_type)
    if len(dictionaries) == 0:
        first_id = "1"
        return first_id
    else:
        return str(int(dictionaries[-1]["id"]) + 1)


def add_new_row(new_dict, data_type):
    new_id = next_id(data_type)
    new_dict["id"] = new_id
    connection.write_new_line_to_csv(new_dict, data_type)


def rewrite_data(data_type, dict_to_rewrite):
    dictionaries = connection.get_data_from_csv(data_type)
    for index in range(len(dictionaries)):
        if dictionaries[index]["id"] == dict_to_rewrite["id"]:
            dictionaries[index] = dict_to_rewrite
    connection.rewrite_csv(dictionaries, data_type)


def delete_a_row(id_to_delete, data_type):
    dictionaries = connection.get_data_from_csv(data_type)
    for index in range(len(dictionaries)):
        if dictionaries[index]["id"] == id_to_delete:
            dictionaries.pop(index)
    connection.rewrite_csv(dictionaries, data_type)