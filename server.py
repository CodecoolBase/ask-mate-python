from flask import Flask, render_template, redirect, url_for, request
import data_manager
import connection
import time


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    stored_questions = data_manager.format_file()
    return render_template('list.html', questions=stored_questions)


@app.route('/question/<question_id>')
def route_question_id(question_id):
    stored_questions = data_manager.format_file()
    return render_template('questiondetails.html', questions=stored_questions, id=question_id)



@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        user_story = {
            'id': data_manager.generate_new_id('sample_data/question.csv'),
            'submission': int(time.time()),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form["QuestionTitle"],
            'message': request.form["NewQuestion"],
            'image': ""
        }
        fieldnames = ['id', 'submission', 'view_number', 'vote_number', 'title', 'message', 'image']
        connection.write_to_file('sample_data/question.csv', user_story, fieldnames)
        return redirect("url_for(route_question_id,  question_id=user_story['id'])")

    return render_template("newquestion.html")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
