from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ccdb'

mysql = MySQL(app)


@app.route('/')
def emailformrender():
   return render_template('EmailForm.html')


@app.route('/email', methods=['POST'])
def emailcheck():
   email = request.form['Email']
   
   cur = mysql.connection.cursor()
   cur.execute("SELECT * FROM customers where Email=%s", (email,))
   items = cur.fetchall()

   mysql.connection.commit()
   cur.close()

   if items == ():
      return redirect(url_for('form', email=email))
   else:
      return redirect(url_for('returnerquestion', email=email))


@app.route('/form/<email>')
def form(email):
   return render_template('CustomerForm.html', email=email)


@app.route('/returnerquestion/<email>')
def returnerquestion(email):
   return render_template('EditInfo.html', email=email)


@app.route('/updateform/<email>')
def updateform(email):
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM customers where Email=%s', (email,))
   customer = cur.fetchall()[0]

   mysql.connection.commit()
   cur.close()

   return render_template('UpdateForm.html', values=customer)


@app.route('/result', methods=['POST'])
def result():
   firstName = request.form['FirstName']
   lastName = request.form['LastName']

   streetName = request.form['StreetAddress']
   city = request.form['City']
   state = request.form['State']
   zipCode = request.form['ZipCode']

   if 'Discounts' in request.form:
      discounts = 1
   else:
      discounts = 0

   phone = request.form['Phone']
   email = request.form['Email']

   cur = mysql.connection.cursor()
   cur.execute("SELECT * FROM geography where PostalCode=%s limit 1", (zipCode,))
   geo = cur.fetchall()

   if geo == ():
      geoKey = None
   else:
      geoKey = geo[0][0]

   cur.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (None, geoKey, '', firstName, '', lastName, '', '', '', '', None, None, None, '', '', None, None, '', '', None, phone, email, streetName, city, state, zipCode, discounts))
   mysql.connection.commit()
   cur.close()

   return redirect(url_for('success'))


@app.route('/update/<origemail>', methods=['POST'])
def update(origemail):
   firstName = request.form['FirstName']
   lastName = request.form['LastName']

   streetName = request.form['StreetAddress']
   city = request.form['City']
   state = request.form['State']
   zipCode = request.form['ZipCode']

   if 'Discounts' in request.form:
      discounts = 1
   else:
      discounts = 0

   phone = request.form['Phone']
   email = request.form['Email']

   cur = mysql.connection.cursor()
   cur.execute("UPDATE customers SET FirstName=%s, LastName=%s, StreetAddress=%s, City=%s, State=%s, ZipCode=%s, Agreement=%s, Email=%s, PhoneNumber=%s WHERE Email=%s", (firstName, lastName, streetName, city, state, zipCode, discounts, email, phone, origemail))

   mysql.connection.commit()
   cur.close()

   return redirect(url_for('returner'))


@app.route('/success')
def success():
   return render_template('Confirmation.html')


@app.route('/returner')
def returner():
   return render_template('ReturnerConfirmation.html')


if __name__ == '__main__':
   app.run(debug = True)