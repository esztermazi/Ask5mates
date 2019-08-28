from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import util

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    five_question_data = data_manager.get_latest_five_question()
    print(five_question_data)
    print(type(five_question_data))
    return render_template('home_page.html', all_questions=five_question_data)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        user_name = request.form['user_name']
        is_valid_username = data_manager.validate_new_username(user_name)
        if not is_valid_username:
            error = 'Username is not available! Please choose another one.'
            return render_template('registration.html', message=error, user_name=user_name)
        else:
            password1 = request.form['password']
            password2 = request.form['password_again']
            is_valid_password = util.validate_password(password1, password2)
            if not is_valid_password:
                error = 'Passwords are not matching'
                return render_template('registration.html', message=error, user_name=user_name)
            else:
                hash = util.hash_password(password1)
                data_manager.register_user(user_name, hash)
                message = f'Successful registration as {user_name}'
                return render_template('registration.html', message=message)
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']

    alert_message = 'Invalid user name or password!'
    if not data_manager.check_username(username):
        return render_template('login.html', alert_message=alert_message)

    hashed_password = data_manager.get_hashed_password(username)
    if not util.verify_password(password, hashed_password):
        return render_template('login.html', alert_message=alert_message)

    session['username'] = request.form['username']
    return redirect(url_for('list_all_questions'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/list')
def list_all_questions():
    order_direction = request.args.get('order_direction')
    order_by = request.args.get('order_by')
    if not order_by or not order_direction:
        order_by = 'submission_time'
        order_direction = 'DESC'
    try:
        all_questions = data_manager.get_all_questions(order_by, order_direction)
        return render_template('all_questions.html', all_questions=all_questions, order_direction=order_direction,
                               order_by=order_by)
    except ValueError:
        return render_template('sorting_error.html')


@app.route('/question/<question_id>')
def detail_question(question_id):
    if request.args.get('count_view'):
        data_manager.increase_view_number(question_id)
        return redirect(url_for("detail_question", question_id=question_id))
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    tags = data_manager.get_tags_by_question_id(question_id)
    return render_template('detailed_question.html', question=question, tags=tags, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    user_id = data_manager.get_user_id_by_username(session['username'])
    question = {
        'title': request.form['title'],
        'message': request.form['message'],
        'user_id': user_id
    }
    data_manager.add_question(question)
    return redirect(url_for('list_all_questions'))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit_question.html', question=question)
    title = request.form['title'],
    message = request.form['message']
    data_manager.edit_question(title=title, message=message, question_id=question_id)
    return redirect(url_for('detail_question', question_id=question_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('list_all_questions'))


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_tag_to_question(question_id):
    if request.method == 'GET':
        return render_template('add_tag.html', question_id=question_id)
    tag = request.form['tag']
    data_manager.add_tag_to_question(tag, question_id)
    return redirect(url_for('detail_question', question_id=question_id))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)
    message = request.form['message']
    data_manager.post_answer(message, question_id)
    return redirect(url_for('detail_question', question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    if request.method == 'GET':
        return render_template('edit_answer.html', answer=answer)

    answer['message'] = request.form['message']
    data_manager.edit_answer(answer)
    return redirect(url_for('detail_question', question_id=answer['question_id']))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question = data_manager.get_question_by_answer_id(answer_id)
    data_manager.delete_an_answer(answer_id)
    return redirect(url_for('detail_question', question_id=question['question_id']))


@app.route('/search')
def search():
    search_phrase = request.args.get('search_phrase')
    results = data_manager.search(search_phrase)
    return render_template('search.html', results=results, search_phrase=search_phrase)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )
