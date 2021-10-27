from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

app = Flask(__name__)
db = SQLAlchemy(app)

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    config = Column(JSONB)

    def __repr__(self):
        return '<User %r>' % self.name

class Populate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    world_id = Column(Integer, ForeignKey(World.id), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    config = db.Column(JSONB)

    def __repr__(self):
        return '<Populate %r>' % self.name

class Writing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    populate_id = Column(Integer, ForeignKey(World.id), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    config = db.Column(JSONB)
    story = db.Column(Text(4294000000))
    def __repr__(self):
        return '<Story %r>' % self.name


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

@app.route("/generate/new/")
def generate():
    gen = "generate"
    name ="generate"
    return render_template(
    'wb/genworld.html', name=name,gen=gen)


@app.route("/populate/")
def newworld():
    gen = "populate"
    name ="populate"
    return render_template(
    'wb/popworld.html', name=name,gen=gen)


@app.route("/worlds/:name/")
def getWorlds(name):
    gen = "read"
    name ="read"
    return render_template(
    'wb/worlds.html',name=name, gen=gen)

if __name__ == "__main__":
    app.run()
