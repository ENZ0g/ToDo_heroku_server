import os
import bottle
from truckpad.bottle.cors import CorsPlugin, enable_cors
import todos_db as db


session = db.create_session()

app = bottle.Bottle()


@enable_cors
@app.route('/api/tasks')
def index():
    tasks = [db.task_to_dict(task) for task in db.get_all_tasks(session)]
    return {'tasks': sorted(tasks, key=lambda x: x['uid']),
            'total': len(tasks),
            'not_completed': db.get_not_completed_tasks(session)}


@enable_cors
@app.route('/api/tasks/<uid:int>', method=['PUT', 'DELETE'])
def change_task(uid):
    try:
        if bottle.request.method == 'DELETE':
            db.delete_task(session, uid)
            return 'The task is deleted successfully'
        elif bottle.request.method == 'PUT':
            db.make_task_completed(session, uid)
            return 'The task is completed successfully'
    except IndexError:
        return bottle.HTTPError(404, f'No task with uid {uid}')


@enable_cors
@app.route('/api/add-task', method='POST')
def add_task():
    description = bottle.request.json['description'].strip()
    if len(description) > 0:
        db.add_task(session, description)
    return 'The task is added successfully'


app.install(CorsPlugin(origins=os.environ.get('CORS_URLS')))

if os.environ.get('APP_LOCATION') == 'heroku':
    bottle.run(app,
               host="0.0.0.0",
               port=int(os.environ.get("PORT", 5000)))
else:
    bottle.run(app,
               host='localhost',
               port=5000)
