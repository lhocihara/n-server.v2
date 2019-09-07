# ----------------------------------------------------------
# Importação dos módulos padrões
# ----------------------------------------------------------
from flask_json_schema import JsonSchema, JsonValidationError
from flask import Flask, Blueprint, request, jsonify
from bson.objectid import ObjectId
import pymongo
import dns

# ----------------------------------------------------------
# Importação do orquestrador da conexão com BD
# ----------------------------------------------------------
from orquestrador.orquestrador import Orquestrador
# ----------------------------------------------------------
# Importação dos Objetos de tratamento de erros
# ----------------------------------------------------------
from biblioteca_respostas.status_internos import StatusInternos
from biblioteca_respostas.respostas_api import RespostasAPI
# ----------------------------------------------------------
# Importação dos schemas referentes a Pessoa
# ----------------------------------------------------------
from schemas.pessoa import schemaCadastro, schemaLoginPessoa,schemaEdicao


orq = Orquestrador()

# ----------------------------------------------------------
# Definição do Blueprint
# ----------------------------------------------------------
blueprint_pessoa = Blueprint("Pessoa", __name__)

# ----------------------------------------------------------
# Definição do Subapp e Schema
# ----------------------------------------------------------
app = Flask("Pessoa")
schema = JsonSchema(app)

# ----------------------------------------------------------
# Rotas dos serviços para o APP
# ----------------------------------------------------------
##
# @pessoa_blue.route: A rota do endpoint
# @schema.validate: O schema a ser validado durante a requisição
# ----------------------------------------------------------

# ----------------------------------------------------------
# Endpoint de cadastro inicial de pessoas
# ----------------------------------------------------------
@blueprint_pessoa.route("/cadastro", methods=['POST'])
@schema.validate(schemaCadastro)
def Cadastrar_Pessoa():
    """ Endpoint responsável por cadastrar pessoas dentro da base de dados.

        `Requisição:` Deve ser feita com base no `SchemaCadastro`.

        `Resposta:` Será com base na `Classe StatusInternos` caso houver `erros internos`, ou na `Classe RespostasAPI` para formatar as referidas respostas.
    """
    pessoa_request = request.json

    print("\n[Requisição-POST] /pessoa/cadastro:\n" +
          str(pessoa_request) + "\n")

    try:
        retorno_id = orq.cadastrar_pessoa(pessoa_request)

        json_retorno = RespostasAPI('Cadastro realizado com sucesso',
                {
                    'segredo': str(retorno_id),
                    'nome_usuario': str(pessoa_request['nome_completo'])
                }
            ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors


# ----------------------------------------------------------
# Endpoint de cadastro inicial de pessoas [POST]
# ----------------------------------------------------------
@blueprint_pessoa.route("/login", methods=['POST'])
@schema.validate(schemaLoginPessoa)
def Logar_Pessoa():

    login_request = request.json

    print("\n[Requisição-POST] /pessoa/login:\n" + str(login_request) + "\n")

    try:
        metodo_entrada = login_request['metodo_entrada']
        senha = login_request['senha']
        tipo_entrada = login_request['tipo_entrada']

        retorno = orq.login_pessoa(metodo_entrada, senha, tipo_entrada)
        print(retorno)
        json_retorno = RespostasAPI('Login realizado com sucesso.',
        {
                'segredo': retorno['segredo'],
                'nome_usuario': retorno['nome_usuario'],
        }
        ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors
 

## ---------------------------------------------------------
## Endpoint de edição de dados de pessoas [PUT]
## ---------------------------------------------------------

## ---------------------------------------------------------
## Endpoint de edição de dados de pessoas
## ---------------------------------------------------------
@blueprint_pessoa.route("/editar_dados", methods=['PUT'])
@schema.validate(schemaEdicao)
def Editar_Pessoa():

    editar_request = request.json
    segredo = editar_request['_id']
    dados_editados = editar_request['dados_editados']
    print("\n[Requisição-PUT] /Edição de dados de Pessoa \n" + str(editar_request) + "\n")
    try:
        
        orq.editar_dados_pessoa(segredo, dados_editados)

        if 'dados_excluidos' in editar_request:
            dados_excluidos = editar_request['dados_excluidos']
            orq.excluir_dados_pessoa(segredo, dados_excluidos)
        else:
            dados_excluidos =  None

        json_retorno = RespostasAPI('Edição realizada com sucesso',
                                {
                                    'segredo': segredo,
                                    'dados editados' : dados_editados,
                                    'dados_excluidos' : dados_excluidos,
                                }
                                ).JSON
        return json_retorno

    except StatusInternos as e:
        return e.errors
    
## ---------------------------------------------------------
## Endpoint de adição de dados de pessoas [PUT]
## ---------------------------------------------------------
    

@blueprint_pessoa.route("/adicionar_dados", methods=['PUT'])
@schema.validate(schemaEdicao)
def AdicionarDados_Pessoa():

    adicionar_dados_request = request.json
    segredo = (adicionar_dados_request['_id'])
    dados_novos = adicionar_dados_request['dados_novos']
    print("\n[Requisição-PUT] /Adicionar_Dados:\n" + str(adicionar_dados_request) + "\n")
    try:
        orq.adicionar_dados_pessoa(segredo,dados_novos)

        json_retorno = RespostasAPI('Adição realizada com sucesso',
                                {
                                    'segredo': str(segredo),
                                    'dados adicionados': str(dados_novos),
                                }
                                ).JSON

        return json_retorno

    except StatusInternos as e:
        return e.errors
    
## ---------------------------------------------------------
## Endpoint de consulta de Pessoa [GET]
## ---------------------------------------------------------

    
@blueprint_pessoa.route("/consultar/<segredo>")
def Consultar_Pessoa(segredo):
    segredo = ObjectId(segredo)
    print("\n[Requisição-GET] /Consulta dados  Pessoa\n" )
    try:
        retorno = orq.verificar_id_usuario(segredo)

        json_retorno = RespostasAPI('Consulta realizada com sucesso',
                                {
                                    'segredo': str(segredo),
                                    'dados': retorno,
                                }
                                ).JSON

        return json_retorno
    except StatusInternos as e:
        return e.errors

## ---------------------------------------------------------
## Endpoint de exclusão de dados de Pessoa
## ---------------------------------------------------------

@blueprint_pessoa.route("/excluir_dados", methods=['DELETE'])
@schema.validate(schemaEdicao)
def ExcluirDados_Pessoa():

    excluir_dados_request = request.json
    segredo = excluir_dados_request['_id']
    dados_excluidos = excluir_dados_request['dados_excluidos']
    print("\n[Requisição-DELETE] /Excluir Dados:\n" + str(excluir_dados_request) + "\n")
    try:
        orq.excluir_dados_pessoa(segredo,dados_excluidos)

        json_retorno = RespostasAPI('Exclusão realizada com sucesso',
                                {
                                    'segredo': str(segredo),
                                    'dados' : str(dados_excluidos),
                                }
                                ).JSON

        return json_retorno

    except StatusInternos as e:
        return e.errors
