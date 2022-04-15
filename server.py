
from config import app, db


if __name__ == '__main__':                              
    print(app.url_map)
    app.run(debug=app.config.get('DEBUG_ON'), host=app.config.get(
        'HOST'), port=app.config.get('PORT'))
