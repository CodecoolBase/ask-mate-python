from server_python.config import app
from data_manager import dm_general, dm_answers
from flask import redirect, request, render_template, jsonify


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
        dm_answers.add_sql_answer(request.form, question_id)
        return redirect('/question_detail/' + question_id)
    return render_template('answer.html', question_id=question_id)


@app.route('/answer/<answer_id>/vote-down/<question_id>')
def answer_vote_down(answer_id, question_id):
    dm_general.change_vote("answer", answer_id, -1)
    return redirect('/question_detail/' + question_id)


@app.route('/answer/<answer_id>/vote-up/<question_id>')
def answer_vote_up(answer_id, question_id):
    dm_general.change_vote("answer", answer_id, 1)
    return redirect('/question_detail/' + question_id)


@app.route('/answer/<answer_id>/vote', methods=['PUT'])
def answer_change_vote(answer_id):
    value_to_change_vote = request.get_json()['voteValue']
    new_vote_value = dm_answers.change_answer_vote(answer_id, value_to_change_vote)
    return jsonify(new_vote_value)