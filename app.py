from flask import Flask, request, redirect, Response, render_template, url_for, session, flash

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
	country = request.form['country']
	# item = Item.find_by_name(first, last, email, topic, institution)
	# if item:
	# 	return render_template("info.html", message=item, count=len(item))
	# return render_template('index.html')
	# barChart(country)
	# data_uri = base64.b64encode(open('barChart.png', 'rb').read()).decode('utf-8')
	# bar = 'data:image/png;base64,{0}'.format(data_uri)
	#
	# pieChart(country)
	# data_uri = base64.b64encode(open('pieChart.png', 'rb').read()).decode('utf-8')
	# pie = 'data:image/png;base64,{0}'.format(data_uri)
	#
	# pieChart1(country)
	# data_uri = base64.b64encode(open('pieChart1.png', 'rb').read()).decode('utf-8')
	# pie1 = 'data:image/png;base64,{0}'.format(data_uri)
	# return render_template('country.html', country=country, bar=bar, pie=pie, pie1=pie1)
	return redirect(url_for('show', country=country))

@app.route('/<country>/')
def show(country):
	res = edu()

	barChart(country)
	data_uri = base64.b64encode(open('barChart.png', 'rb').read()).decode('utf-8')
	bar = 'data:image/png;base64,{0}'.format(data_uri)

	pieChart(country)
	data_uri = base64.b64encode(open('pieChart.png', 'rb').read()).decode('utf-8')
	pie = 'data:image/png;base64,{0}'.format(data_uri)

	pieChart1(country)
	data_uri = base64.b64encode(open('pieChart1.png', 'rb').read()).decode('utf-8')
	pie1 = 'data:image/png;base64,{0}'.format(data_uri)
	return render_template('country.html', country=country, bar=bar, pie=pie, pie1=pie1, res=res)

def edu():
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT city, SUM(amount) as A FROM items WHERE category = 'Education' GROUP BY city ORDER BY A"
	result = cursor.execute(query)
	list = result.fetchall()

	order = []
	total = 0
	for x in list:
		order.append(x[0])
		total += x[1]
	per = []

	for x in list:
		per.append(int(x[1] * 100 // total))

	res = zip(order, per)

	connection.close()
	return res


def barChart(countryName):
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items WHERE city = ?"
	result = cursor.execute(query, (countryName, ))

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

def pieChart(countryName):
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items WHERE city = ?"
	result = cursor.execute(query, (countryName, ))
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

def pieChart1(countryName):
	connection = sqlite3.connect("data.db")
	cursor = connection.cursor()
	query = "SELECT * FROM items WHERE city = ?"
	result = cursor.execute(query, (countryName, ))
	list = result.fetchall()

	total = 0
	sizes = [0, 0, 0, 0, 0]
	for transaction in list:
		total = total + transaction[3]
		if transaction[2] == 'Entertainment' :
			sizes[0] = sizes[0] + transaction[3]
		elif transaction[2] == 'Restaurant' :
			sizes[1] = sizes[1] + transaction[3]
		elif transaction[2] == 'Grocery' :
			sizes[2] = sizes[2] + transaction[3]
		elif transaction[2] == 'Education':
			sizes[3] = sizes[3] + transaction[3]
		else:
			sizes[4] = sizes[4] + transaction[3]

	sizes[0] = sizes[0] * 100 / total
	sizes[1] = sizes[1] * 100 / total
	sizes[2] = sizes[2] * 100 / total
	sizes[3] = sizes[3] * 100 / total
	sizes[4] = sizes[4] * 100 / total


	labels = 'Entertainment', 'Restaurant', 'Grocery', 'Education', 'Transportation'
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'darkblue']
	explode = (0, 0, 0, 0.1, 0)
	plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

	plt.axis('equal')
	plt.savefig('pieChart1.png')
	plt.close()
	connection.close()



if __name__ == "__main__":
	app.run(port=5000, debug=True)
