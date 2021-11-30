from os import environ 
import sys
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
db = SQLAlchemy(app)

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    config = db.Column(JSONB)

    def __repr__(self):
        return '<User %r>' % self.name

class Populate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    world_id = db.Column(db.Integer, db.ForeignKey(World.id))
    name = db.Column(db.String(80))
    creator =db.Column(db.String(80))
    config = db.Column(JSONB)

    def __repr__(self):
        return '<Populate %r>' % self.name

class Writing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    populate_id = db.Column(db.Integer, db.ForeignKey(Populate.id))
    name = db.Column(db.String(80))
    creator =db.Column(db.String(80))
    config = db.Column(JSONB)
    story = db.Column(db.Text)
    def __repr__(self):
        return '<Story %r>' % self.name


@app.route("/")
def index():
    #db.session.query(World).delete()
    #db.session.commit()

    gen = "generate"
    resdata ={}
    worlds = World.query.all()
    name ="wah"
    for w in worlds:
            resdata[w.id] = w.name
    return render_template('wb/index.html',worlds=resdata, name=name,gen=gen) #build world or #choose world

def generate(request):
    gen = "generate"
    name ="generate"
    msg = ""
    id = 0
    resdata ={}
    if request.method == 'POST': 
        newdata ={}
        data = request.form
        name= request.form["name"] or "untitled"
        for d in data.keys():
            if len(data[d]) > 0:
                if "category" in d:
                    number = int(d.replace('category',''))
                    category = data[d]
                    options = data["options%d" % number]
                    if category != "":
                        newdata[category] = options
                        
            world = World(name=name, config=newdata)
            db.session.add(world)
            db.session.commit()
            id = world.id
        else: 
            msg = "pick a world"

       # worlds = World.query.all()
       # for w in worlds:
       #     resdata[w.id] = {"id":w.id,"name":w.name,"data":w.config}
    
     #filter(User.email.endswith('@example.com')).all()
    return id


@app.route("/populate/<world_id>/", methods=['GET', 'POST'])
def newworld(world_id):
    resdata ={}
    
    if request.method == 'POST': 
        newdata ={"cat":{},"all":{}} 
        data = request.form
        name= request.form["name"] or "untitled world from %s" % world_id
        print(data)
        print(data.keys())
        for d in data.keys():
            if len(data[d]) > 0:
                if d[0] == "i":
                    n = d[2:len(d)]
                    option = n.split("_")[0]
                    pb1= data["c_%s" % option]
                    pb2= data["pb_%s" % n]
                    if pb1 not in newdata["cat"]:
                        newdata["cat"][pb1] =[]
                    if pb2 not in newdata["all"]:
                        newdata["all"][pb2] =[]   
                    val = {data["c_%s" % option]:data[d]}    
                    newdata["cat"][pb1].append(val)
                    newdata["all"][pb2].append(val)
                        
        world = Populate(name=name, world_id=world_id,config=newdata,creator="")
        db.session.add(world)
        db.session.commit()
        id = world.id
     else:   
        try:
            world = Populate.query.get(world_id)
        except:
            index()
    return render_template(
        'wb/popworld.html', name=name,config=world.config, world_id=world.world_id)
    

@app.route("/story/<populate_id>/")
def story(populate_id):
    msg = ""
    gen = "populate"
    if request.method == 'POST': 
        data = request.form
        name= request.form["name"] or "piece from %s" % populate_id
        story = data["story"]
        config = {}
        for d in data.keys():
                if d[0] == "c":
                    count = data[d+"_c"]
                    n = d[2:len(d)]
                    link = data[d[0]]
                    config[count] = {n:link}
                    


        world = Writing(name=name, populate_id=populate_id,config=data,creator="",story=story)
        db.session.add(world)
        db.session.commit()
    else:
        try:
            w = Writing.query.get(populate_id)
        except:
            index()
    return render_template(
    'wb/story.html', name=name,gen=gen,data=world.config,story=world.story)


@app.route("/world/<id>/", methods=['GET', 'POST'])
def getWorlds(id):
    gen = "read"
    name ="read"
    resdata ={}
    if (id == "new"):
        id =generate(request)
    w = World.query.get(id)
    name = w.name
    gen = {"id":w.id,"name":w.name,"data":w.config, "cat":", ".join(list(w.config.keys()))}
        
    return render_template(
    'wb/genworld.html',name=name, gen=gen)

if __name__ == "__main__":
    #   db.create_all() 
    app.run()
