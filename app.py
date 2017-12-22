#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

#authentication extension written by Miguel Grinberg
auth = HTTPBasicAuth()

@auth.get_password
def get_login(username):
    if username == 'admin':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

#Task list
tasks = [
    {
        'id': 1,
        'title': u'Open door',
        'description': u'Task for opening the door',
        'done': False
    },
    {
        'id': 2,
        'title': u'Close door',
        'description': u'Task for closing the door',
        'done': False
    }
]

#Display task URI in get_task, create_task, update_task and delete_task
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

#show all tasks
@app.route('/door/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

#show individual task based on id
@app.route('/door/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

#Add task
@app.route('/door/api/tasks', methods=['POST'])
@auth.login_required #Add this above the functions to require authentication
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': [make_public_task(task) for task in tasks]}), 201

#Update task
@app.route('/door/api/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        aboort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': [make_public_task(task) for task in tasks]})

#Delete task
@app.route('/door/api/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

#error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#boilerplate
if __name__ == '__main__':
    app.run(debug=False)
