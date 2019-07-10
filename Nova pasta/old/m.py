from flask import Flask, jsonify, request

app = Flask(__name__)
##Definição do endpoint - NÃO FUNCIONA AINDA
@app.route("/hi")
def boas_vindas():
    return jsonify({"message": "eae meu!"})