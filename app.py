from __init__ import app
from waitress import serve

if __name__ == '__main__':
    # app.run(debug=False, port=5300)
    serve(app, port = 5300)
