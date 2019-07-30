from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return

# /list
#
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


if __name__ = "__main__":
    app.run(
        debug=True,
        port=5000
    )
