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
    return render_template("detailed_question.html", question=question)

# /add-question
#
# /list?order_by=title &order_direction=desc
#
# /question/<question_id>/edit
#
# /question/<question_id>/delete
#


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
