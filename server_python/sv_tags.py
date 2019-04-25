from server_python.config import app
from data_manager import dm_tags
from flask import request, redirect, render_template


@app.route('/question/new-tag', methods=['GET', 'POST'])
def route_add_tag():
    question_id = request.args.get('question_id')
    options = dm_tags.get_tags(question_id)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('new_tag'):
            new_tag = request.form.get('new_tag')
            dm_tags.add_new_tag(new_tag)
        dm_tags.add_tags_to_question(request.form, question_id)
        return redirect(f'/question_detail/{question_id}')
    return render_template('tag.html', options=options, question_id=question_id)


@app.route('/question_detail/<question_id>/tag/<tag_id>/delete', methods=['GET'])
def route_delete_tag(question_id, tag_id):
    dm_tags.delete_tag_from_question(question_id, tag_id)
    return redirect(f'/question_detail/{question_id}')


@app.route('/tags', methods=['GET'])
def route_show_tags():
    tags = dm_tags.get_tags_and_count()
    return render_template('tag.html', tags=tags)
