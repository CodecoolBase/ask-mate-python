
from flask import Flask, render_template, request

import data_handler

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        reqv = request.form.to_dict()
        if reqv["question_id"] == '':
            asd = data_handler.generate_question_dict(reqv)
        elif reqv["question_id"] != '':
            asd = data_handler.generate_answer_dict(reqv)
        app.logger.info(asd)
        return render_template('test.html', d=asd)
    return render_template('add-question.html')


if __name__ == '__main__':
    app.run(debug=True)
