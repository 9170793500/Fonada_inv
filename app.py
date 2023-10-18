

import bcrypt
import datetime
from flask import Flask, flash, jsonify, make_response, render_template, request, url_for,  redirect, session
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
import requests
from sqlalchemy import func


app = Flask(__name__, template_folder='templats')

# app.secret_key = user = {
#     "username": "fonada@125.com", "password": "fonada@123"}


app.secret_key ='secret_key'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sdm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sdm'
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class System_inventry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    storage = db.Column(db.String(20), nullable=False)
    serial_number = db.Column(db.String(20), nullable=False)
    ram = db.Column(db.String(20), nullable=False)
    charger_serialnum = db.Column(db.String(20), nullable=False)
    mouse_serialnum = db.Column(db.String(20), nullable=False)
    extra_device = db.Column(db.String(50), nullable=False)
    assign = db.Column(db.String(50), nullable=False)
    assign_date = db.Column(db.String(20), nullable=False)
 
# class Crpm(db.Model):
#         transactionId = db.Column(db.String,primary_key=True)
#         recpient = db.Column(db.String(1000), nullable=False)
#         sender = db.Column(db.String(1000), nullable=False)
#         description = db.Column(db.String(1000), nullable=False)
#         totalPdu = db.Column(db.String(1000), nullable=False)
#         deliverystatus = db.Column(db.String(1000), nullable=False)
#         deliverydt = db.Column(db.String(500), nullable=False)
#         submitdt = db.Column(db.String(500), nullable=False)
#         corelationId = db.Column(db.String(1000), nullable=False)
#         message = db.Column(db.String(1000), nullable=False)


class Stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    Specification = db.Column(db.String(500), nullable=False)
    sr_number = db.Column(db.String(100), nullable=False)
    other_device = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)


class Mouse(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45))

    def __init__(self,username,password):
        self.username =username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def chek_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

# @app.route('/check_database')
# def check_database():

#     data = User.query.all()
#     for entry in data:
#         print(entry.id, entry.username, entry.password)

#     return "Database checked. Check your console for data."


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
    
    new = User(username=username, password=password)
    db.session.add(new)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'},200)

@app.route('/login', methods=['POST'])
def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

        user= User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = user.username
            session['password'] = user.password
            return jsonify({"massage":"login succesfully"})
        else:
            return jsonify({"massage":" unsuccesfully"}) 


    





# @app.route('/api/sms', methods=['GET'])
# def sms():
#     if request.method == 'GET':
#         transactionId = request.args.get('transactionId')
#         recpient = request.args.get('recpient')
#         sender = request.args.get('sender')
#         description = request.args.get('description')
#         totalPdu = request.args.get('totalPdu')
#         deliverystatus = request.args.get('deliverystatus')
#         deliverydt = request.args.get('deliverydt')
#         submitdt = request.args.get('submitdt')
#         corelationId = request.args.get('corelationId')
#         message = request.args.get('message')

#         item_data = Crpm.query

#         if transactionId:
#             query = item_data.filter(Crpm.transactionId == transactionId)
#         if recpient:
#             query = item_data.filter(Crpm.recpient == recpient)
#         if sender:
#             query = item_data.filter(Crpm.sender == sender)
#         if description:
#             query = item_data.filter(Crpm.description == description)
#         if totalPdu:
#             query = item_data.filter(Crpm.totalPdu == totalPdu)
#         if deliverystatus:
#             query = item_data.filter(Crpm.deliverystatus == deliverystatus)
#         if deliverydt:
#             query = item_data.filter(Crpm.deliverydt == deliverydt)
#         if submitdt:
#             query = item_data.filter(Crpm.submitdt == submitdt)
#         if corelationId:
#             query = item_data.filter(Crpm.corelationId == corelationId)
#         if message:
#             query = item_data.filter(Crpm.message == message)


#         new_entry = Crpm(
#              transactionId=transactionId,
#              recpient=recpient,
#              sender=sender,
#              description=description,
#              totalPdu=totalPdu,
#              deliverystatus=deliverystatus,
#              deliverydt=deliverydt,
#              submitdt=submitdt,
#              corelationId=corelationId,
#              message=message)
        
     
#         db.session.add(new_entry)
#         db.session.commit()
        
#         return jsonify(make_response({"payload": new_entry.to_json()}, 200))


    
# @app.route('/api/sms', methods=[ 'POST'])
# def data_add():
#     if request.method == 'POST':
#         data = request.json
#         new_entry = Crpm(
#             transactionId=data['transactionId'],
#             recpient=data['recpient'],
#             sender=data['sender'],
#             description=data['description'],
#             totalPdu=data['totalPdu'],
#             deliverystatus=data['deliverystatus'],
#             deliverydt=data['deliverydt'],
#             submitdt=data['submitdt'],
#             corelationId=data['corelationId'],
#             message=data['message']
#         )
#         db.session.add(new_entry)
#         db.session.commit()
#         return jsonify({"message": "Data added successfully"})



@app.route("/system_inventry", methods=['POST'])
def contact():
    if (request.method == 'POST'):
        device_name = request.form.get('device_name')
        storage = request.form.get('storage')
        serial_number = request.form.get('serial_number')
        ram = request.form.get('ram')
        charger_serialnum = request.form.get('charger_serialnum')
        mouse_serialnum = request.form.get('mouse_serialnum')
        extra_device = request.form.get('extra_device')
        assign = request.form.get('assign')
        assign_date = request.form.get('assign_date')
        entry = System_inventry(device_name=device_name, storage=storage, serial_number=serial_number,
                                ram=ram, charger_serialnum=charger_serialnum, mouse_serialnum=mouse_serialnum,
                                extra_device=extra_device, assign=assign, assign_date=assign_date)
        db.session.add(entry)
        db.session.commit()
    return render_template('system_inventry.html')


@app.route("/campaign")
def campian():
    system_inventry = System_inventry.query.filter_by().all()
    return jsonify(system_inventry)



@app.route('/api/system_inventry', methods=['GET'])
def get_system_inventry():
    system= System_inventry.query.all()
    data = [{'sno': item.sno,
             'device_name': item.device_name,
             'storage': item.storage,
             'serial_number': item.serial_number,
             'ram': item.ram,
             'charger_serialnum': item.charger_serialnum,
             'mouse_serialnum': item.mouse_serialnum,
             'extra_device': item.extra_device,
             'assign': item.assign,
             'assign_date': item.assign_date}
            for item in system]
    return jsonify(data)


@app.route('/api/add_inventory', methods=['POST'])
def add_system_inventory():
    if request.method == 'POST':
        data = request.json 
        new_inventory = System_inventry(
            device_name=data['device_name'],
            storage=data['storage'],
            serial_number=data['serial_number'],
            ram=data['ram'],
            charger_serialnum=data['charger_serialnum'],
            mouse_serialnum=data['mouse_serialnum'],
            extra_device=data['extra_device'],
            assign=data['assign'],
            assign_date=data['assign_date']
        )
        db.session.add(new_inventory)
        db.session.commit()
        return jsonify({'message': 'System inventory data added successfully'})
    

@app.route("/api/add_stock_mouse", methods=['POST'])
def add_mouse_stock():
    if request.method == 'POST':
        data = request.json
        item = Mouse(
            device_name=data['device_name'],
            brand=data['brand'],
            serial_number=data['serial_number'],
            quantity=data['quantity'] 
        )
       
        db.session.add(item)
        db.session.commit()
        return jsonify({'message': 'Mouse stock data added successfully'})

@app.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit(sno):
    item = System_inventry.query.filter_by(sno=sno).first()
    return render_template('edit.html', item=item, sno=sno)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def editRecord(sno):
    if request.method == "POST":
        storage = request.form.get('storage')
        serial_number = request.form.get('serial_number')
        ram = request.form.get('ram')
        charger_serialnum = request.form.get('charger_serialnum')
        mouse_serialnum = request.form.get('mouse_serialnum')
        extra_device = request.form.get('extra_device')
        assign = request.form.get('assign')
        assign_date = request.form.get('assign_date')

        item = System_inventry.query.filter_by(sno=sno).first()
        item.storage = storage
        item.serial_number = serial_number
        item.ram = ram
        item.charger_serialnum = charger_serialnum
        item.mouse_serialnum = mouse_serialnum
        item.extra_device = extra_device
        item.assign = assign
        item.assign_date = assign_date
        db.session.merge(item)
        db.session.commit()

    return campian()

@app.route("/api/get_inventory/<int:sno>", methods=['GET'])
def get_inventory_item(sno):
    item = System_inventry.query.get(sno)
    return jsonify(item)

@app.route ("/api/update_inventory/<int:sno>", methods=['POST'])
def update_inventory_item(sno):
    if request.method == "POST":
        item = System_inventry.query.get(sno)
        data = request.json
        item.device_name = data ['device_name']
        item.storage = data['storage']
        item.serial_number = data['serial_number']
        item.ram = data['ram']
        item.charger_serialnum = data['charger_serialnum']
        item.mouse_serialnum = data['mouse_serialnum']
        item.extra_device = data['extra_device']
        item.assign = data['assign']
        item.assign_date = data['assign_date']
        db.session.commit()
        return jsonify({'message': 'Inventory item updated successfully'})


# @app.route("/dashboard")
# def dashboard():
#     total = db.session.query(func.sum(Stock.quantity)).scalar()
#     total = total or 0
#     total_sno = db.session.query(func.count(Stock.sno)).scalar()
#     total_item = db.session.query(func.count(System_inventry.assign)).scalar()

#     quantity = db.session.query(func.count(Mouse.quantity)).scalar()
#     quantity = quantity or 0

#     mouse = Mouse.query.filter_by().all()[0:10]
#     stock = Stock.query.filter_by().all()[0:10]
#     # , stock =stock
#     return render_template("dashboard.html", stock=stock, mouse=mouse, total_sno=total_sno, total=total,  total_item=total_item)


@app.route('/api/stock')
def get_stock_data():
    stock_data = Stock.query.all()
    data = [{'sno': item.sno, 'name': item.name, 'brand': item.brand, 'Specification': item.Specification,
             'sr_number': item.sr_number, 'other_device': item.other_device, 'quantity': item.quantity}
            for item in stock_data]
    return jsonify(data)


@app.route('/api/mouse')
def get_mouse_data():
    mouse_data = Mouse.query.all()
    data = [{'sno': item.sno, 'device_name': item.device_name,
             'brand': item.brand, 'serial_number': item.serial_number, 'quantity': item.quantity} for item in mouse_data]
    return jsonify(data)


@app.route("/stock_add", methods=['GET', 'POST'])
def stock_add():
    if (request.method == 'POST'):
        name = request.form.get('name')
        brand = request.form.get('brand')
        Specification = request.form.get('Specification')
        sr_number = request.form.get('sr_number')
        other_device = request.form.get('other_device')
        quntity = request.form.get('quntity')

        add_stock = Stock(name=name, brand=brand, Specification=Specification,
                          sr_number=sr_number, other_device=other_device, quntity=quntity)
        db.session.add(add_stock)
        db.session.commit()
    return render_template("stock_add.html")


@app.route("/mouse_add", methods=['GET', 'POST'])
def mouse_add():

    if (request.method == 'POST'):
        data = request.get_json()
        device_name = request.form.get('device_name')
        brand = request.form.get('brand')
        serial_number = request.form.get('serial_number')
        quntity = request.form.get('quntity')
        mouse = Mouse(device_name=device_name, brand=brand,
                      serial_number=serial_number, quntity=quntity)
        db.session.add(mouse)
        db.session.commit()
    return render_template("mouse_add.html", data=data)
    return jsonify(message="Data added successfully" , data=data)










# @app.route("/", methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         if username == user['username'] and password == user['password']:
#             session['user'] = username
#             flash('This is a flash message')
#             return redirect('/dashboard')

#         flash(u'Invalid username or password')

#     return render_template("login.html")




@app.route("/contribution")
def contribution_route():
    return render_template("contribution.html")

@app.route("/media")
def media_route():
    return render_template("media.html")

@app.route("/gallery")
def gallery_route():
    return render_template("gallery.html")

@app.route("/contect")
def contect_route():
    return render_template("contect.html")


# @app.route("campaign")
# def campaign_route():
#     return render_template("campaign.html")

@app.route("/system_inventry")
def system_inventry_route():
    return render_template("system_inventry.html")


@app.route("/dashboard")
def dashboard_route():
    return render_template("dashboard.html")

@app.route("/appreciation")
def appreciation_route():
    return render_template("appreciation.html")

@app.route("/layout")
def layout_route():
    return render_template('layout.html')


@app.route('/logout')
def logout_route():
    session.pop('user')
    return redirect('/login')


# from controller import *




if __name__ == "__main__":
    app.run(debug=True, port= 8000)


