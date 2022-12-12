import os

from flask import Flask, render_template  # Remove: import Flask

from src.requests import requests
from src.server_status import server_status

app = Flask(__name__)
app.register_blueprint(server_status)
app.register_blueprint(requests)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=os.environ.get('PORT', 8080),
        debug=True
    )
