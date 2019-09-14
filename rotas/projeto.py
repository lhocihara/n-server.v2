## ----------------------------------------------------------
## Importação dos módulos padrões
## ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
import pymongo
import dns
from bson.objectid import ObjectId


## ----------------------------------------------------------
## Importação do orquestrador da conexão com BD
## ----------------------------------------------------------
from orquestrador.orquestrador import Orquestrador
## ----------------------------------------------------------
## Importação dos Objetos de tratamento de erros
## ----------------------------------------------------------
from biblioteca_respostas.status_internos import StatusInternos
from biblioteca_respostas.respostas_api import RespostasAPI
## ----------------------------------------------------------
## Importação dos schemas referentes a Projetos
## ----------------------------------------------------------
from schemas.projeto import schemaCadastro

orq = Orquestrador()

## ----------------------------------------------------------
## Definição do Blueprint
## ----------------------------------------------------------
blueprint_projeto = Blueprint("Projeto", __name__)

## ----------------------------------------------------------
## Definição do Subapp e Schema
## ----------------------------------------------------------
app = Flask("Projeto")
schema = JsonSchema(app)

## ----------------------------------------------------------
## Rotas dos serviços para o APP
## ----------------------------------------------------------
##
## @projeto_blue.route: A rota do endpoint
## @schema.validate: O schema a ser validado durante a requisição
## ----------------------------------------------------------

## ----------------------------------------------------------
## Endpoint de cadastro de projetos
## ----------------------------------------------------------

## ----------------------------------------------------------
## Endpoint de cadastro de projetos
## ----------------------------------------------------------
@blueprint_projeto.route("/cadastro", methods=['POST'])
def Cadastrar_Projeto():

    projeto_request = request.json

    print("\n[Requisição-POST] /Cadastro de Projeto: \n" + str(projeto_request) + "\n")

    try:
        retorno_id = orq.cadastrar_projeto(projeto_request)

        json_retorno = RespostasAPI('Cadastro realizado com sucesso',
                                    {
                                        'segredo': str(retorno_id),
                                        'nome_projeto': projeto_request['nome_projeto']
                                    }
                                    ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors

## ----------------------------------------------------------
## Endpoint de consulta de projetos
## ----------------------------------------------------------
@blueprint_projeto.route("/consultar/<segredo>")
def Consultar_Projeto(segredo):

    segredo = ObjectId(segredo)
    print("\n[Requisição-GET] /Consultar dados Projeto:\n" "\n")
    try:
        retorno = orq.verificar_id_projeto(segredo)

        json_retorno = RespostasAPI('Consulta realizada com sucesso',
                                {
                                    'segredo': str(segredo),
                                    'dados': retorno
                                }
                                ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors





