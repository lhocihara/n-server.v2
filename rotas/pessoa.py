from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo
import dns

from orquestrador.orquestrador import Orquestrador 
from biblioteca_retornos.status_retorno import StatusRetorno

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
    
    print("\n[Requisição-POST] /pessoa:\n" + str(pessoa_request) + "\n")

    try:
        retorno_id = orq.cadastrar_pessoa(pessoa_request)
        
        json_retorno = {
            'mensagem': 'Cadastro realizado com sucesso',
            'codigo': 201,
            'objeto': {
                'segredo': str(retorno_id),
                'nome_usuario': str(pessoa_request['nome_completo'])
            }
        }
        return jsonify(json_retorno)
    except StatusRetorno as e:
        return e.errors