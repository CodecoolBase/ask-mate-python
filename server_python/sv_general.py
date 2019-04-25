from server_python.config import app, photos
from data_manager import dm_general
from flask import request, redirect, render_template
from util import highlight_search_term
from flask import Markup


@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        question_id = request.args.get('question_id', type=str)
        answer_id = request.args.get('answer_id', type=str)
        try:
            filename = photos.save(request.files['photo'])
        except Exception:
            return redirect('/question_detail/' + question_id)

        id = answer_id if answer_id else question_id
        table = "answer" if answer_id else "question"

        dm_general.update_image_path(table, filename, id)
        return redirect('/question_detail/' + question_id)


@app.route('/search')
def route_search():
    search_term = request.args.get('search_term')
    searched_questions, searched_answers = dm_general.search_results(search_term)
    questions_count = len(searched_questions)
    highlight_search_term_fn = lambda sequence: highlight_search_term(search_term, sequence)
    return render_template('search_results.html',
                           searched_questions=searched_questions,
                           searched_answers=searched_answers,
                           questions_count=questions_count,
                           highlight_search_term_fn=highlight_search_term_fn,
                           markup=Markup)

