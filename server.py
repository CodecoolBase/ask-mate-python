from flask import Flask, render_template, redirect, url_for, request
import data_manager

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    stored_questions = data_manager.format_file()
    return render_template('list.html', questions=stored_questions, title="Welcome!")


@app.route('/new-answer', methods=['GET', 'POST'])
def add_new_answer():
    return render_template('answer.html', title="Add New Answer!")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )