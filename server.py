
from config import app

if __name__ == '__main__':    
    app.run(debug=app.config.get('DEBUG_ON'), host=app.config.get(
        'HOST'), port=app.config.get('PORT'))
