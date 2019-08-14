from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
def index():
    five_question_data = data_manager.get_latest_five_question()
    return render_template('home_page.html', all_questions=five_question_data)


@app.route("/list")
def list_all_questions():
    order_direction = request.args.get("order_direction")
    order_by = request.args.get("order_by")
    if not order_by or not order_direction:
        order_by = "submission_time"
        order_direction = "DESC"
    try:
        all_questions = data_manager.get_all_questions(order_by, order_direction)
        return render_template("all_questions.html", all_questions=all_questions)
    except ValueError:
        return render_template("sorting_error.html")


@app.route("/question/<question_id>")
def detail_question(question_id):
    question = data_manager.get_questions_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template("detailed_question.html", question=question, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')

    question = {
        'title': request.form['title'],
        'message': request.form['message']
    }
    data_manager.add_new_row(question, "question")
    return redirect(url_for('list_all_questions'))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_questions_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit_question.html', question=question)

    edited_question = {
        'id': question['id'],
        'title': request.form['title'],
        'message': request.form['message']
    }
    data_manager.rewrite_data('question', edited_question)
    return redirect(url_for("detail_question", question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    answers = data_manager.get_answers_by_question_id(question_id)
    answer_ids = data_manager.get_ids_from_answers(answers)
    for answer_id in answer_ids:
        data_manager.delete_a_row(answer_id, "answer")
    data_manager.delete_a_row(question_id, "question")
    return redirect(url_for('list_all_questions'))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question = data_manager.get_question_by_answer_id(answer_id)
    data_manager.delete_an_answer(answer_id)
    return redirect(url_for('detail_question', question_id=question[0]['question_id']))


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == "GET":
        return render_template('add_answer.html', question_id=question_id)

    answer = {
        'message': request.form['answer_message'],
        'question_id': question_id
    }
    data_manager.add_new_row(answer, 'answer')
    return redirect(url_for("detail_question", question_id=question_id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
