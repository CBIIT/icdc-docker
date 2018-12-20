from pidgin.app import app

app.config['API_URL'] = 'http://localhost/v0/submission/graphql/' # peregrine endpoint
app.run('127.0.0.1', 5000, debug=True)
