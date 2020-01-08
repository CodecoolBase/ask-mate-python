from flask import Flask, render_template, redirect, request, url_for
import data_handler
import database_manager
import os
from werkzeug.utils import secure_filename
from datetime import datetime
app = Flask(__name__)


@app.route('/')
@app.route('/lists')
def route_lists():
    try:
        order_by = request.args['order_by']
        order_direction = request.args['order_direction']
    except KeyError:
        order_by = 'submission_time'
        order_direction = 'asc'

    sorted_questions = database_manager.get_all_questions_sorted(order_by, order_direction)
    return render_template("lists.html", question=sorted_questions, order_by=order_by, order_direction=order_direction)


@app.route('/add_question', methods=['GET', 'POST'])
def route_new_question():
    if request.method == 'POST':
        new_question = {'submission_time': datetime.now(),
                        'title': request.form.get('title'),
                        'message': request.form.get('message'),
                        'view_number': request.form.get('view_number'),
                        'vote_number': request.form.get('vote_number'),
                        'image': request.form.get('image')}
        if request.files['image'].filename != "":

            image = request.files['image']
            if not data_handler.allowed_image(image.filename):
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(data_handler.IMAGE_UPLOAD_PATH, filename))
                new_question.update({'image': f"{data_handler.IMAGE_UPLOAD_PATH}/{image.filename}"})

        database_manager.add_question(new_question)
        return redirect('/lists')

    return render_template("add_question.html",
                           comment_name='Add new question',
                           form_url=url_for('route_new_question'),
                           comment_title='Question title',
                           comment_message='Question message',
                           type='question')


@app.route('/question/<question_id>')
def route_question(question_id):
    question = database_manager.get_question_by_id(question_id)
    answers = database_manager.get_all_answer_by_question_id(question_id)
    try:
        order_by = request.args['order_by']
        order_direction = request.args['order_direction']
    except:
        order_by = 'submission_time'
        order_direction = 'asc'
    sorted_answers = data_handler.sort_data(answers, order_by, order_direction)

    return render_template("answer.html",
                           question=question[0],
                           answer=sorted_answers,
                           order_by=order_by,
                           order_direction=order_direction,
                           positive=data_handler.POSITIVE)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        new_answer = {'message': request.form.get('message'),
                      'vote_number': request.form.get('vote_number'),
                      'image': request.form.get('image'),
                      'question_id': request.form.get('question_id')}
        if request.files['image'].filename != "":
            image = request.files['image']
            if not data_handler.allowed_image(image.filename):
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)

                image.save(os.path.join(data_handler.IMAGE_UPLOAD_PATH, filename))
                new_answer.update({'image': f"{data_handler.IMAGE_UPLOAD_PATH}/{image.filename}"})
        new_answer['submission_time'] = datetime.now()
        database_manager.add_answer(new_answer)
        return redirect(f'/question/{question_id}')

    return render_template("add_question.html",
                           type='answer',
                           comment_name='Add new answer',
                           form_url=url_for('route_new_answer', question_id=question_id),
                           comment_message='Answer message',
                           question_id=question_id,
                           timestamp=data_handler.date_time_in_timestamp())


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_handler.delete_image_by_id(question_id)
    database_manager.delete_question(question_id)
    return redirect('/lists')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = database_manager.get_answer_by_id(answer_id)[0]['question_id']
    data_handler.delete_image_by_id(answer_id)
    database_manager.delete_answer(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote_up')
def question_vote_up(question_id):
    database_manager.vote(question_id, type='question', positive=True)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote_down')
def question_vote_down(question_id):
    database_manager.vote(question_id, type='question', positive=False)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    question = database_manager.get_answer_by_id(answer_id)
    question_id = question[0]['question_id']
    database_manager.vote(answer_id, type='answer', positive=True)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    question = database_manager.get_answer_by_id(answer_id)
    question_id = question[0]['question_id']
    database_manager.vote(answer_id, type='answer', positive=False)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = database_manager.get_question_by_id(question_id)[0]
    if request.method == 'POST':
        datas_from_edit = ['title', 'message']
        for data in datas_from_edit:
            question[data] = request.form[data]
        database_manager.update_question(question, question_id)
        return redirect(url_for('route_question', question_id=question_id))

    return render_template('edit_question.html',
                           question=question,
                           from_url=url_for('edit_question', question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)[0]
    if request.method == 'POST':
        datas_from_edit = ['message']
        for data in datas_from_edit:
            answer[data] = request.form[data]
        database_manager.update_answer(answer, answer_id)
        return redirect(url_for('route_question', question_id=answer['question_id']))

    return render_template('edit_answer.html',
                           answer=answer,
                           from_url=url_for('edit_answer', answer_id=answer_id))

@app.route('/search')
def route_search():
    search_phrase = request.args.get('search')
    questions = database_manager.search_in_questions(search_phrase)
    answers = database_manager.search_in_answers(search_phrase)
    return render_template('Search.html',
                           question=questions,
                           answer=answers)

@app.route('/question/<question_id>/new_comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id):
    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['submission_time'] = datetime.now()
        database_manager.write_new_comment(new_comment)
        return redirect(f'/question/{question_id}')

    return render_template("new_comment.html",
                               comment_name='Add Comment',
                               form_url=url_for('add_new_comment_to_question', question_id=question_id),
                               comment_message='Add Comment',
                               question_id=question_id,)



if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        )
