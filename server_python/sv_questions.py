from server_python.config import app
from data_manager import dm_questions, dm_answers, dm_comments, dm_tags
from flask import request, redirect, render_template, jsonify, session
from util import check_referer_url, truncate_question


@app.route('/')
def route_home():
    questions = dm_questions.get_5_questions_sql_sorted_by_submission_time()
    return render_template('index.html', questions=questions, truncate_fn=truncate_question)


@app.route('/list')
def route_list():
    questions = dm_questions.get_all_questions_sql_sorted_by_submission_time()
    return render_template('list.html', questions=questions, truncate_fn=truncate_question)


@app.route('/sort')
def route_sort_questions():
    feature_to_order_by = request.args.get('order_by', default='title', type=str)
    # todo > everywhere we receive user input - even in URL - make checks if parameters exist
    # if feature_to_order_by not in ['title', 'message']:
    #     return 'Error: wrong parameter'
    order_direction = request.args.get('order_direction', default='asc', type=str)
    questions = dm_questions.get_questions_sorted(feature_to_order_by, order_direction)
    return render_template('list.html',
                           questions=questions,
                           truncate_fn=truncate_question)


@app.route('/add', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = None
        dm_questions.add_question_sql(request.form, user_id)
        return redirect('/list')
    return render_template('form.html')


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    dm_questions.delete_question(question_id)
    return redirect('/list')


@app.route('/question_detail/<id>')
def route_question_detail(id):
    is_different_referer = check_referer_url(id)
    if is_different_referer:
        dm_questions.update_question_view_increase_count(id)
    question = dm_questions.get_question_sql_by_id(id)
    answers = dm_answers.get_all_sql_answers_by_question_id(id)
    question_comments = dm_comments.show_question_comments_by_id(id)
    answer_comments = dm_comments.show_answer_comments_by_id(id)
    tags = dm_tags.get_tags_of_question_by_id(id)
    return render_template('qd.html', question=question,
                           id=id, answers=answers,
                           count=len(answers),
                           question_comments=question_comments,
                           answer_comments=answer_comments,
                           tags=tags)


@app.route('/question_detail/edit', methods=['GET', 'POST'])
def route_question_edit():
    question_id = request.args.get('question_id')
    question = dm_questions.get_question_sql_by_id(question_id)
    if request.method == 'POST':
        dm_questions.update_question_sql(question_id, request.form)
        return redirect('/question_detail/' + question_id)
    return render_template('form.html', question=question)


@app.route('/question/<question_id>/vote', methods=['PUT'])
def question_change_vote(question_id):
    value_to_change_vote = request.get_json()['voteValue']
    new_vote_value = dm_questions.change_question_vote(question_id, value_to_change_vote)
    return jsonify(new_vote_value)


