from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    whatsapp = db.Column(db.String(12))
    dia = db.Column(db.String(10))
    horario = db.Column(db.String(10))
    tipo_cilio = db.Column(db.String(20))

@app.route('/dados', methods=['POST'])
def receber_dados():
    if request.method == 'POST':
        dados = request.json
        print(dados)  # Imprime os dados recebidos do JSON

        nome = dados.get('nome')
        whatsapp = dados.get('whatsapp')
        dia = dados.get('dia')
        horario = dados.get('horario')
        tipo_cilio = dados.get('tipo_cilio')

        novo_dado = Dados(nome=nome, whatsapp=whatsapp, dia=dia, horario=horario, tipo_cilio=tipo_cilio)
        db.session.add(novo_dado)
        db.session.commit()

        return 'Dados recebidos e salvos com sucesso!'

@app.route('/dados/<int:id>', methods=['PUT'])
def atualizar_dados(id):
    if request.method == 'PUT':
        dados = request.json

        nome = dados.get('nome')
        whatsapp = dados.get('whatsapp')
        dia = dados.get('dia')
        horario = dados.get('horario')
        tipo_cilio = dados.get('tipo_cilio')

        dado_existente = Dados.query.get(id)
        dado_existente.nome = nome
        dado_existente.whatsapp = whatsapp
        dado_existente.dia = dia
        dado_existente.horario = horario
        dado_existente.tipo_cilio = tipo_cilio

        db.session.commit()

        return 'Dados atualizados com sucesso!'

@app.route('/dados/<int:id>', methods=['DELETE'])
def deletar_dados(id):
    if request.method == 'DELETE':
        dado_excluir = Dados.query.get(id)
        db.session.delete(dado_excluir)
        db.session.commit()

        return 'Dados excluídos com sucesso!'
    else:
        return 'Método DELETE não permitido.'

@app.route('/dados', methods=['GET'])
def mostrar_dados():
    if request.method == 'GET':
        dados = Dados.query.all()
        dados_json = []

        for dado in dados:
            dado_dict = {
                'id': dado.id,
                'nome': dado.nome,
                'whatsapp': dado.whatsapp,
                'dia': dado.dia,
                'horario': dado.horario,
                'tipo_cilio': dado.tipo_cilio
            }
            dados_json.append(dado_dict)

        return jsonify(dados_json)

if __name__ == '__main__':
    db.create_all()
    app.run(host='192.168.10.20', port=8000)
