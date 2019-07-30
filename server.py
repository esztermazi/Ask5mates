from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def index():
    all_questions = data_manager.get_data("question")
    return render_template("list.html", all_questions=all_questions)


# /question/<question_id>
#
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
