import sqlite3
from flask import request
from flask_restful import Resource, reqparse

class Item(Resource):
	# parser = reqparse.RequestParser()
	# parser.add_argument("email",
	# 	type = string,
	# 	required = True,
	# 	help = "This field cannot be left blank."
	# )

	@classmethod
	def find_by_name(cls, firstName, lastName, email, topic, institution):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()
		firstName = '%' + firstName.upper() + '%'
		lastName = '%' + lastName.upper() + '%'
		email = '%' + email.upper() + '%'
		topic = '%' + topic + '%'
		institution = '%' + institution + '%'

		query = "SELECT * FROM items WHERE firstName LIKE ? and lastName LIKE ? and email LIKE ? and topic LIKE ? and institution LIKE ?"
		result = cursor.execute(query, (firstName, lastName, email, topic, institution))

		list = result.fetchall()
		connection.close()

		return list

	@classmethod
	def find_by_id(cls, id):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE id=?"
		result = cursor.execute(query, (id,))


		item = result.fetchall()
		connection.close()

		return item

	@classmethod
	def insert(cls, item):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		insert_item = "INSERT INTO items (email, firstName, lastName, institution, department, street, city, state, zipCode, country, officePhone, mobilePhone, website, topic, twitter, facebook, requirements, needs, M, D, Y) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		cursor.execute(insert_item, item)

		connection.commit()
		connection.close()

	@classmethod
	def delete(cls, id):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		delete_item = "DELETE FROM items WHERE Id=?"
		cursor.execute(delete_item, (id,))

		connection.commit()
		connection.close()

	@classmethod
	def update(cls, id, item):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		update_item = "UPDATE items SET email=?, firstName=?, lastName=?, institution=?, department=?, street=?, city=?, state=?, zipCode=?, country=?, officePhone=?, mobilePhone=?, website=?, topic=?, twitter=?, facebook=?, requirements=?, needs=?, M=?, D=?, Y=? WHERE Id=?"
		cursor.execute(update_item, (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16], item[17], item[18], item[19], item[20], id))

		connection.commit()
		connection.close()

class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		query = "SELECT * FROM items"
		result = cursor.execute(query)
		items = []
		for row in result:
			items.append({'firstName': row[0], 'lastName': row[1], 'email': row[2]})

		connection.close()

		return {'items': items}
