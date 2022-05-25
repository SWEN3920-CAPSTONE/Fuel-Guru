from config import app,db, UserType

if __name__ == '__main__':
    if len(db.session.query(UserType).all()) == 0:
        # run seed if db is empty
        import seed
        
    app.run(debug=app.config.get('IS_DEV'), host=app.config.get(
        'HOST'), port=app.config.get('PORT'))
