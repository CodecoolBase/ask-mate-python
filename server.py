from flask import Flask, render_template, redirect, url_for, request
import connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    stored_questions = connection.formatted_file()
    return render_template('list.html', questions=stored_questions)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )