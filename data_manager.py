import database_common
from psycopg2 import sql
import util


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT id, submission_time, view_number, title, message 
                    FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question_by_id = cursor.fetchone()
    question_by_id["message"] = util.convert_linebreaks_to_br(question_by_id["message"])
    return question_by_id


@database_common.connection_handler
def get_question_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id
                    FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    question = cursor.fetchone()
    return question


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT id, submission_time, question_id, message 
                    FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    answer_by_id = cursor.fetchone()
    return answer_by_id


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT id, message, submission_time
                    FROM answer
                    WHERE question_id = %(question_id)s ;
                    """,
                   {'question_id': question_id})
    answers_by_id = cursor.fetchall()
    for answer in answers_by_id:
        answer["message"] = util.convert_linebreaks_to_br(answer["message"])
    return answers_by_id


@database_common.connection_handler
def get_latest_five_question(cursor):
    cursor.execute("""
                    SELECT id, title, submission_time 
                    FROM question
                    ORDER BY submission_time DESC LIMIT 5;
                    """)
    latest_five_questions_data = cursor.fetchall()
    return latest_five_questions_data


@database_common.connection_handler
def get_all_questions(cursor, ordered_by, direction):
    if ordered_by not in ["id", "title", "submission_time"] or direction not in ["DESC", "ASC"]:
        raise ValueError
    sql_string = sql.SQL("""
                    SELECT id, title, submission_time 
                    FROM question
                    ORDER BY {ordered_by} {direction};""").format(
                    ordered_by=sql.Identifier(ordered_by),
                    direction=sql.SQL(direction))
    cursor.execute(sql_string)
    all_questions = cursor.fetchall()
    return all_questions


@database_common.connection_handler
def add_question(cursor, question):
    question["submission_time"]=util.get_time()
    cursor.execute("""
                    INSERT INTO question (submission_time, title, message)
                    VALUES (%(submission_time)s, %(title)s, %(message)s)
                    """, question)


@database_common.connection_handler
def edit_question(cursor, title, message, question_id):
    current_time = util.get_time()
    cursor.execute(
                    """
                    UPDATE question
                    SET title= %(title)s, message= %(message)s, submission_time= %(current_time)s
                    WHERE id=%(question_id)s
                    """,
                    {"title": title, "message": message, "question_id": question_id, "current_time": current_time})


@database_common.connection_handler
def delete_question(cursor, id_to_delete):
    cursor.execute("""
                    DELETE FROM comment WHERE question_id = %(id_to_delete)s;
                    DELETE FROM comment WHERE answer_id IN (SELECT id FROM answer WHERE question_id = %(id_to_delete)s);
                    DELETE FROM answer WHERE question_id = %(id_to_delete)s;
                    DELETE FROM question_tag WHERE question_id = %(id_to_delete)s;
                    DELETE FROM question WHERE id = %(id_to_delete)s
                    """,
                   {'id_to_delete': id_to_delete})


@database_common.connection_handler
def insert_tag(cursor,name):
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES (%(name)s)
                    RETURNING id
                    """,
                   {'name': name})
    result = cursor.fetchall()
    print(result)
    return result[0]['id']


@database_common.connection_handler
def insert_question_tag(cursor, question_id, tag_id):
    cursor.execute("""
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES (%(question_id)s, %(tag_id)s)
                        """,
                   {'question_id': question_id, 'tag_id': tag_id})

def add_tag_to_question(tag, question_id):
    id = insert_tag(tag)
    insert_question_tag(question_id, id)


@database_common.connection_handler
def post_answer(cursor, message, question_id):
    submission_time = util.get_time()
    cursor.execute("""
                    INSERT INTO answer (submission_time, question_id, message)
                    VALUES(%(submission_time)s, %(question_id)s, %(message)s)
                    """,
                   {'submission_time': submission_time, 'question_id': question_id, 'message': message})


@database_common.connection_handler
def edit_answer(cursor, answer):
    answer["submission_time"] = util.get_time()
    cursor.execute("""
                    UPDATE answer
                    SET submission_time=%(submission_time)s, message=%(message)s
                    WHERE id=%(id)s""",
                   answer)


@database_common.connection_handler
def delete_an_answer(cursor, id_to_delete):
    cursor.execute("""
                    DELETE FROM comment WHERE answer_id = %(id_to_delete)s;
                    DELETE FROM answer WHERE id = %(id_to_delete)s
                    """,
                   {'id_to_delete': id_to_delete})


@database_common.connection_handler
def search(cursor, phrase):
    cursor.execute("""
                    SELECT DISTINCT id, title, submission_time
                    FROM question
                    WHERE
                        title LIKE '%%' || %(phrase)s || '%%'
                    OR message LIKE '%%' || %(phrase)s || '%%'
                    OR id IN
                        (SELECT question_id
                        FROM answer
                        WHERE
                            message LIKE '%%' || %(phrase)s || '%%');
                    """,
                   {'phrase': phrase})
    search_results = cursor.fetchall()
    return search_results
