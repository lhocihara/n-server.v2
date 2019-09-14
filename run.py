import os
from main import app

envi_prod = True
# ----------------------------------------------------------
# configuração de IP e porta
# ----------------------------------------------------------
if __name__ == '__main__' and envi_prod:
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=port)

elif __name__ == '__main__' and not envi_prod:
    app.run(host='127.0.0.1', debug=False, use_reloader=True)
