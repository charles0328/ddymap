from flask import Flask, render_template
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://charles:1111@cluster0.szvramp.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbddymap

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/board')
def board():
   return render_template('board.html')

@app.route('/about')
def about():
   return render_template('about.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)