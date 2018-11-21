from flask import Flask , render_template, redirect, url_for, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def show_list():
    questions = data_manager.get_all_questions()
    questions.sort(reverse=True, key=lambda question: question["submission_time"])
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def show_question(question_id, is_new_answer=False):
    question = data_manager.get_question_by_id(question_id)
    answers_for_question = data_manager.get_answers_for_question(question_id)

    return render_template('maintain-question.html',
                           question=question,
                           answers_for_question=answers_for_question,
                           is_new_answer=is_new_answer)


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def add_new_answer(question_id):
    if request.method == "GET":
        return show_question(question_id, is_new_answer=True)
    elif request.method == "POST":
        data_manager.save_new_answer(request.form.to_dict(), question_id)
        return redirect(url_for("show_question", question_id=question_id))



@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    '''GET: Renders the form for the question
    POST: Adds a new question to the database'''
    if request.method == 'GET':
        return render_template('add-question.html', question={})
    elif request.method == 'POST':
        question_id = data_manager.save_new_question(request.form.to_dict())

        return redirect(url_for('show_question', question_id=question_id))


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id, convert_stamp=False)

    if request.method == "GET":

        return render_template('add-question.html', question=question)
    elif request.method == 'POST':
        updated_details = request.form.to_dict()

        updated_question = {}
        for key in question.keys():
            updated_question[key] = updated_details[key] if key in updated_details else question[key]

        data_manager.update_question(updated_question)

        return redirect(url_for('show_question', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )