import os
from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import data_manager
import connection
import util

UPLOAD_FOLDER = '/home/iulian/PycharmProjects/ask-mate-python/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

LAST_VISITED_QUESTION = 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['GET', 'POST'])
def route_list():
    if request.method == 'GET':
        sort_by = request.args.get(key='order_by')
        order_direction = request.args.get(key='order_direction')
        if sort_by == 'submission time' and order_direction == 'desc':
            questions = data_manager.sort_questions('submission_time', True)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'submission time' and order_direction == 'asc':
            questions = data_manager.sort_questions('submission_time', False)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'title' and order_direction == 'desc':
            questions = data_manager.sort_questions('title', True)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'title' and order_direction == 'asc':
            questions = data_manager.sort_questions('title', False)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'message' and order_direction == 'desc':
            questions = data_manager.sort_questions('message', True)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'message' and order_direction == 'asc':
            questions = data_manager.sort_questions('message', False)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'view number' and order_direction == 'desc':
            questions = data_manager.sort_questions('view_number', True)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'view number' and order_direction == 'asc':
            questions = data_manager.sort_questions('view_number', False)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'vote number' and order_direction == 'desc':
            questions = data_manager.sort_questions('vote_number', True)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        elif sort_by == 'vote number' and order_direction == 'asc':
            questions = data_manager.sort_questions('vote_number', False)
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
        else:
            questions = data_manager.get_data()
            return render_template('list.html',
                                   category=sort_by,
                                   questions=questions)
    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_question = {"id": util.generate_question_id(),
                        "submission_time": data_manager.create_time(),
                        "view_number": 0,
                        "vote_number": 0,
                        'title': request.form['title'],
                        'message': request.form['message'],
                        'image': UPLOAD_FOLDER + '/' + filename if file.filename else ''}
        data_manager.add_question_table(new_question)
        questions = data_manager.get_data()
        return render_template('/list.html',
                               questions=questions)


@app.route('/question/<question_id>/new-answer', methods=['GET'])
def new_answer(question_id):
    return render_template('new-answer.html',
                           question_id=question_id)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_question(question_id):
    global LAST_VISITED_QUESTION
    if request.method == 'GET':
        question = data_manager.get_question(question_id)
        answers = data_manager.get_answers(question_id)
        LAST_VISITED_QUESTION = question_id
        return render_template('question.html',
                               question=question,
                               answers=answers,
                               question_id=question_id)
    elif request.method == 'POST':
        data_manager.add_answer_to_file(request.form['post_answer'], question_id)
        question = data_manager.get_question(question_id)
        answers = data_manager.get_answers(question_id)
        LAST_VISITED_QUESTION = question_id
        return render_template('question.html',
                               question=question,
                               answers=answers,
                               question_id=question_id)


@app.route('/answer/<answer_id>/delete', methods=['GET'])
def delete_answer(answer_id):
    answers = connection.read_answers()
    i = 0
    while i < len(answers):
        if answers[i]['id'] == answer_id:
            question_id = answers[i]['question_id']
            answers.pop(i)
        i += 1
    connection.write_answers(answers)
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers(question_id)
    return render_template('question.html',
                           question=question,
                           answers=answers,
                           question_id=question_id)


@app.route('/add-question')
def add_question():
    return render_template('/add-question.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)

