import os
from main import app


## ----------------------------------------------------------
## configuração de IP e porta
## ----------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, use_reloader=False,host='0.0.0.0', port=port)