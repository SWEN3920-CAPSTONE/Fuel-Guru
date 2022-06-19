from config import app, db

if __name__ == '__main__':       
    app.run(debug=app.config.get('IS_DEV'), host=app.config.get(
        'HOST'), port=app.config.get('PORT'), )
