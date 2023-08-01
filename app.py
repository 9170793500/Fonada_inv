
from flask import Flask, flash, render_template, request, url_for,  redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


app = Flask(__name__, template_folder='templats')
app.secret_key = user = {
    "username": "fonada@125.com", "password": "fonada@123"}


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sdm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sdm'
db = SQLAlchemy(app)


class System_inventry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    divice_name = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(100), nullable=True)
    charger_serialnum = db.Column(db.String(100), nullable=False)
    mouse_serialnum = db.Column(db.String(100), nullable=False)
    extra_device = db.Column(db.String(100), nullable=False)
    assign = db.Column(db.String(20), nullable=False)
    assign_date = db.Column(db.String(20), nullable=False)


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
    quntity = db.Column(db.String(200), nullable=False)


@app.route("/system_inventry", methods=['GET', 'POST'])
def contact():

    if (request.method == 'POST'):
        divice_name = request.form.get('divice_name')
        storage = request.form.get('storage')
        serial_number = request.form.get('serial_number')
        ram = request.form.get('ram')
        charger_serialnum = request.form.get('charger_serialnum')
        mouse_serialnum = request.form.get('mouse_serialnum')
        extra_device = request.form.get('extra_device')
        assign = request.form.get('assign')
        assign_date = request.form.get('assign_date')
        entry = System_inventry(divice_name=divice_name, storage=storage, serial_number=serial_number,
                                ram=ram, charger_serialnum=charger_serialnum, mouse_serialnum=mouse_serialnum,
                                extra_device=extra_device, assign=assign, assign_date=assign_date)
        db.session.add(entry)
        db.session.commit()
    return render_template('system_inventry.html')


@app.route("/campaign")
def campian():
    system_inventry = System_inventry.query.filter_by().all()[0:10]
    return render_template("campaign.html", system_inventry=system_inventry  )


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
    total = db.session.query(func.sum(Stock.quntity)).scalar()
    total = total or 0
    total_sno = db.session.query(func.count(Stock.sno)).scalar()
    total_item = db.session.query(func.count(System_inventry.assign)).scalar()
    print(total_item)
    quntity = db.session.query(func.count(Mouse.quntity)).scalar()
    quntity = quntity or 0
    
    mouse = Mouse.query.filter_by().all()[0:10]
    stock = Stock.query.filter_by().all()[0:10]
    # , stock =stock
    return render_template("dashboard.html", stock=stock, mouse=mouse, total_sno=total_sno, total=total, quntity=quntity,total_item=total_item)


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
        device_name = request.form.get('device_name')
        brand = request.form.get('brand')
        serial_number = request.form.get('serial_number')
        quntity = request.form.get('quntity')
        mouse = Mouse(device_name=device_name, brand=brand,
                      serial_number=serial_number, quntity=quntity)
        db.session.add(mouse)
        db.session.commit()
    return render_template("mouse_add.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
