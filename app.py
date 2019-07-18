from flask import Flask, request, redirect, Response, render_template, url_for, session, flash
from flask_restful import Api

import matplotlib.pyplot as plt
import base64
import sqlite3

import json, datetime

# .\venv\Scripts\activate.bat

app = Flask(__name__)
app.secret_key = 'miaomiao'

# @app.route('/home/')
# def home():
# 	return render_template('front.html')

@app.route('/')
def output():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def foo():
	zipCode = request.form['zipCode']
	# item = Item.find_by_name(first, last, email, topic, institution)
	# if item:
	# 	return render_template("info.html", message=item, count=len(item))
	# return render_template('index.html')
	barChart()
	data_uri = base64.b64encode(open('barChart.png', 'rb').read()).decode('utf-8')
	bar = 'data:image/png;base64,{0}'.format(data_uri)

	pieChart()
	data_uri = base64.b64encode(open('pieChart.png', 'rb').read()).decode('utf-8')
	pie = 'data:image/png;base64,{0}'.format(data_uri)

	pieChart1()
	data_uri = base64.b64encode(open('pieChart1.png', 'rb').read()).decode('utf-8')
	pie1 = 'data:image/png;base64,{0}'.format(data_uri)
	return render_template('country.html', zipCode=zipCode, bar=bar, pie=pie, pie1=pie1)


def barChart():
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items"
	result = cursor.execute(query)

	list = result.fetchall()

	# amount of transactions split by ages
	total = 0
	y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	for transaction in list:
		total = total + transaction[3]
		i = transaction[1] // 10 - 1
		y[i] = y[i] + transaction[3]

	index = 0
	for amt in y:
		y[index] = amt * 100 / total
		index = index + 1

	x = range(10, 100, 10)
	width = 2
	plt.bar(x, y, width, color="blue")
	plt.xlabel('age')
	plt.ylabel('percentage / %')
	plt.savefig('barChart.png')
	plt.close()
	connection.close()

def pieChart():
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items"
	result = cursor.execute(query)
	list = result.fetchall()

	total = 0
	sizes = [0, 0]
	for transaction in list:
		total = total + transaction[3]
		sizes[transaction[0]] = sizes[transaction[0]] + transaction[3]

	sizes[0] = sizes[0] * 100 / total
	sizes[1] = sizes[1] * 100 / total


	labels = 'Man', 'Women'
	colors = ['gold', 'lightskyblue']
	explode = (0.1, 0)  # explode 1st slice

	# Plot
	plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

	plt.axis('equal')
	plt.savefig('pieChart.png')
	plt.close()
	connection.close()

def pieChart1():
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items"
	result = cursor.execute(query)
	list = result.fetchall()

	total = 0
	sizes = [0, 0, 0, 0]
	for transaction in list:
		total = total + transaction[3]
		if transaction[2] == 'Entertainment' :
			sizes[0] = sizes[0] + transaction[3]
		elif transaction[2] == 'Restaurant' :
			sizes[1] = sizes[1] + transaction[3]
		elif transaction[2] == 'Grocery' :
			sizes[2] = sizes[2] + transaction[3]
		else:
			sizes[3] = sizes[3] + transaction[3]

	sizes[0] = sizes[0] * 100 / total
	sizes[1] = sizes[1] * 100 / total
	sizes[2] = sizes[2] * 100 / total
	sizes[3] = sizes[3] * 100 / total


	labels = 'Entertainment', 'Restaurant', 'Grocery', 'Transportation'
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	plt.tight_layout()
	plt.savefig('pieChart1.png')
	plt.close()
	connection.close()

if __name__ == "__main__":
	app.run(port=5000, debug=True)
