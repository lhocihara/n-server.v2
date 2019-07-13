# -*- coding: utf-8 -*-
from flask import jsonify

class RespostasAPI:
  def __call__(self, mensagem_resposta, objeto=None):    
    self.codigo = 201
    self.mensagem = mensagem_resposta
    self.objeto = objeto    
    
    return self.retorno()
  
  def retorno(self):
    print("\n[Status retorno] JSON de retorno:\n" + str({
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