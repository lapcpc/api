import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, db, initialize_app

#Inicializar nuestra app Flask
app = Flask(__name__)
#Establecemos conexion con firebase database
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://to-do-list-fb0a9-default-rtdb.firebaseio.com/'
})

ref = db.reference('tasks')
#READ
@app.route('/list', methods=['GET'])
def read():
    try:
        task_id = request.args.get('id')
        if task_id:
            task = ref.child(task_id)
            return jsonify(task.get()), 200
        else:
            tasks = ref.get()
            return jsonify(tasks), 200
    except Exception as e:
        return f"Ocurrio el siguiente error: {e}"

#CREATE
@app.route('/add', methods=['POST'])
def create():
    try:
        id = request.json['id']
        task = {
            'id': id,
            'name': request.json['name'],
            'check': False
        }
        ref.child(id).set(task)
        return jsonify({"sucess": True}), 200
    except Exception as e:
        return f"Ocurrio el siguiente error: {e}"

#UPDATE
@app.route('/update', methods=['PUT'])
def update():
    try:
        id = request.json['id']
        ref.child(id).update(request.json)
        return jsonify({"sucess": True}), 200
    except Exception as e:
        return f"Ocurrio el siguiente error: {e}"

#DELETE
@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        task_id = request.args.get('id')
        ref.child(task_id).delete()
        return jsonify({"sucess": True}), 200
    except Exception as e:
        return f"Ocurrio el siguiente error: {e}"

port = int(os.environ.get('PORT', 8000))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
