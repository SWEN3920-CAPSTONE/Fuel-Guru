"""
Driver for the server for Fuel Guru.

"""

from config import app

if __name__ == '__main__':
    app.run(debug=app.config.get('IS_DEV'), host=app.config.get(
        'HOST'), port=app.config.get('PORT'), )
