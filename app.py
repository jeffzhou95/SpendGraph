from flask import Flask, request, redirect, Response, render_template, url_for, session, flash
from flask_restful import Api

import json, datetime

from item import Item

# .\venv\Scripts\activate.bat

app = Flask(__name__)
app.secret_key = 'miaomiao'

@app.route('/home/')
def home():
	return render_template('front.html')

@app.route('/')
def output():
	if not session.get('logged_in'):
		session['url'] = url_for('output')
		return render_template('login.html')
	return render_template('index.html')

@app.route('/', methods=['POST'])
def foo():
	first = request.form['first']
	last = request.form['last']
	email = request.form['email']
	topic = request.form['topic']
	institution = request.form['institution']
	item = Item.find_by_name(first, last, email, topic, institution)
	if item:
		return render_template("info.html", message=item, count=len(item))
	flash('I cannot find any information for your search, please go back!')
	return render_template('index.html')

@app.route('/add/')
def add():
	if not session.get('logged_in'):
		session['url'] = url_for('add')
		return render_template('login.html')
	return render_template('add.html')

@app.route('/add/', methods=['POST'])
def addThis():
	item = []
	item.append(request.form['email'])
	item.append(request.form['first'])
	item.append(request.form['last'])
	item.append(request.form['institution'])
	item.append(request.form['department'])
	item.append(request.form['street'])
	item.append(request.form['city'])
	item.append(request.form['state'])
	item.append(request.form['zipCode'])
	item.append(request.form['country'])
	item.append(request.form['officePhone'])
	item.append(request.form['mobilePhone'])
	item.append(request.form['website'])
	item.append(request.form['topic'])
	item.append(request.form['twitter'])
	item.append(request.form['facebook'])
	item.append(request.form['requirements'])
	item.append(request.form['needs'])
	item.append(request.form['M'])
	item.append(request.form['D'])
	item.append(request.form['Y'])
	Item.insert(item)
	flash('Add successfully!')
	return render_template('add.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/layout/')
def layout():
	return render_template('layout.html')

@app.route('/<id>/')
def info(id):
	if not session.get('logged_in'):
		if not url_for('info', id=id) == '/favicon.ico/':
			session['url'] = url_for('info', id=id)
		return render_template('login.html')
	item = Item.find_by_id(id)
	if item:
		return render_template('item.html', message=item[0], warning="")
	return render_template('item.html', message=[], warning="I don't have this user.")

@app.route('/<id>/delete/')
def delete(id):
	if not session.get('logged_in'):
		return render_template('login.html')
	item = Item.find_by_id(id)
	Item.delete(item[0][21])
	flash('Delete ' + item[0][1] + ' ' + item[0][2] + ' from our database successfully!')
	return render_template('index.html')

@app.route('/<id>/update/')
def update(id):
	if not session.get('logged_in'):
		return render_template('login.html')
	item = Item.find_by_id(id)
	return render_template('update.html', item=item[0])

@app.route('/<id>/update/', methods=['POST'])
def upd(id):
	item = []
	item.append(request.form['email'])
	item.append(request.form['first'])
	item.append(request.form['last'])
	item.append(request.form['institution'])
	item.append(request.form['department'])
	item.append(request.form['street'])
	item.append(request.form['city'])
	item.append(request.form['state'])
	item.append(request.form['zipCode'])
	item.append(request.form['country'])
	item.append(request.form['officePhone'])
	item.append(request.form['mobilePhone'])
	item.append(request.form['website'])
	item.append(request.form['topic'])
	item.append(request.form['twitter'])
	item.append(request.form['facebook'])
	item.append(request.form['requirements'])
	item.append(request.form['needs'])
	item.append(request.form['M'])
	item.append(request.form['D'])
	item.append(request.form['Y'])
	Item.update(id, item)
	flash('Update successfully!')
	return redirect(url_for('info', id=id))

@app.route('/login/')
def login():
	return render_template('login.html', loginOrNot=session.get('logged_in'))

@app.route('/login/', methods=['POST'])
def log():
	if request.form['user'] == 'Miaomiao' and request.form['key'] == 'Admin':
		session['logged_in'] = True
		flash('Login successfully!')
		if 'url' in session:
			return redirect(session['url'])
		return render_template('index.html')
	else:
		flash('Wrong Username or Key!')
		return render_template('login.html')

@app.route('/logout/')
def logout():
	if not session.get('logged_in'):
		return render_template('login.html')
	session['logged_in'] = False
	flash('Logout successfully!')
	return render_template('login.html', loginOrNot=session.get('logged_in'))


if __name__ == "__main__":
	app.run(port=5000, debug=True)
