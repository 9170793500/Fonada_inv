
import datetime
from flask import Flask, flash, jsonify, render_template, request, url_for,  redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS



app = Flask(__name__, template_folder='templats')
app.secret_key = user = {
    "username": "fonada@125.com", "password": "fonada@123"}


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sdm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sdm'
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
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
 


class Crpm(db.Model):
        transactionId = db.Column(db.String,primary_key=True)
        recpient = db.Column(db.String(1000), nullable=False)
        sender = db.Column(db.String(1000), nullable=False)
        description = db.Column(db.String(1000), nullable=False)
        totalPdu = db.Column(db.String(1000), nullable=False)
        deliverystatus = db.Column(db.String(1000), nullable=False)
        deliverydt = db.Column(db.String(500), nullable=False)
        submitdt = db.Column(db.String(500), nullable=False)
        corelationId = db.Column(db.String(1000), nullable=False)
        message = db.Column(db.String(1000), nullable=False)


class Stock(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    Specification = db.Column(db.String(500), nullable=False)
    sr_number = db.Column(db.String(100), nullable=False)
    other_device = db.Column(db.String(50), nullable=False)
    quntity = db.Column(db.String(100), nullable=False)


class Mouse(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)


@app.route('/api/get_sms', methods=['GET'])
def get_sms():
    sms_list = []

    sdm = Crpm.query.all()

    for entry in sdm:
        sms_list=({
            'transactionId': entry.transactionId,
            'recipient': entry.recpient,
            'sender': entry.sender,
            'description': entry.description,
            'totalPdu': entry.totalPdu,
            'deliverystatus': entry.deliverystatus,
            'deliverydt': entry.deliverydt,
            'submitdt': entry.submitdt,
            'corelationId': entry.corelationId,
            'message': entry.message
        })

    print('transactionId')
    return jsonify(sms_list)


@app.route('/api/add_sms', methods=['POST'])
def add_sms():
    if request.method == 'POST':
        data = request.json
        
        sms = Crpm(
            transactionId=data.get('transactionId'),
            recpient=data.get('recpient'),
            sender=data.get('sender'),
            description=data.get('description'),
            totalPdu=data.get('totalPdu'),
            status=data.get('status'),
            doneDate=data.get('doneDate'),
            submittedDate=data.get('submittedDate'),
            corelationid=data.get('corelationid'),
            message=data.get('message')
        )
        
        db.session.add(sms)
        db.session.commit()
        
        return jsonify({'message': 'Crpm data added successfully'})
    



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

@app.route("/api/update_inventory/<int:sno>", methods=['POST'])
def update_inventory_item(sno):
    if request.method == "POST":
        item = System_inventry.query.get(sno)
        data = request.json
        item.device_name = data['device_name']
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

@app.route("/", methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            flash('This is a flash message')
            return redirect('/dashboard')

        flash(u'Invalid username  password')

        return render_template("login.html")
    return render_template("login.html")


@app.route("/layout")
def layout():
    return render_template("layout.html")


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


@app.route("/dashboard")
def dashboard():
    total = db.session.query(func.sum(Stock.quantity)).scalar()
    total = total or 0
    total_sno = db.session.query(func.count(Stock.sno)).scalar()
    total_item = db.session.query(func.count(System_inventry.assign)).scalar()

    quntity = db.session.query(func.count(Mouse.quantity)).scalar()
    quntity = quntity or 0

    mouse = Mouse.query.filter_by().all()[0:10]
    stock = Stock.query.filter_by().all()[0:10]
    # , stock =stock
    return render_template("dashboard.html", stock=stock, mouse=mouse, total_sno=total_sno, total=total,  total_item=total_item)


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


# @app.route("/stock_add", methods=['GET', 'POST'])
# def stock_add():
#     if (request.method == 'POST'):
#         name = request.form.get('name')
#         brand = request.form.get('brand')
#         Specification = request.form.get('Specification')
#         sr_number = request.form.get('sr_number')
#         other_device = request.form.get('other_device')
#         quntity = request.form.get('quntity')

#         add_stock = Stock(name=name, brand=brand, Specification=Specification,
#                           sr_number=sr_number, other_device=other_device, quntity=quntity)
#         db.session.add(add_stock)
#         db.session.commit()
#     return render_template("stock_add.html")


# @app.route("/mouse_add", methods=['GET', 'POST'])
# def mouse_add():

#     if (request.method == 'POST'):
#         data = request.get_json()
#         device_name = request.form.get('device_name')
#         brand = request.form.get('brand')
#         serial_number = request.form.get('serial_number')
#         quntity = request.form.get('quntity')
#         mouse = Mouse(device_name=device_name, brand=brand,
#                       serial_number=serial_number, quntity=quntity)
#         db.session.add(mouse)
#         db.session.commit()
#     return render_template("mouse_add.html", data=data)
    # return jsonify(message="Data added successfully" , data=data)



if __name__ == '__main__':
   
    app.run(debug=True, port=8000)
