from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def index():
    not_show = ["image"]
    order_direction = request.args.get("order_direction")
    order_by = request.args.get("order_by")
    if not order_by or not order_direction:
        order_by = "submission_time"
        order_direction = "desc"
    is_descending = True if order_direction == "desc" else False
    all_questions = data_manager.get_data(
        "question",
        is_sorted=True,
        sort_key=order_by,
        is_descending=is_descending
        )
    return render_template(
        "list.html",
        all_questions=all_questions,
        not_show=not_show,
        order_by=order_by,
        order_direction=order_direction
    )


@app.route("/question/<question_id>")
def detail_question(question_id):
    not_show = ["question_id", "image", "vote_number"]
    question = data_manager.get_questions_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template("detailed_question.html", question=question, answers=answers, not_show=not_show)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')

    question = {
        'title': request.form['title'],
        'message': request.form['message']
    }
    data_manager.add_new_row(question, "question")
    return redirect(url_for('index'))


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
    return redirect(url_for('index'))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    question_id = data_manager.get_question_id(answer_id)
    data_manager.delete_a_row(answer_id, "answer")
    return redirect(url_for('detail_question', question_id=question_id))


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
