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


@app.route("/search")
def search():
    searched_word = request.args.get('q').lower()
    if searched_word is not None:
        questions = data_manager.search_in(searched_word)
        updated_questions = []
        for question in questions:
            if question not in updated_questions:
                updated_questions.append(question)
        print(updated_questions)

        return render_template('search.html', searched_word=searched_word, questions=updated_questions)
    return redirect(url_for('route_list'))


@app.route("/question/<int:question_id>/vote-up", methods=['GET', 'POST'])
def vote_up_question(question_id):
    if request.method == 'POST':
        data_manager.vote_up_question(question_id)
        return redirect(url_for('route_question_id', question_id=question_id))


@app.route("/question/<int:question_id>/vote-down", methods=['GET', 'POST'])
def vote_down_question(question_id):
    if request.method == 'POST':
        data_manager.vote_down_question(question_id)
        return redirect(url_for('route_question_id', question_id=question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-up", methods=['GET', 'POST'])
def vote_up_answer(question_id, answer_id):
    if request.method == 'POST':
        data_manager.vote_up_answer(question_id, answer_id)
        return redirect(url_for('route_question_id', question_id=question_id))


@app.route("/question/<int:question_id>/<int:answer_id>/vote-down", methods=['GET', 'POST'])
def vote_down_answer(question_id, answer_id):
    if request.method == 'POST':
        data_manager.vote_down_answer(question_id, answer_id)
        return redirect(url_for('route_question_id', question_id=question_id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
