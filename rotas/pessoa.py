from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo


## ----------------------------------------------------------
## Definição do Blueprint
## ----------------------------------------------------------
blueprint_pessoa = Blueprint("Pessoa",__name__)

## ----------------------------------------------------------
## Definição do Subapp e Schema
## ----------------------------------------------------------
app = Flask("Pessoa")
schema = JsonSchema(app)

## ----------------------------------------------------------
## Definição do schema de validação do Json a ser recebido pela requisição HTTP
## ----------------------------------------------------------
schemaCadastroPessoa = {
    "title": "Pessoa",
    "type": "object",
    "required": ["nome_completo", "cpf", "data_nasc", "genero", "email", "senha"],
    "properties": {
        "nome_completo": {
            "type": "string", "pattern": "^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$"
        },
        "cpf": {
            "type": "string", "minLength": 11, "maxLength": 11
        },
        "rg:": {
            "type": "object",
            "properties": {
                "emissor":{
                    "type": "string", "minLength": 3, "maxLength": 3
                },
                "numero": {
                    "type": "string", "maxLength": 14
                }
            }
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
            "type": "string", "minLength": 8 #Adicionar criptografia
        }
    }
}

## ----------------------------------------------------------
## Rotas dos serviços para o APP
## ----------------------------------------------------------
##
## @pessoa_blue.route: A rota do endpoint
## @schema.validate: O schema a ser validado durante a requisição
## ----------------------------------------------------------

## ----------------------------------------------------------
## Endpoint de cadastro inicial de pessoas
## ----------------------------------------------------------
@blueprint_pessoa.route("/pessoa", methods=['PUT'])
@schema.validate(schemaCadastroPessoa)
def Cadastrar_Pessoa():
    ## ----------------------------------------------------------
    ## Conexão com MongoDB
    ## ----------------------------------------------------------
    mongo = pymongo.MongoClient("mongodb+srv://dev_connect:rgPuzhTgc8HAHFlV@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = pymongo.database.Database(mongo, 'TCC')
    dbcol = pymongo.collection.Collection(db, 'Pessoas')

    ## Requisição do Json
    if not request.json:
        return 'ERRO 400, requisição não encontrada'
    ## Verifica se o CPF já existe no Banco
    if dbcol.find({'cpf': dict(request.json)['cpf']}).limit(1).count() > 0:
        return 'Já existe um cadastro com este CPF em nossa base de dados'
    ## Caso CPF não exista no banco, realiza o cadastro/insere dados no banco
    else:
        pessoa_gerada = dbcol.insert_one(request.json)
        
        json_retorno = {
            'msg': 'Cadastro realizado com sucesso',
            'cod': '201',
            'segredo': str(pessoa_gerada.inserted_id),
            'nome_usuario': str(request.json['nome_completo'])
        }

        return jsonify(json_retorno)
        # return ('Cadastro realizado com sucesso, ' + str(request.json['nome']))