
from flask import Flask, flash,render_template,request,  redirect, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templats')
app.secret_key = user = {"username": "fonada@125.com", "password": "fonada@123"}
  

# local_server = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sdm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sdm'
db = SQLAlchemy(app)


class System_inventry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    divice_name = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.String(100), nullable=False)
    serial_number= db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(100), nullable=True)
    charger_serialnum = db.Column(db.String(100), nullable=False)
    mouse_serialnum = db.Column(db.String(100), nullable=False)
    extra_device = db.Column(db.String(100), nullable=False)
    assign = db.Column(db.String(20), nullable=False)
    assign_date = db.Column(db.String(20), nullable=False)


@app.route("/system_inventry", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
    
        divice_name = request.form.get('divice_name')
        storage = request.form.get('storage')
        serial_number = request.form.get('serial_number')
        ram = request.form.get('ram')
        charger_serialnum = request.form.get('charger_serialnum')
        mouse_serialnum = request.form.get('mouse_serialnum')
        extra_device = request.form.get('extra_device')
        assign = request.form.get('assign')
        assign_date = request.form.get('assign_date')
        entry = System_inventry( divice_name= divice_name, storage = storage, serial_number = serial_number,
                                 ram=  ram,charger_serialnum = charger_serialnum, mouse_serialnum=mouse_serialnum,
                                  extra_device=extra_device , assign=assign , assign_date=assign_date)
        db.session.add(entry)
        db.session.commit()
    return render_template('system_inventry.html')



@app.route("/", methods = ['POST', 'GET'])
def login():
      if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:
            session['user'] = username
            flash('This is a flash message')
            return redirect('/dashboard')
        
        flash(u'Invalid username  password')
        
        return  render_template("login.html" )
      return  render_template("login.html" )

@app.route("/layout")
def layout():
      return render_template("layout.html")
@app.route("/update")
def update():
      return render_template("update.html")
      
@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')


@app.route("/dashboard")
def dashboard():
    return  render_template("dashboard.html")


@app.route("/campaign")
def campian():
     system_inventry = System_inventry.query.filter_by().all()[0:10]
     return  render_template("campaign.html" ,system_inventry=system_inventry)


if __name__ == '__main__':
  app.run(debug=True , port=8000 )
