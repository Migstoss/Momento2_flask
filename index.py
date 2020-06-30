from flask import Flask, render_template, request, redirect, url_for, flash
import requests as req

app = Flask(__name__)

@app.route('/index')
def index():
	response = req.get('http://192.168.0.6:3000/api/listProperty');	
	result = response.json()['properties']	

	return render_template('index.html', properties = result)

@app.route('/')
def login():

	return render_template('login.html')

@app.route('/add', methods=['POST'])
def add():
	title = request.form['titleRes']
	type = request.form['typeRes']
	address = request.form['addressRes']
	rooms = request.form['roomsRes']
	price = request.form['priceRes']
	area = request.form['areaRes']
	addData = {"title": title, "type": type, "address": address, "rooms": rooms, "price": price, "area": area}
	response = req.post('http://localhost:3000/api/addProperty', json = addData)

	return redirect(url_for('index'))

@app.route('/create')
def create():
  return render_template('create-property.html')

@app.route('/addrecord', methods=['POST'])
def addrecord():
	return redirect(url_for('index'))
	
@app.route('/edit')
def edit():
	id = request.args.get('id')
	response = req.post(f'http://192.168.0.6:3000/api/getProperty?id={id}')
	
	result = response.json()['property']	

	return render_template('edit-property.html', properties = result)

@app.route('/update', methods = ['POST'])
def update():
	id = request.args.get('id')
	title = request.form['titleEd']
	type = request.form['typeEd']
	address = request.form['addressEd']
	rooms = request.form['roomsEd']
	price = request.form['priceEd']
	area = request.form['areaEd']

	editData = {"id": id, "title": title, "type": type, "address": address, "rooms": rooms, "price": price, "area": area}
	response = req.put('http://192.168.0.6:3000/api/updateProperty', json = editData)

	return redirect(url_for('index'))

@app.route('/delete')
def delete():
  id = request.args.get('id')
  deleteData = {"id": id}
  response = req.delete('http://192.168.0.6:3000/api/deleteProperty', json = deleteData)

  return redirect(url_for('index'))

@app.route('/auth', methods= ['POST'])
def auth():
	email = request.form['emailLog']
	password = request.form['passLog']

	getUser = {"email": email, "password": password}	
	response = req.post('http://192.168.0.6:3000/api/getUser', json = getUser)	
	result = response.json()['user']

	if result == []:
		print("Error")	
		return redirect(url_for('login'))
	else:
		print("Succ")
		return redirect(url_for('index'))

@app.route('/register', methods= ['POST'])
def registerUser():
	name = request.form['nameUser']
	surname = request.form['surnameUser']
	email = request.form['emailUser']
	password = request.form['passUser']
	addUser = {"name": name, "surname": surname, "email": email, "password": password}
	response = req.post('http://localhost:3000/api/addUser', json = addUser)
	
	return redirect(url_for('login'))

@app.route('/createUser')
def createUser():
  return render_template('create-user.html')

if __name__ == "__main__":
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'

	app.run(debug = True)