from flask import Flask, render_template, redirect, url_for, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    stored_questions = data_manager.get_questions()
    return render_template('list.html', questions=stored_questions, title="Welcome!")


@app.route('/question/<int:question_id>')
def route_question_id(question_id):
    stored_questions = data_manager.get_questions()
    stored_answers = data_manager.get_answers()
    return render_template('questiondetails.html', questions=stored_questions, answers=stored_answers, id=question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == "POST":
        data_manager.add_answer(question_id, request.form["answer"])
        return redirect(url_for('route_question_id', question_id=question_id))

    return render_template('answer.html', title="Add New Answer!", question_id=question_id)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        user_story_id = data_manager.add_question(request.form["question-title"], request.form["new-question"])
        return redirect(url_for('route_question_id',  question_id=user_story_id))

    return render_template("newquestion.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
