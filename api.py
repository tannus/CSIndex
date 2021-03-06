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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

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
	dept = request.args.get('dept')
   	area = request.args.get('area')

   	if len(dep)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		for filename in files:
   			if filename == (area + "-out-scores.csv"):
   				file = filename

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

   	correct = ""
   	for line in data.readlines():
		if line.find(dept) != -1:
 			correct = line
	
	out = open(file_path + area + "-dept-scores.csv", "w")
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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

   	out = open(file_path + area + "-all-papers.csv", "w")

   	year = ""
   	title = ""
   	dept = ""
   	authors = ""
   	for line in reader(data):
   		year = line[0]
   		title = line[2]
   		dept = line[3]
		authors = line[4]
   		out.write(year + "," + title + "," + dept + "," + authors + "\n")	
   	
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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

   	out = open(file_path + area + "-all-papers-year.csv", "w")

   	xyear = ""
   	title = ""
   	dept = ""
   	authors = ""
   	writer = csv.writer(out, delimiter=",")
   	for line in reader(data):
   		xyear = line[0]
   		if xyear == year:
   			title = line[2]
   			dept = line[3]
			authors = line[4]
			if isinstance(title, str):
				title = unicode(title, "utf-8")
			if isinstance(dept, str):
				dept = unicode(dept, "utf-8")
			if isinstance(authors, str):
				authors = unicode(authors, "utf-8")
   			writer.writerow([year.encode("utf-8"),title.encode("utf-8"),dept.encode("utf-8"),authors.encode("utf-8")])
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

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

   	out = open(file_path + area + "-all-papers-dept.csv", "w")

   	xdept = ""
   	title = ""
   	dept = ""
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
			if isinstance(dept, str):
				dept = unicode(dept, "utf-8")
			if isinstance(authors, str):
				authors = unicode(authors, "utf-8")
   			writer.writerow([year.encode("utf-8"),title.encode("utf-8"),dept.encode("utf-8"),authors.encode("utf-8")])
   	return str(1)

#10 - Todos os papers de um professor (dado o seu nome)
@app.route("/api/10")
def get_papers_area_prof():
	area = request.args.get('area')
	prof = request.args.get('prof')

   	if len(prof)==0 or len(area)==0:
   		abort(404)
   	
   	file = ""
   	file_path = "data/"

   	for root, dirs, files in os.walk("data"):
   		if dirs != "profs":
	   		for filename in files:
	   			if filename == (area + "-out-papers.csv"):
	   				file = filename

   	data = ""
   	try:
   		data = open(file_path + file, "r")
   	except:
   		abort(404)

   	out = open(file_path + area + "-all-papers-prof.csv", "w")

   	dept = ""
   	title = ""
   	authors = ""
   	writer = csv.writer(out, delimiter=",")
   	for line in reader(data):
   		authors = line[4]
   		if isinstance(authors, str):
			authors = unicode(authors, "utf-8")
   		if authors.find(prof) != -1:
   			year = line[0]
   			title = line[2]
			dept = line[3]	
			if isinstance(title, str):
				title = unicode(title, "utf-8")
			if isinstance(dept, str):
				dept = unicode(dept, "utf-8")
   			writer.writerow([year.encode("utf-8"),title.encode("utf-8"),dept.encode("utf-8"),authors.encode("utf-8")])
   	return prof

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == '__main__':
	app.run(debug=True)