from flask import Flask, render_template, redirect, url_for, request
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    stored_questions = data_manager.format_file()
    return render_template('list.html', questions=stored_questions)

@app.route('/question/<question_id>')
def route_question_id():

    return render_template('questiondetails.html')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )