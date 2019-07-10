from create_app import app
import os
app.run(debug=False, use_reloader=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)