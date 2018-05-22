""" 
API para trabalho de Engenharia de Software 2

Autores: 
	Henrique Eustaquio Lopes Ferreira 2015068990
	Tiago Melo Tannus 2012079762

Implementado com:
	Flask 1.0.2
	Python 2.7.10 (default, Jul 15 2017, 17:16:57)
	[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)]
"""

import os
import re
from flask import Flask, jsonify, abort, make_response, request
from tokenize import generate_tokens
from collections import defaultdict
import csv
from csv import reader
import sys

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

#1 - Numero de publicacoes em uma determinada conferencia de uma area
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

 	ans = correct[correct.find(",")+1:len(correct)-1]
 	
 	out = open(file_path + area + "-publi-conf.csv", "w")
 	out.write(ans)

   	return ans

#2 - Numero de publicacoes no conjunto de conferencias de uma area
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
   	
   	out = open(file_path + area + "-publi.csv", "w")
 	out.write(str(n))

   	return str(n)

#3 - Scores de todos os departamentos em uma area
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

   	out = open(file_path + area + "-dep-scores.csv", "w")

   	n = 0
   	for line in data.readlines():
   		out.write(line)
		n += float(line[line.find(",")+1:len(line)-1])
   	
 	out.write("TOTAL," + str(n))

   	return str(n)

#4 - Score de um determinado departamento em uma area
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

   	correct = ""
   	for line in data.readlines():
		if line.find(dep) != -1:
 			correct = line
	
	out = open(file_path + area + "-dep-scores.csv", "w")
	out.write(correct)

   	return correct

#5 - Numero de professores que publicam em uma determinada area (organizados por departamentos)
@app.route("/api/5")
def get_prof_dep_area():
	area = request.args.get('area')

   	if len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = open(file_path + file, "r")

   	n = 0
   	dep = ""
   	tok_line = []
   	ans = defaultdict(int)
   	for line in data.readlines():
   		tok_line = line.split(",")
   		dep = tok_line[3]
		ans[dep] += 1
   	
   	out = open(file_path + area + "-prof-dep-publi.csv", "w")

   	for key,val in ans.items():
   		out.write(str(key) + ",")
   		out.write(str(val) + "\n")
   		n += val
   	
   	out.write("TOTAL," + str(n))
   	return str(n)

#6 - Numero de professores de um determinado departamento que publicam em uma area
@app.route("/api/6")
def get_prof_sdep_area():
	area = request.args.get('area')
	dep = request.args.get('dep')

   	if len(dep)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = open(file_path + file, "r")

   	n = 0
   	dep = ""
   	tok_line = []
   	ans = defaultdict(int)
   	for line in data.readlines():
   		tok_line = line.split(",")
   		dep = tok_line[3]
		ans[dep] += 1
   	
   	out = open(file_path + area + "-prof-sdep-publi.csv", "w")

   	for key,val in ans.items():
   		if key == dep:
   			out.write(str(key) + ",")
   			out.write(str(val) + "\n")
   		n += val
   	
   	out.write("TOTAL," + str(n))
   	return str(n)

#7 - Todos os papers de uma area (ano, titulo, deptos e autores)
@app.route("/api/7")
def get_papers_area():
	area = request.args.get('area')
	
   	if len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = open(file_path + file, "r")

   	out = open(file_path + area + "-all-papers.csv", "w")

   	year = ""
   	title = ""
   	depts = ""
   	authors = ""
   	for line in reader(data):
   		year = line[0]
   		title = line[2]
   		depts = line[3]
		authors = line[4]
   		out.write(year + "," + title + "," + depts + "," + authors + "\n")	
   	
   	return str(1)

#8 - Todos os papers de uma area em um determinado ano
@app.route("/api/8")
def get_papers_area_year():
	area = request.args.get('area')
	year = request.args.get('year')

   	if len(year)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = open(file_path + file, "r")

   	out = open(file_path + area + "-all-papers-year.csv", "w")

   	xyear = ""
   	title = ""
   	depts = ""
   	authors = ""
   	writer = csv.writer(out, delimiter=",")
   	for line in reader(data):
   		xyear = line[0]
   		if xyear == year:
   			title = line[2]
   			depts = line[3]
			authors = line[4]
			if isinstance(title, str):
				title = unicode(title, "utf-8")
			if isinstance(depts, str):
				depts = unicode(depts, "utf-8")
			if isinstance(authors, str):
				authors = unicode(authors, "utf-8")
   			writer.writerow([year.encode("utf-8"),title.encode("utf-8"),depts.encode("utf-8"),authors.encode("utf-8")])
   	return str(1)

#9 - Todos os papers de um departamento em uma area
@app.route("/api/9")
def get_papers_area_dept():
	area = request.args.get('area')
	dept = request.args.get('dept')

   	if len(dept)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = open(file_path + file, "r")

   	out = open(file_path + area + "-all-papers-dept.csv", "w")

   	xdept = ""
   	title = ""
   	depts = ""
   	authors = ""
   	writer = csv.writer(out, delimiter=",")
   	for line in reader(data):
   		xdept = line[3]
   		if xdept == dept:
   			year = line[0]
   			title = line[2]
			authors = line[4]
			if isinstance(title, str):
				title = unicode(title, "utf-8")
			if isinstance(depts, str):
				depts = unicode(depts, "utf-8")
			if isinstance(authors, str):
				authors = unicode(authors, "utf-8")
   			writer.writerow([year.encode("utf-8"),title.encode("utf-8"),depts.encode("utf-8"),authors.encode("utf-8")])
   	return str(1)

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