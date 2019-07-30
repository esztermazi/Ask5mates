from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def index():
    all_questions = data_manager.get_sorted_data("question", "submission_time", is_descending=True)
    return render_template("list.html", all_questions=all_questions)


@app.route("/question/<question_id>")
def detail_question(question_id):
    all_questions = data_manager.get_sorted_data("question", "submission_time", is_descending=True)
    for question in all_questions:
        if question_id == question["id"]:
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
