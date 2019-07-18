# -*- coding: utf-8 -*-
from flask import jsonify

class RespostasAPI():
  def __init__(self, mensagem_resposta, objeto=None):    
    self.codigo = 201
    self.mensagem = mensagem_resposta
    self.objeto = objeto

    self.JSON  = self.retorno() 
  
  def retorno(self):
    if (self.objeto):
      print("\n[Retorno API] JSON de retorno: \n" + str({
        "codigo": self.codigo,
        "mensagem": self.mensagem,
        "objeto": self.objeto,
        "timestamp": "0000-00-00 00000000000"
      }) + "\n")

    
      return jsonify(
        codigo= self.codigo,
        mensagem= self.mensagem,
        objeto= self.objeto,
        timestamp= "0000-00-00 00000000000"
      )
    else:
      print("\n[Retorno API] JSON de retorno: \n" + str({
        "codigo": self.codigo,
        "mensagem": self.mensagem,
        "timestamp": "0000-00-00 00000000000"
      }) + "\n")

      return jsonify(
        codigo= self.codigo,
        mensagem= self.mensagem, 
        timestamp= "0000-00-00 00000000000"
      )