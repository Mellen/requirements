from requirements import app

app.config.from_object('requirements.settings')
app.run()
