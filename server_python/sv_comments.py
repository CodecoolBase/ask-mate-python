from server_python.config import app
from data_manager import dm_comments
from flask import request, redirect, render_template, session


@app.route('/question/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_question():
    question_id = request.args.get('question_id')
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = None
        dm_comments.add_comment_to_question(request.form, question_id, user_id)
        return redirect(f'/question_detail/{question_id}')
    return render_template('comment.html',
                           question_id=question_id,
                           is_add_comment_to_question=True)


@app.route('/answer/new-comment', methods=['GET', 'POST'])
def route_add_comment_to_answer():
    question_id = request.args.get('question_id')
    answer_id = request.args.get('answer_id')
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
        else:
            user_id = None
        dm_comments.add_comment_to_answer(request.form, answer_id, question_id, user_id)
        return redirect(f"/question_detail/{question_id}")
    return render_template('comment.html',
                           question_id=question_id,
                           answer_id=answer_id,
                           is_add_comment_to_answer=True)


@app.route('/comment/edit', methods=['GET', 'POST'])
def route_edit_comment():
    comment_id = request.args.get('comment_id')
    comment = dm_comments.get_comment_by_id(comment_id)
    if request.method == 'POST':
        question_id = dm_comments.update_comment_by_id(request.form, comment_id)
        return redirect(f"/question_detail/{question_id['question_id']}")
    return render_template('comment.html', comment=comment)


@app.route('/comment/delete', methods=['GET'])
def route_delete_comment():
    comment_id = request.args.get('comment_id')
    question_id = request.args.get('question_id')
    dm_comments.delete_comment_by_id(comment_id)
    return redirect(f"/question_detail/{question_id}")
