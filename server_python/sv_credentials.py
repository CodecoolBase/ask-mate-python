from server_python.config import app
from flask import flash, render_template, session, redirect
from Forms import forms
from data_manager import dm_credentials
from server_python import config


@app.route('/register', methods=['GET', 'POST'])
def register():
    form_data = forms.RegistrationForm()
    if form_data.validate_on_submit():
        hashed_password = config.bcrypt.generate_password_hash(form_data.password.data).decode('utf-8')
        dm_credentials.register_user(form_data, hashed_password)
        flash(f'Account created for {form_data.name.data}!', 'success')
        return redirect('/')
    return render_template('register.html', form=form_data, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user_data = dm_credentials.get_user_data(form.email.data)
        is_user_email = bool(user_data['email'])
        hashed_password = user_data['password']
        is_valid_password = config.bcrypt.check_password_hash(hashed_password, form.password.data)
        if is_user_email and is_valid_password:
            user_id = user_data['id']
            session['user_id'] = user_id
            flash('You logged in!', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials!', 'danger')
            return redirect('/login')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    flash('You\'ve logged out!', 'success')
    session.pop('user_id', None)
    return redirect('/')

