from datetime import datetime
import time
import connection


def convert_time(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def get_unix_timestamp():
    return int(time.time())


def get_data(data_type, is_sorted=False, sort_key="submission_time", is_descending=True):
    all_data = connection.get_data_from_csv(data_type)
    if is_sorted:
        all_data.sort(key=lambda x: x[sort_key], reverse=is_descending)
    for row in all_data:
        row["submission_time"] = convert_time(int(row["submission_time"]))
        row["message"] = convert_linebreaks_to_br(row["message"])
    return all_data


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
    new_timestamp = get_unix_timestamp()
    new_dict["submission_time"] = new_timestamp
    new_dict["vote_number"] = "0"
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


def get_questions_by_id(question_id):
    all_questions = get_data("question")
    for question in all_questions:
        if question_id == question["id"]:
            return question


def get_answers_by_question_id(question_id):
    all_answers = get_data("answer", is_sorted=True)
    answers = []
    for answer in all_answers:
        if answer["question_id"] == question_id:
            answers.append(answer)
    return answers


def convert_linebreaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))
