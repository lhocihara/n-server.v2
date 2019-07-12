## ----------------------------------------------------------
## Importação dos módulos padrões
## ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo
import dns

## ----------------------------------------------------------
## Importação do orquestrador da conexão com BD
## ----------------------------------------------------------
from orquestrador.orquestrador import Orquestrador 
## ----------------------------------------------------------
## Importação dos Objetos de tratamento de erros
## ----------------------------------------------------------
from biblioteca_retornos.status_interno import ListaStatusInterno
## ----------------------------------------------------------
## Importação dos schemas referentes a Pessoa
## ----------------------------------------------------------
from schemas.pessoa import schemaCadastro


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
@schema.validate(schemaCadastro)
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
    except ListaStatusInterno as e:
        return e.errors