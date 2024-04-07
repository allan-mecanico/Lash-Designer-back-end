Para corrigir o código e gerar um token apenas para o admin, você precisa fazer algumas alterações. Aqui está o código atualizado:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
import jwt

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

@app.route('/create_admin', methods=['POST'])
def create_admin():
    dados = request.json
    new_password = dados.get('new_password')

    global ADMIN_PASSWORD
    ADMIN_PASSWORD = new_password

    return jsonify({'mensagem': 'Credenciais de administrador criadas com sucesso'}), 200

class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    whatsapp = db.Column(db.String(12))
    dia = db.Column(db.String(10))
    horario = db.Column(db.String(10))
    tipo_cilio = db.Column(db.String(20))

ADMIN_PASSWORD = "sua_senha_administrativa"
SECRET_KEY = "chave_secreta_para_jwt"

def autenticar(username, password):
    return username == 'admin' and password == ADMIN_PASSWORD

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    username = dados.get('username')
    password = dados.get('password')
    
    if autenticar(username, password):
        token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token.decode('utf-8')}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'mensagem': 'Token ausente'}), 401

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido'}), 401

        if decoded_token['username'] != 'admin':
            return jsonify({'mensagem': 'Acesso não autorizado'}), 401

        return func(*args, **kwargs)

    return wrapper

@app.route('/dados', methods=['GET'])
@require_token
def mostrar_dados_protegido():
    return jsonify({'mensagem': 'Esses são os dados protegidos'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='192.168.10.20', port=8000)