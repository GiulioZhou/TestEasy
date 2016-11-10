from flask import Flask, render_template, request, jsonify, url_for, session, current_app
from app import app
import json, os

def ret_url(filename):
    return os.path.join(current_app.root_path, current_app.static_folder, filename)

def get_static_json_file(filename):
    url = ret_url(filename)
    return json.load(open(url))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/api/get', methods=['GET'])
def getta():
    print("sono qui dentro")
    print(request.args["user_id"])
    return "ciao"


@app.route('/prova', methods=['GET', 'POST'])
def ciao():
    return render_template('prova.html')

@app.route('/api/register', methods=['POST'])
def register():
        json_data = request.json
        data=get_static_json_file("users.json")
        key=json_data["given_name"]+" "+json_data["family_name"]+" <"+json_data["email"]+">"
        if key in data:
            status = 'this user is already registered'
        else:
            data[key] = json_data
            with open(ret_url("users.json"), "w") as file:
                json.dump(data, file)
            status = 'success'
        return jsonify({'result': status})

@app.route('/api/login',methods=['POST'])
def login():
        json_data = request.json
        #NON FUNZIONA LA OPEN!
        data=get_static_json_file("users.json")
        status = False
        for user in data.values():
                #user["email"] NON FUNZIONA
		print user["email"]
                if user["email"]==json_data["email"] and user["pass"]==json_data["pass"]:
                        #session NON FUNZIONA
                        session['logged_in'] = True
                        session['email'] = user["email"]
                        session['name'] = user["given_name"]
                        session['surname'] = user["family_name"]
                        status = True
			print session
                        break
        return jsonify({'result': status})

@app.route('/api/logout')
def logout():
        session.pop('logged_in', None)
        return jsonify({'result': 'success'})
