## ----------------------------------------------------------
## Importação dos módulos padrões
## ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
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
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
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
@cross_origin()
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
@cross_origin()
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

## ----------------------------------------------------------
## Endpoint de consulta de projetos
## ----------------------------------------------------------
@blueprint_projeto.route("/consulta_por_pessoa/<segredo>")
@cross_origin()
def Consultar_Por_Pessoa(segredo):

    print("\n[Requisição-GET] /Consultar dados Projeto por Pessoa:\n" "\n")
    try:
        
        lista_projetos = orq.consulta_projetos_por_pessoa(segredo)

        if lista_projetos != None:
                               
            json_retorno = RespostasAPI('Consulta realizada com sucesso',
                                    {
                                        'segredo': str(segredo),
                                        'dados': lista_projetos
                                    }
                                    ).JSON
            return json_retorno
        else:
            raise StatusInternos('SI-23', {'pessoa': segredo})       
    except StatusInternos as e:
        return e.errors


## ----------------------------------------------------------
## Aceite de termos
## ----------------------------------------------------------
@blueprint_projeto.route("/aceite_termos", methods=['PUT'])
@cross_origin()
def Aceitar_Termos():
    print("\n[Requisição-PUT] /Definir permissão do usuário para o projeto:\n" "\n")
    try:
        segredo = request.json['segredo']
        aceito = request.json['aceito']

        if (type(aceito) != bool):       
            raise StatusInternos('SI-XX', {'segredo': segredo})        

        status = orq.aceite_termos(segredo, aceito)

        if status != None:
                               
            json_retorno = RespostasAPI('Permissão definida',
                                        {
                                            'segredo': str(segredo),
                                            'dados': status
                                        }
                                        ).JSON
            return json_retorno       
        else:
            raise StatusInternos('SI-4', {'segredo': segredo})         
    except StatusInternos as e:
        return e.errors
