from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from __init__ import create_app, db
from models import ToDoList

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])  # home page that return 'index'
def index():
    if request.method == 'POST':
        if current_user.is_authenticated:
            new_to_do_list = ToDoList(todo=request.form['projectFilepath'], is_done=False, user_id=current_user.name)
            db.session.add(new_to_do_list)
            db.session.commit()
            return redirect(url_for('main.index'))

    if request.method == 'GET':
        if current_user.is_authenticated:
            all_todos = ToDoList.query.filter_by(user_id=current_user.name).all()
            return render_template('index.html', user=current_user.name, all_todos=all_todos)
        else:
            return render_template('index.html')


@main.route('/profile')  # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/delete/<delete_id>', methods=['GET'])  # home page that return 'index'
def delete(delete_id):
    todo_to_delete = ToDoList.query.get(delete_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/update/<update_id>', methods=['GET'])  # home page that return 'index'
def update(update_id):
    todo_to_update = ToDoList.query.get(update_id)
    if todo_to_update.is_done:
        todo_to_update.is_done = False
    else:
        todo_to_update.is_done = True
    db.session.commit()
    return redirect(url_for('main.index'))


app = create_app()  # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app())  # create the SQLite database
    app.run(debug=True)  # run the flask app on debug mode
