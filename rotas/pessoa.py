from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo


from orquestrador.orquestrador import Orquestrador 

orq = Orquestrador()

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
@blueprint_pessoa.route("/pessoa", methods=['POST'])
@schema.validate(schemaCadastroPessoa)
def Cadastrar_Pessoa():
    
    pessoa_request = request.json
    
    print(pessoa_request)

    try:
        raise BaseException("eae menó")
        orq.cadastrar_pessoa(pessoa_request)
        
        json_retorno = {
                "mensagem": "oi.",
                "codigo": 200
            }
        return jsonify(json_retorno)
    except Exception as e:
        return jsonify(str(e))

    # anterior -------------------------------------------------
    
    ## ----------------------------------------------------------
    ## Conexão com MongoDB
    ## ----------------------------------------------------------
    mongo = pymongo.MongoClient("mongodb+srv://dev_connect:rgPuzhTgc8HAHFlV@cluster0-hygoa.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = pymongo.database.Database(mongo, 'TCC')
    dbcol = pymongo.collection.Collection(db, 'Pessoas')

    ## Requisição do Json
    if not request.json:
        json_retorno = {
            "mensagem": "Requisição não encontrada.",
            "codigo": 400
        }
        return jsonify(json_retorno)
        # return 'ERRO 400, requisição não encontrada'
    ## Verifica se o CPF já existe no Banco
    if dbcol.find({'cpf': dict(request.json)['cpf']}).limit(1).count() > 0:
        json_retorno = {
            "mensagem": "Já existe um cadastro com este CPF em nossa base de dados",
            "codigo": "SI-1"
        }
        return jsonify(json_retorno)
    ## Caso CPF não exista no banco, realiza o cadastro/insere dados no banco
    else:
        pessoa_gerada = dbcol.insert_one(request.json)
        
        json_retorno = {
            "mensagem": "Cadastro realizado com sucesso.",
            "codigo": 201,
            "objeto": {
                "segredo": str(pessoa_gerada.inserted_id),
                "nome_usuario": str(request.json["nome_completo"])
            }
        }

        return jsonify(json_retorno)
        # return ('Cadastro realizado com sucesso, ' + str(request.json['nome']))