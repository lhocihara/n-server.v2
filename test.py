import requests, json

headers = {'content-type': 'application/json; charset=utf-8'}
data = {
    "nome_completo": "Ragnar Lothbrok",
    "cpf": "39008867890",
    "data_nasc": "1997-10-27T00:00:00.000Z",
    "genero": "D",
    "email": "Sif@gmail.com",
    "senha": "75f7313c20144e39edcf57a14733d074aee0c482320d5178ee0ef2f2608c2996"
}
for i in range(0,100):
    
    r = requests.post("http://n-server-v2.herokuapp.com/pessoa", data=json.dumps(data),headers=headers)
    print (r.text)