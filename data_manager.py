import database_common
from psycopg2 import sql
import util


# def get_question_id(answer_id):
#     all_answers = connection.get_data_from_csv("answer")
#     for answer in all_answers:
#         if answer['id'] == answer_id:
#             return answer['question_id']


@database_common.connection_handler
def get_latest_five_question(cursor):
    cursor.execute("""
                    SELECT id, title, submission_time FROM question
                    ORDER BY submission_time DESC LIMIT 5;
                    """)
    latest_five_questions_data = cursor.fetchall()
    return latest_five_questions_data


@database_common.connection_handler
def get_all_questions(cursor, ordered_by, direction):
    if ordered_by not in ["id", "title", "submission_time"] or direction not in ["DESC", "ASC"]:
        raise ValueError
    cursor.execute(f"""
        SELECT id, title, submission_time FROM question
        ORDER BY {ordered_by} {direction};
        """)
    all_questions = cursor.fetchall()
    return all_questions


# def get_data(data_type, is_sorted=False, sort_key="submission_time", is_descending=True):
#     all_data = connection.get_data_from_csv(data_type)
#     if is_sorted:
#         all_data.sort(key=lambda x: x[sort_key], reverse=is_descending)
#     for row in all_data:
#         row["submission_time"] = util.convert_time(int(row["submission_time"]))
#         row["message"] = util.convert_linebreaks_to_br(row["message"])
#     return all_data


# def next_id(data_type):
#     dictionaries = connection.get_data_from_csv(data_type)
#     if len(dictionaries) == 0:
#         first_id = "1"
#         return first_id
#     else:
#         return str(int(dictionaries[-1]["id"]) + 1)
#
#
# def add_new_row(new_dict, data_type):
#     if data_type == 'question':
#         new_dict["view_number"] = "0"
#     new_id = next_id(data_type)
#     new_dict["id"] = new_id
#     new_timestamp = str(util.get_unix_timestamp())
#     new_dict["submission_time"] = new_timestamp
#     new_dict["vote_number"] = "0"
#     connection.write_new_line_to_csv(new_dict, data_type)
#
#
# def rewrite_data(data_type, dict_to_rewrite):
#     dictionaries = connection.get_data_from_csv(data_type)
#     for index in range(len(dictionaries)):
#         if dictionaries[index]["id"] == dict_to_rewrite["id"]:
#             dictionaries[index]["submission_time"] = str(util.get_unix_timestamp())
#             dictionaries[index]["title"] = dict_to_rewrite["title"]
#             dictionaries[index]["message"] = dict_to_rewrite["message"]
#     connection.rewrite_csv(dictionaries, data_type)
#
#
# def delete_a_row(id_to_delete, data_type):
#     dictionaries = connection.get_data_from_csv(data_type)
#     for index in range(len(dictionaries)):
#         if dictionaries[index]["id"] == id_to_delete:
#             dictionaries.pop(index)
#             break
#     connection.rewrite_csv(dictionaries, data_type)
#
#
# def get_questions_by_id(question_id):
#     all_questions = get_data("question")
#     for question in all_questions:
#         if question_id == question["id"]:
#             return question
#
#
# def get_answers_by_question_id(question_id):
#     all_answers = get_data("answer", is_sorted=True)
#     answers = []
#     for answer in all_answers:
#         if answer["question_id"] == question_id:
#             answers.append(answer)
#     return answers
#
#
# def get_ids_from_answers(answers):
#     answer_ids = [answer["id"] for answer in answers]
#     return answer_ids
