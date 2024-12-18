from flask import Flask, render_template
from dotenv import load_dotenv
import os
from config.mongo import mongo
from routes.todo import todo

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mi_basedatos')

if not MONGO_URI:
    raise ValueError("La variable MONGO_URI no está configurada correctamente")

app.config['MONGO_URI'] = MONGO_URI
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

# Registro del blueprint para las rutas '/todo'
app.register_blueprint(todo, url_prefix='/todo')

if __name__ == '__main__':
    app.run(debug=True)
