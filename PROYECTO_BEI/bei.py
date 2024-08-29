from flask import Flask, render_template, request, redirect, session,  url_for, flash # config
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#Conexión a mysql
app.config['user'] = 'localhost'
app.config['MYSQL_USER'] = 'syntax'
app.config['MYSQL_PASSWORD'] = 'syntax'
app.config['MYSQL_DB'] = 'bei'
mysql = MySQL(app)

# configuraciones para la conexión
app.secret_key = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')#Ruta para el home signup
def index():
   return render_template('index.html')

@app.route('/signup') 
def signup():
    return render_template('01-SIGN_UP.html')

@app.route('/usuarios') #Mostrar los datos de usuarios en la tabla 
def mostrar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM signup')
    datos = cur.fetchall()
    print('datos')
    return render_template('usuarios.html', signup = datos)

      
@app.route('/add_usuario', methods= ['POST']) #Añadir usuarios en el formulario
def add():
   if request.method == 'POST':
      name = request.form ['name']
      email = request.form ['email']
      password = request.form ['password']
      direccion = request.form ['direccion']
      telefono = request.form ['telefono']
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO signup (name, email, password, direccion, telefono) VALUES (%s, %s, %s, %s, %s)', (name, email, password, direccion, telefono))
      mysql.connection.commit()
      flash('Cuenta creada satisfactoriamente')
      return redirect(url_for('login')) #Redirecciona al signup de nuevo después de hacer el submit
    #Para empezar a guardar datos

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM signup WHERE email=%s AND password=%s', (email, password))
        user = cur.fetchone()
        if user:
            session['user'] = user[0]
            return redirect(url_for('index'))
        else:
            flash('⚠️ Nombre o contraseña incorrectos')
    return render_template('02-LOGIN.html')
      


@app.route('/editar_usuarios/<id>') #función para que en la tabla se logre editar información de la basedatos
def obtener_usuario(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM signup WHERE id = %s', [id])
   data = cur.fetchall()
   return render_template('editar_usuarios.html', usuarios = data[0]) #redirecciona al formulario de editar usuario

@app.route('/actualizar/<id>', methods = ['POST'])
def actualizar_usuario(id):
   if request.method == 'POST':
        name = request.form ['name']
        email = request.form ['email']
        password = request.form ['password']
        direccion = request.form ['direccion']
        telefono = request.form ['telefono']
        tipo = request.form ['tipo']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE signup SET name = %s, email = %s, password = %s, direccion = %s, telefono = %s, tipo = %s WHERE id = %s', (name, email, password, direccion, telefono, tipo, id))
        mysql.connection.commit()
        flash('Contacto actualizado satisfactoriamente')
        return redirect(url_for('mostrar_usuarios')) #Al terminar de editar redireccionará a la tabla de usuarios esto poniendo el def que se puso anteriormente

@app.route('/eliminar_usuario/<string:id>')
def eliminar(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM signup WHERE id = {0}'.format(id))
   mysql.connection.commit()
   flash('Contacto removido satisfactoriamente')
   return redirect(url_for('mostrar_usuarios'))

#Conexión al formulario de contacto

@app.route('/conozcanos') #Ruta para el formulario de contacto
def conozcanos():
    return render_template('12-CONOZCANOS.html')

@app.route('/add_message', methods = ['POST'])
def add_message():
   if request.method == 'POST':
      name = request.form ['name']
      email = request.form ['email']
      message = request.form ['message']
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO contactus (name, email, message) VALUES (%s, %s, %s)', (name, email, message))
      mysql.connection.commit()
      flash('Mensaje enviado satisfactoriamente')
      return redirect(url_for('conozcanos'))
   
@app.route('/mensajes') #Mostrar los datos de usuarios en la tabla 
def mostrar_mensajes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactus')
    data = cur.fetchall() #data es igual a todos los datos de la BD
    return render_template('mensajes.html', mensajes = data) #la variablE mensajes va a contener los datos que tiene data entonces en jinja

@app.route('/carrito') 
def carrito():
    return render_template('09-CARRITO.html')

@app.route('/pago') 
def pago():
    return render_template('13-PAGO.html')

@app.route('/factura') 
def factura():
    return render_template('11-FACTURA.html')

@app.route('/producto') 
def producto():
    return render_template('08-PRODUCT.html')
@app.route('/signup_a', methods=['GET', 'POST'])
def registro_a():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']  # Don't forget to get the 'rol' value from the form
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, password, rol) VALUES (%s, %s, %s)", (nombre, password, rol))
            mysql.connection.commit()
            cur.close()
            flash('¡Administrador registrado exitosamente!', 'success')
        except Exception as e:
            flash(f"Error al registrar el administrador: {e}", 'error')
        
        return redirect(url_for('signup_a'))
    
    return render_template('14-signup_a.html')


@app.route('/subir_producto') 
def subir_producto():
    return render_template('subir_producto.html')

@app.route('/cambio_contraseña')
def cambio_contraseña():
    return render_template('05-CAMBIO_DE_CONTRASEÑA.html')


# Seguridad

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
    
@app.route('/homeadmin')
def homeadmin():
    if 'nombre' in session and 'email' in session:
        return render_template('homeadmin.html')
    else:
        return redirect(url_for('02-LOGIN.html'))


if __name__=='__main__':
 app.run(debug=True)
