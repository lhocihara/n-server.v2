# -*- coding: utf-8 -*-
import os, pymongo
from flask import Flask, jsonify, request, render_template
from flask_json_schema import JsonSchema, JsonValidationError


app = Flask(__name__)
##app.config['MONGO_DBNAME'] = 'TCC.Pessoas'
##app.config['MONGO_URI'] = 'mongodb+srv://admin_connect:<#_n2noficial_#>@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority'
mongo = pymongo.MongoClient("mongodb+srv://dev_connect:rgPuzhTgc8HAHFlV@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = pymongo.database.Database(mongo, 'TCC')
dbcol = pymongo.collection.Collection(db, 'TCC.Pessoas')

## ----------------------------------------------------------
## Rotas padrões
## ----------------------------------------------------------

## Setando tratamento de erros na validação
@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'Erro': e.message, 'Errors': [validation_error.message for validation_error in e.errors]})

## Endpoint de boas vindas
@app.route("/hi")
def boas_vindas():
    return render_template("bem_vindos.html")

## Endpoint index
@app.route("/")
def index():
    return render_template("index.html")

## ----------------------------------------------------------
## Rotas dos serviços para o APP
## ----------------------------------------------------------

schema = JsonSchema(app)
## Definição do schema de validação do Json a ser recebido pela requisição HTTP
schemaCadastroPessoa = {
    "title": "Pessoa",
    "type": "object",
    "required": ["nome", "cpf", "data_nasc", "genero", "email", "senha"],
    "properties": {
        "nome": {
            "type": "string", "pattern": "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
        },
        "cpf": {
            "type": "string", "minLength": 11, "maxLength": 11
        },
        "data_nasc": {
            "type": "string", "format": "date-time"
        },
        "genero": {
            "type": "string", "pattern": "^[M|F|D]$"
        },
        "email": {
            "type": "string", "format": "email"
        },
        "senha": {
            "type": "string", "minLength": 8, "maxLength": 30 #Adicionar criptografia
        }
    }
}

##Definição do endpoint
@app.route("/panic", methods=['POST'])
##O schema a ser validado durante a requisição
@schema.validate(schemaCadastroPessoa)
def nao_entre_em_panico():
    if request.headers.get('Authorization') == '42':
        return jsonify({"42": "Nao entra em panico, soh estou fazendo o tcc, e com autorização, hehe!"})
    return jsonify({"message": "Nao entra em panico, soh estou fazendo o tcc, utilizando o tcc!"})

##Definição do endpoint
@app.route("/pessoa", methods=['POST'])
##O schema a ser validado durante a requisição
@schema.validate(schemaCadastroPessoa)
## função  de cadastro inicial de pessoas
def Cadastrar_Pessoa():
    ##Requisição do Json
    if not request.json:
        return 'ERRO 400, requisição não encontrada'
    ##Verifica se o CPF já existe no Banco
    if dbcol.find({'cpf': dict(request.json)['cpf']}).limit(1).count() > 0:
        return 'Já existe um cadastro com este CPF em nossa base de dados'
    ##Caso CPF não exista no banco, realiza o cadastro/insere dados no banco
    else:
        dbcol.insert_one(request.json)
        return ('Cadastro realizado com sucesso, ' + str(request.json['nome']))

## ----------------------------------------------------------
## configuração de IP e porta
## ----------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)