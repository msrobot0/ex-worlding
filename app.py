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
    gen = "index"
    name = "index"
    return render_template('wb/index.html',worlds={}, name=name,gen=gen) #build world or #choose world

@app.route("/world/", methods=['POST'])
def new_world():
    gen = "read"
    name ="read"
    data = request.form
    newdata = {}
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
    world_id = world.id
    print(world_id)  
    name = world.name
    gen = {"id":world.id,"name":world.name,"data":world.config, "cat":", ".join(list(world.config.keys()))}
        
    return render_template(
    'wb/genworld.html',name=name, gen=gen,allworlds=[])

@app.route("/world/<world_id>/", methods=['GET'])
def get_world(world_id):
    gen = "read"
    name ="read"
    print("hi");
    print(world_id)
    resdata ={}
    w = World.query.get(world_id)
    name = w.name
    gen = {"id":w.id,"name":w.name,"data":w.config, "cat":", ".join(list(w.config.keys()))}
        
    return render_template(
    'wb/genworld.html',name=name, gen=gen,allworlds=[])

@app.route("/populate/", methods=['POST'])
def new_populated_world():
    if request.method == 'POST': 
        gen = "new populated world"
        world_id = request.form['world_id']
        newdata ={"world":{},"all":[]} 
        data = request.form
        name= request.form["name"] or "untitled world from %s" % world_id
        print (data)
        for d in data.keys():
            if len(data[d]) > 0:
                if d[0] == "c":
                    new_group = {}
                    names = d.split("_")
                    cat = names[1]
                    items = int(names[-1])
                    pb =data["pb_%s_0" % cat]
                    for i in range(0,items):
                        new_group= {"cat":cat,"items":items,"pb":pb,"item":data["i_%s_%s"%(cat,i)],"itempb":data["pb_%s_%s"%(cat,i)]}
                        newdata["all"].append(new_group)
                        if pb not in newdata["world"]:
                            newdata["world"][pb] = []
                        newdata["world"][pb].append(new_group)
                        
        world = Populate(name=name, world_id=world_id,config=newdata,creator="")
        db.session.add(world)
        db.session.commit()
        
        name = World.query.get(world_id).name    
        return render_template(
        'wb/popworld.html', gen=gen, name=name,config=world.config, populate_id=world.id,world_id=world_id)


@app.route("/populate/<world_id>/", methods=['GET'])
def get_populated_world(world_id):
    gen = "get populated world"
    world = Populate.query.get(world_id)
    name = World.query.get(world.world_id).name
    return render_template(
        'wb/popworld.html', gen=gen, name=name,config=world.config, populate_id=world.id,world_id=world_id)

 
@app.route("/story/", methods=["POST"])
def new_story():    
    if request.method == 'POST': 
        gen = "new story"
        data = request.form
        story = data["story"]
        populate_id = data["populate_id"]
        color1 = data["color1"]
        color2 = data["color2"]
        
        populate = Populate.query.get(populate_id)
        config = populate.config
        name= " ".join(story[:25].split(" ")[0:-2])
        world = Writing(name=name, populate_id=populate_id,config={"world_id":populate.world_id,"color1":color1,"color2":color2,"config":config},creator="",story=story)
        populate_id = world.id
        db.session.add(world)
        db.session.commit()
        name = world.name
        return render_template(
    'wb/worlds.html', name=name,gen=gen,config=world.config,story=world.story,populate_id=world.populate_id)


@app.route("/story/<populate_id>/", methods=["GET"])
def get_story(populate_id):
    gen = "get story"
    world = Writing.query.get(populate_id)
    name = world.name
    return render_template(
    'wb/worlds.html', name=name,gen=gen,config=world.config,story=world.story)


@app.route("/read/", methods=["GET"])
def read_all():
    w = Writing.query.all()
    stories = {}    
    
    for ww in w:
        world_id = ww.config["world_id"] 
        name = ww.name
        if world_id not in stories: 
            stories[world_id] = {"name":name,"stories":[]}
        stories[world_id]["stories"].append({"name":name,"id":ww.id})
        print(stories)
    return render_template(
    'wb/allworlds.html', allworlds=stories)

@app.route("/read/<story_id>/", methods=['GET'])
def read_one(story_id):
    gen = "read one"

    world = Writing.query.get(story_id)
    name = world.name
    
    return render_template(
'wb/worlds.html', name=name,gen=gen,config=world.config,story=world.story)


if __name__ == "__main__":
    #db.create_all() 
    app.run()
