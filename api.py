""" 
API para trabalho de Engenharia de Software 2

Autores: 
	Henrique Eustaquio Lopes Ferreira 2015068990
	Tiago Melo Tannus 

Implementado com:
	Flask 1.0.2
	Python 2.7.10 (default, Jul 15 2017, 17:16:57)
	[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)]
"""

from flask import Flask, jsonify, abort, make_response, request
import os

app = Flask(__name__)

tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
		'done': False 
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web',
		'done': False 
	}
]

# Numero de publicacoes em uma determinada conferencia de uma area
@app.route("/api/1")
def get_publi_conf_area():
	conf = request.args.get('conf')
   	area = request.args.get('area')

   	if len(conf)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		for filename in files:
   			if filename == (area + "-out-confs.csv"):
   				file = filename

   	data = open(file_path + file, "r")

   	correct = ""
   	for line in data.readlines():
		if line.find(conf) != -1:
 			correct = line
   	
   	return correct[correct.find(",")+1:len(correct)-1]

# Numero de publicacoes no conjunto de conferencias de uma area
@app.route("/api/2")
def get_publi_area():
	area = request.args.get('area')

   	if len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		for filename in files:
   			if filename == (area + "-out-confs.csv"):
   				file = filename

   	data = open(file_path + file, "r")

   	n = 0
   	for line in data.readlines():
		n += int(line[line.find(",")+1:len(line)-1])
   	
   	return str(n)

# Scores de todos os departamentos em uma area
@app.route("/api/3")
def get_score_area():
	area = request.args.get('area')

   	if len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		for filename in files:
   			if filename == (area + "-out-scores.csv"):
   				file = filename

   	data = open(file_path + file, "r")

   	n = 0
   	for line in data.readlines():
		n += float(line[line.find(",")+1:len(line)-1])
   	
   	return str(n)

# Numero de publicacoes em uma determinada conferencia de uma area
@app.route("/api/4")
def get_publi_dep_area():
	dep = request.args.get('dep')
   	area = request.args.get('area')

   	if len(dep)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		for filename in files:
   			if filename == (area + "-out-scores.csv"):
   				file = filename

   	data = open(file_path + file, "r")

   	for line in data.readlines():
		if line.find(dep) != -1:
 			correct = line
   	
   	return correct[correct.find(",")+1:len(correct)-1]



@app.route("/todo/api/v1.0/tasks", methods=['GET'])
def get_tasks():
	return jsonify({'tasks': tasks})

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/todo/api/v1.0/tasks", methods=['POST'])
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
	return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
    
if __name__ == '__main__':
	app.run(debug=True)