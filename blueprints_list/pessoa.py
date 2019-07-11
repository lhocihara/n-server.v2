# # coding: utf-8
import os, pymongo
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, jsonify, Blueprint, request, current_app, send_from_directory, render_template


## ----------------------------------------------------------
## Conexão com MongoDB
## ----------------------------------------------------------
pessoa_blueprint = Blueprint('pessoa', __name__)
# schema = JsonSchema(pessoa_blueprint)


## ----------------------------------------------------------
## Conexão com MongoDB
## ----------------------------------------------------------
mongo = pymongo.MongoClient("mongodb+srv://dev_connect:rgPuzhTgc8HAHFlV@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = pymongo.database.Database(mongo, 'TCC')
dbcol = pymongo.collection.Collection(db, 'TCC.Pessoas')


## ----------------------------------------------------------
## Definição do schema de validação do Json a ser recebido pela requisição HTTP
## ----------------------------------------------------------
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


## ----------------------------------------------------------
## Rotas dos serviços para o APP
##
## pessoas_blueprint.route: Definição do endpoint
## schema.validate: Schema a ser validado durante a requisição
## ----------------------------------------------------------

## ----------------------------------------------------------
## Cadastro inicial de pessoas
## ----------------------------------------------------------
@pessoa_blueprint.route("/cad", methods=['POST'])
# @schema.validate(schemaCadastroPessoa)
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
