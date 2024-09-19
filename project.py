from flask import Flask
from flask_mysqldb import MySQL
import datetime
from query import obtenerUsuarios

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
app = Flask(__name__, static_folder='static', template_folder='template')

@app.route('/login')
def login():     
    obtenerUsuarios()
    return render_template('login.html')

if __name__ =='__main__':
    app.run(port =4000, debug =True)