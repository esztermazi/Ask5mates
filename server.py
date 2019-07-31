from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def index():
    all_questions = data_manager.get_data("question", is_sorted=True, sort_key="submission_time")
    return render_template("list.html", all_questions=all_questions)


@app.route("/question/<question_id>")
def detail_question(question_id):
    question = data_manager.get_questions_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template("detailed_question.html", question=question, answers=answers)

@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = {
        'id': data_manager.next_id("question"),
        'submission_time': data_manager.get_unix_timestamp(),
        'view_number': 0,
        'vote_number': 0,
        'title': request.form['title'],
        'message': request.form['message'],
        'image': None
        }
        data_manager.add_new_row(question, "question")
        return redirect('/')
    return render_template('add_question.html')
#
# /list?order_by=title &order_direction=desc
#
# /question/<question_id>/edit
#
@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    data_manager.delete_a_row(question_id, "question")
    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
