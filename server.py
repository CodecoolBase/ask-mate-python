from flask import Flask, render_template, request, redirect, session, url_for, escape
import question_data_manager
import comment_data_manager
import answer_data_manager
import util
import password_hash
import user_data_manager


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def render_index():
    questions = question_data_manager.collect_latest_5_question()
    if 'username' in session:
        user_data = user_data_manager.get_user_id(username=session['username'])
        user_id=user_data['id']
    else:
        user_id=''
    return render_template('index.html', questions=questions, user_id=user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    questions = question_data_manager.collect_latest_5_question()
    login_message = 'You are not logged in'
    session['login_message'] = login_message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        find_user = user_data_manager.find_user(username=username)
        if find_user != None:
            h_password = user_data_manager.get_hashed_password(user_name=username)
            hashed_password = h_password['hashed_password']
            verify = password_hash.verify_password(password, hashed_password)
            if verify == True:
                session['verify'] = verify
                session['username'] = username
                login_message = 'Logged in as ' + username
                session['login_message'] = login_message
                return redirect(url_for('render_index', verify=verify, login_message=login_message, questions=questions))
            else:
                session['verify'] = verify
                login_message = 'Invalid username or password'
                session['login_message'] = login_message
                return redirect(url_for('render_index', login_message=login_message, questions=questions))
        else:
            login_message = 'Invalid username or password'
            session['login_message'] = login_message
            return redirect(url_for('render_index', login_message=login_message, questions=questions))
    return redirect(url_for("render_index"))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('render_index'))


@app.route('/all_question')
def show_all_question():
    questions = question_data_manager.collect_questions()
    return render_template('all_question.html', questions=questions)


@app.route('/all_question/sort', methods=['GET', 'POST'])
def show_all_sorted_question():
    questions = sort_questions()
    return render_template('all_question.html', questions=questions)


def sort_questions():
    sort_options = request.form.get('sort_options')
    option = request.form.get('options')
    result = question_data_manager.sort_questions(option=option, how=sort_options)
    return result


@app.route('/question_page/vote_question',methods=['GET','POST'])
def vote_question():
    vote = int(request.form.get('vote_num'))
    vote_up = request.form.get('vote_up')
    vote_down = request.form.get('vote_down')
    q_id = request.form.get('q_id')
    id = question_data_manager.get_userid_used_question(q_id)
    reputation = question_data_manager.get_reputation(id[0]['user_id'])
    if request.method == 'POST':
        if vote_up == 'up':
            reputation = reputation['reputation'] + 5
            question_data_manager.update_reputation(id[0]['user_id'], reputation)
            vote += 1
        elif vote_down == 'down':
            reputation = reputation['reputation'] - 2
            question_data_manager.update_reputation(id[0]['user_id'], reputation)
            vote -= 1
        question_data_manager.update_vote_number_question(vote=vote, q_id=q_id)
        return redirect(url_for('show_question', question_id=q_id))


@app.route('/question_page/vote_answer',methods=['GET','POST'])
def vote_answer():
    q_id= request.form.get('question_id')
    vote = int(request.form.get('vote_num'))
    vote_up = request.form.get('vote_up')
    vote_down = request.form.get('vote_down')
    a_id = request.form.get('a_id')
    id = answer_data_manager.get_userid_used_answer(a_id)
    reputation = answer_data_manager.get_reputation(id[0]['user_id'])
    if request.method == 'POST':
        if vote_up == 'up':
            reputation = reputation['reputation'] + 10
            answer_data_manager.update_reputation(id[0]['user_id'], reputation)
            vote += 1
        elif vote_down == 'down':
            reputation = reputation['reputation'] -2
            answer_data_manager.update_reputation(id[0]['user_id'], reputation)
            vote -= 1
    answer_data_manager.update_vote_number_answer(vote=vote, a_id=a_id)
    return redirect(url_for('show_question',question_id=q_id))


@app.route('/question_page/<question_id>/delete')
def delete_question(question_id):
    question_data_manager.delete_question(q_id=question_id)
    return redirect(url_for('show_all_question'))


@app.route('/question_page/<question_id>/<answer_id>/answer-delete')
def delete_answer(question_id, answer_id):
    answer_data_manager.delete_answer(q_id=question_id, a_id=answer_id)
    return redirect(url_for('show_question',question_id=question_id))


@app.route('/search', methods=['POST'])
def search():
    question_data = request.form.get('question_data')
    result = question_data_manager.find_searched_questions(searched_data=question_data)
    return render_template('all_question.html', questions=result)


@app.route('/question_page/<question_id>')
def show_question(question_id):
    question = question_data_manager.find_question(q_id=question_id)
    answers = answer_data_manager.collect_answers(q_id=question_id)
    comment_data_manager.update_view_number(q_id=question_id)
    comment = comment_data_manager.collect_comment_to_question(q_id=question_id)
    answer_comment = []
    for answer in answers:
        temporary = comment_data_manager.collect_comment_to_answer(a_id=answer['id'])
        if len(temporary) > 0:
            answer_comment.append(temporary)
    if len(answer_comment) <= 0:
        answer_comment = ['']
    return render_template('question_page.html', question=question, answers=answers, comment=comment,
                           answer_comment=answer_comment[0])


@app.route('/question_page/<question_id>/edit')
def edit_question(question_id):
    result = question_data_manager.find_question(q_id=question_id)
    return render_template('add_question.html', result=result)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username, password = get_registration_data()
        submission_time = util.submission_time_generator()
        reputation=0
        user_data_manager.insert_new_user(submission_time=submission_time, username=username, h_password=password, user_reputation = reputation)
        return redirect('/')
    return render_template('registration.html')


def get_registration_data():
    user_name = request.form.get('user_name')
    password = password_hash.hash_password(request.form.get('password'))
    return user_name, password


@app.route('/rewrite_question', methods=['POST'])
def rewrite_question():
    updated_question = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'view_number': request.form.get('view_number'),
        'vote_number': request.form.get('vote_number'),
        'title': request.form.get('title'),
        'message': request.form.get('message'),
        'image': request.form.get('image')
    }
    question_data_manager.update_question(datas=updated_question)
    return redirect(url_for('show_question', question_id=updated_question['id']))


@app.route('/question_page/<question_id>/new-answer', methods=['GET', 'POST'])
def post_an_answer(question_id):
    result = []
    message = ""
    if request.method == 'POST':
        new_answer = create_answer(question_id, request.form['message'], request.form['image'])
        answer_data_manager.add_answer(form_data=new_answer)
        return redirect(url_for('show_question', question_id=question_id))
    question = question_data_manager.find_question(question_id)
    return render_template('new_answer.html', question=question, result=result, message=message)


@app.route('/accept-answer', methods=['POST', 'GET'])
def accept_answer():
    answer_id = request.form['a_id']
    question_id = request.form['q_id']
    answer_data_manager.accept_answer(a_id=answer_id)
    return redirect(url_for('show_question', question_id=question_id))


def create_answer(question_id, message, image):
    user_id=user_data_manager.get_user_id(username=session['username'])
    return {
        'submission_time': util.submission_time_generator(),
        'vote_number': 1,
        'question_id': question_id,
        'message': message,
        'image': image,
        'user_id': user_id['id'],
        'accepted': False
    }


@app.route('/question_page/<answer_id>/update')
def edit_answer(answer_id):
    result = answer_data_manager.find_answer(a_id=answer_id)
    return render_template('new_answer.html', result=result)


@app.route('/rewrite_answer', methods=['POST'])
def rewrite_answer():
    updated_answer = {
        'id': request.form.get('id'),
        'submission_time': request.form.get('submission_time'),
        'vote_number': request.form.get('vote_number'),
        'question_id': request.form.get('question_id'),
        'message': request.form.get('message'),
        'image': request.form.get('image'),
    }
    answer_data_manager.update_answer(datas=updated_answer)
    return show_question(updated_answer['question_id'])


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    result = []
    message = ""
    if request.method == 'POST':
        new_question = create_question(request.form['message'], request.form['image'], request.form['title'])
        question_data_manager.add_question(from_data=new_question)
        return redirect('/')
    return render_template('add_question.html', result=result, message=message)


def create_question(message, image, title):
    user_name = session['username']
    user_id = user_data_manager.get_user_id(username=user_name)
    return {
        'submission_time': util.submission_time_generator(),
        'vote_number': 1,
        'message': message,
        'title': title,
        'image': image,
        'view_number': 1,
        'user_id': user_id['id']
    }


@app.route('/question_page/<question_id>/comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    comment = 'question'
    if request.method == 'POST':
        user_name=session['username']
        user_id=user_data_manager.get_user_id(username=user_name)
        message = request.form['message']
        time = util.submission_time_generator()
        comment_data_manager.add_comment_to_question(q_id=question_id, comment_message=message, u_id=user_id['id'], s_time=time)

        return show_question(question_id)
    return render_template('add_comment.html', question_id=question_id, comment=comment)


@app.route('/question_page/<question_id>/<answer_id>/comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id, question_id):
    comment = 'answer'
    if request.method == 'POST':
        message = request.form['message']
        comment_data_manager.add_comment_to_answer(a_id=answer_id, comment_message=message)
        return show_question(question_id)
    return render_template('add_comment.html', answer_id=answer_id, question_id=question_id, comment=comment)


@app.route('/all-user')
def list_all_user():
    result = user_data_manager.select_all_user()
    return render_template('all_users.html', users=result)

@app.route('/user_page/<user_id>')
def show_user_page(user_id):
    questions_by_user=question_data_manager.get_all_quesrion_by_user(u_id=user_id)
    answers_by_user=answer_data_manager.get_all_answes_form_user(u_id=user_id)
    comments_by_user= comment_data_manager.get_all_comments_from_user(u_id=user_id)
    user_data = user_data_manager.get_user_data(u_id=user_id)
    return render_template('user_page.html', questions=questions_by_user, answers=answers_by_user, comments=comments_by_user, user_data=user_data)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
