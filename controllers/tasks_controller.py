from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import task_repository, user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks", __name__)

@tasks_blueprint.route("/tasks")
def tasks():
    tasks = task_repository.select_all()
    return render_template("tasks/index.html", all_tasks=tasks)

#NEW
# GET 'tasks/new'
@tasks_blueprint.route("/tasks/new")
def new_task():
    users = user_repository.select_all()
    return render_template("tasks/new.html", all_users=users)
    # "I'm the new route" (test)

# CREATE
# POST '/tasks'
@tasks_blueprint.route("/tasks", methods =["POST"])
def create_task():
    description = request.form["description"]
    duration = request.form["duration"]
    completed = request.form["completed"]
    user_id = request.form["user_id"]
    user = user_repository.select(user_id)
    new_task = Task(description, user, duration, completed)
    task_repository.save(new_task)
    return redirect("/tasks")


# SHOW
# GET '/tasks/<id>'
@tasks_blueprint.route("/tasks/<id>", methods=['GET'])
def show_task(id):
    task = task_repository.select(id)
    return render_template('tasks/show.html', task = task)

@tasks_blueprint.route("/tasks/<id>/edit", methods=['GET'])
def edit_task(id):
    task = task_repository.select(id)
    users= user_repository.select_all()
    return render_template('tasks/edit.html', task = task, all_users = users)

@tasks_blueprint.route("/tasks/<id>", methods=['POST'])
def update_task(id):
    description = request.form['description']
    user_id     = request.form['user_id']
    duration    = request.form['duration']
    completed   = request.form['completed']
    user        = user_repository.select(user_id)
    task        = Task(description, user, duration, completed, id)
    task_repository.update(task)
    return redirect('/tasks')

@tasks_blueprint.route("/tasks/<id>/delete", methods =["POST"])
def delete_task(id):
    task_repository.delete(id)
    return redirect("/tasks")