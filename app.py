from flask import Flask, request, redirect, Response, render_template, url_for, session, flash
from flask_restful import Api

import matplotlib.pyplot as plt
import base64
import sqlite3

import json, datetime

from item import Item

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
	img_tag = 'data:image/png;base64,{0}'.format(data_uri)
	return render_template('country.html', zipCode=zipCode, tag=img_tag)


def barChart():
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items"
	result = cursor.execute(query)

	list = result.fetchall()
	# print(list)

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



	# y = [3, 10, 7, 5, 3, 4.5, 6, 8.1]
	x = range(10, 100, 10)
	width = 2
	plt.bar(x, y, width, color="blue")
	plt.xlabel('age')
	plt.ylabel('percentage / %')
	plt.savefig('barChart.png')
	connection.close()

if __name__ == "__main__":
	app.run(port=5000, debug=True)
