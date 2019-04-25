from server_python.config import app
from data_manager import dm_general, dm_answers, dm_questions, dm_users
from flask import redirect, request, render_template, jsonify, session


@app.route('/answer/delete')
def route_delete_answer():
    answer_id = request.args.get('answer_id')
    question_id = request.args.get('question_id')
    dm_answers.delete_answer(answer_id)
    return redirect('/question_detail/' + question_id)


@app.route('/answer/edit', methods=['GET', 'POST'])
def route_edit_answer():
    answer_id = request.args.get('answer_id')
    question_id = request.args.get('question_id')
    answer = dm_answers.qet_answer_by_id(answer_id)
    if request.method == 'POST':
        dm_answers.update_answer(answer_id, request.form)
        return redirect('/question_detail/' + question_id)
    return render_template('answer.html', answer=answer, question_id=question_id)


@app.route('/question/new-answer', methods=['GET', 'POST'])
def route_new_answer():
    question_id = request.args.get('question_id')
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = None
        dm_answers.add_sql_answer(request.form, question_id, user_id)
        return redirect('/question_detail/' + question_id)
    return render_template('answer.html', question_id=question_id)


@app.route('/answer/<answer_id>/accept/<question_id>')
def answer_accept(answer_id, question_id):
    if 'user_id' in session:
        if session['user_id'] == dm_questions.qet_users_id_by_question_id(question_id):
            dm_answers.accept_answer(answer_id, 1)
            reputation_value = 15
            users_id = dm_answers.qet_users_id_by_answer_id(answer_id)
            if users_id:
                dm_users.update_user_reputation(users_id, reputation_value)
    return redirect('/question_detail/' + question_id)


@app.route('/answer/<answer_id>/unaccept/<question_id>')
def answer_unaccept(answer_id, question_id):
    if 'user_id' in session:
        if session['user_id'] == dm_questions.qet_users_id_by_question_id(question_id):
            dm_answers.accept_answer(answer_id, 0)
    return redirect('/question_detail/' + question_id)


@app.route('/answer/<answer_id>/vote', methods=['PUT'])
def answer_change_vote(answer_id):
    value_to_change_vote = request.get_json()['voteValue']
    new_vote_value = dm_answers.change_answer_vote(answer_id, value_to_change_vote)
    if value_to_change_vote > 0:
        reputation_value = 10
    else:
        reputation_value = -2
    users_id = dm_answers.qet_users_id_by_answer_id(answer_id)
    if users_id:
        dm_users.update_user_reputation(users_id, reputation_value)
    return jsonify(new_vote_value)
