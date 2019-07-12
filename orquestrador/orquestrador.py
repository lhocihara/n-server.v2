import json
from pymongo import MongoClient # Para acessar o MongoDB
from bson.objectid import ObjectId
import urllib.parse # (OPCIONAL) Para criar texto de URI 

# from CodigoStatusApi import CodigoStatusApi
# from CodigoStatusHttp import CodigoStatusHttp

class Orquestrador(object):
  def __init__(self):
    print("\n[Orquestrador] instanciado com sucesso!\n")
    
    # Carregando com paramêtros de acesso para desenvolvedor
    usuario_banco = urllib.parse.quote_plus('dev_connect')
    senha_banco = urllib.parse.quote_plus('rgPuzhTgc8HAHFlV')

    # Criando conexão com o MongoDB
    conexao_servidor = MongoClient('mongodb+srv://%s:%s@cluster0-hygoa.gcp.mongodb.net/?retryWrites=true' % (usuario_banco, senha_banco))

    # Instanciando um gerenciador do banco de dados TCC
    self.conexao_bd = conexao_servidor.TCC

  def cadastrar_pessoa(self, pessoa):
    try:
      colecao_pessoas = self.conexao_bd.Pessoas
    except Exception as e:
      print("[Orquestrador.ERRO] erro durante a conexão com a coleção")
      raise str(e)
    #   raise Exception(CodigoStatusHttp(500).retorno())
    
    bd_doc = "{"

    for i,k in enumerate( pessoa.lista_chaves_encontradas):
      if(isinstance(getattr(pessoa, k), str)):
        v_formatado = str('"' + getattr(pessoa, k)+ '"')
      else:
        v_formatado = str(getattr(pessoa, k))
      
      if len(pessoa.lista_chaves_encontradas) -1 != i :
        bd_doc += str('"' + k + '":' + str(v_formatado) + ",")
      else:
        bd_doc += str('"' + k + '":' + str(v_formatado))
    
    bd_doc += "}"
    
    # # Linha para ser aplicada quando a validação por e-mail for implementada
    #bd_doc += str(" 'acesso_validado': 0")
    #print(k, ': ', getattr(pessoa, k))
    
    print('\n[Orquestrador] documento de cadastro em formato json: \n' + bd_doc + "\n")
  
    try:
      #Chamada de função para inserir documento de cadastro
      pessoa_id = colecao_pessoas.insert_one(json.loads(bd_doc))

       # # Chama função de cadastro do Blockchain
      print("\n[Orquestrador] pessoa cadastrada com sucesso!\n")
      print(str(pessoa_id.inserted_id))
      return(str(pessoa_id.inserted_id))
    except Exception as e:
      print("[Orquestrador] Falha ao executar comando de cadastro de pessoa.")
      raise str(e)
    #   raise Exception(CodigoStatusHttp(500).retorno())

  def adcionar_dados_pessoa(self, pessoa):
    # simulando retorno OK
    return True
    
  def editar_dados_pessoa(self, pessoa):
    # simulando retorno OK
    return True

  def excluir_pessoa(self, pessoa_id_usuario):
    # simulando retorno OK
    return True

  def verificar_cpf(self,pessoa_cpf):
    try:
      retorno_consulta = self.conexao_bd.Pessoas.find({ "cpf": pessoa_cpf})
      
      try:
        print("[Orquestrador] CPF encontrado na coleção de Pessoas, exibindo documento retornado:\n" + str(retorno_consulta[0]) + "\n")
        return True
      except IndexError:
        return False 
    except Exception as e:
      print("[Orquestrador.ERRO] Erro durante a execução do comando de seleção.")
      raise str(e)
    #   raise Exception(CodigoStatusHttp(500).retorno())


  def login_pessoa(self,valor_login, senha, tipo):  
    # Login por cpf
    if(tipo == '0'):
      metodo_login = "cpf"
    # Login por e-mail  
    elif(tipo == '1'):  
      metodo_login = "email"
    # Login com identificador errado
    else:
      print("[Orquestrador.ERRO] Método de login não identificou o método de login.")
      return False

    try:
      if(self.conexao_bd.Pessoas.find({"$and": [{metodo_login: valor_login}, {"senha": senha}]}).limit(1).count() > 0):
        print("[Orquestrador] "+ metodo_login + ": '"+ valor_login +"' encontrado na coleção de Pessoas, exibindo documento retornado:")

        dados_pessoa = self.conexao_bd.Pessoas.find({"$and": [{metodo_login: valor_login}, {"senha": senha}]})
        
        print(str(dados_pessoa[0]['_id']))

        return str(dados_pessoa[0]['_id'])
      else:
        print("[Orquestrador] "+ metodo_login + ": '"+ valor_login +"' não encontrado na coleção de Pessoas.")
        return None
    except Exception as e:
      print("[Orquestrador.ERRO] Erro durante a execução do comando de seleção.")
      raise str(e)
    #   raise Exception(CodigoStatusHttp(500).retorno())

  def verificar_id_usuario(self,pessoa_id_usuario):
    try:
      if(self.conexao_bd.Pessoas.find({ "_id": ObjectId(pessoa_id_usuario)}).limit(1).count() > 0):
        print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) + "' encontrado na coleção de Pessoas, exibindo documento retornado:\n")
        dados_pessoa = self.conexao_bd.Pessoas.find({ "_id": ObjectId(pessoa_id_usuario)})
        print(str(dados_pessoa[0]))
        return dados_pessoa[0]
      else:
        print("[Orquestrador] id pessoa '" + str(pessoa_id_usuario) + "' não encontrado na coleção de Pessoas\n")
        return None 
    except Exception as e:
      print("[Orquestrador.ERRO] erro durante a execução do comando de seleção")
      print(e)
      
      # raise Exception(CodigoStatusHttp(500).retorno())