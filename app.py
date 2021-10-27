from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)

@app.route("/")
def index():
    gen = "generate"
    worlds ={"earth":"my-earth","mars":"my-mars"}
    name ="wah"
    return render_template('wb/index.html',worlds=worlds, name=name,gen=gen) #build world or #choose world

@app.route("/read/")
def world():
    gen = "read"
    name ="read"
    return render_template(
    'wb/worlds.html', name=name,gen=gen)

@app.route("/populate/")
def newworld():
    gen = "populate"
    name ="populate"
    return render_template(
    'wb/newworld.html', name=name,gen=gen)


@app.route("/worlds/:name/")
def getWorlds(name):
    gen = "read"
    name ="read"
    return render_template(
    'wb/worlds.html',name=name, gen=gen)

if __name__ == "__main__":
    app.run()
