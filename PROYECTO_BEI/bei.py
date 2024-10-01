from flask import Flask, render_template, request, redirect, session,  url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json

import os
 
app = Flask(__name__)

#Conexión a mysql

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'beiweb'
app.config['MYSQL_PASSWORD'] = 'syntaxis'
app.config['MYSQL_DB'] = 'bei'
mysql = MySQL(app)
     





# configuraciones para la conexión
app.secret_key = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')#Ruta para el home signup
def index():
   return render_template('index.html')

@app.route('/signup', methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form ['name']
        email = request.form ['email']
        password = request.form ['password']
        direccion = request.form ['direccion']
        telefono = request.form ['telefono']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM signup WHERE email = %s', (email,))
        
        if cursor.fetchone():
            flash('⚠️ Este email ya está registrado')
            return redirect(url_for('signup'))
        cursor.execute('INSERT INTO signup (name, email, password, direccion, telefono) VALUES (%s, %s, %s, %s, %s)', (name, email, password, direccion, telefono))

        mysql.connection.commit()
        flash('✅ Cuenta creada satisfactoriamente')
        return redirect(url_for('login'))
    return render_template('01-SIGN_UP.html')

@app.route('/usuarios') #Mostrar los datos de usuarios en la tabla 
def mostrar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM signup')
    datos = cur.fetchall()
    print('datos')
    return render_template('usuarios.html', signup = datos)


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
      flash('✅ Mensaje enviado satisfactoriamente')
      return redirect(url_for('conozcanos'))
   
@app.route('/mensajes') #Mostrar los datos de usuarios en la tabla 
def mostrar_mensajes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactus')
    data = cur.fetchall() #data es igual a todos los datos de la BD
    return render_template('mensajes.html', mensajes = data) #la variablE mensajes va a contener los datos que tiene data entonces en jinja

@app.route('/carrito') 
def carrito():
    # if 'user' in session:
        return render_template('09-CARRITO.html')
    # else:
    #     flash('⚠️ Debe logearse para ver su carrito')
        return redirect(url_for('login'))

@app.route('/añadir_al_carrito/<int:producto_id')
def añadir_al_carrito(producto_id):
    connection = MySQL()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id))
        producto = cursor.fetchone()
        cursor.close()
        connection.close()

        if producto:
            carrito = session.get('carrito', {})
            if str(producto_id) in carrito:
                if carrito[str(producto_id)]['cantidad'] < producto['cantidad']:
                    carrito[str(producto_id)]['cantidad'] += 1
                    flash(f"añadiste {producto['nombre']}' en el carrito", 'success')
                else:
                    flash(f"no tenemos suficiente cantidad de{['nombre']}", 'warning')
            else:
                carrito[str(producto_id)] = {
                    'nombre': producto['nombre'],
                    'precio': float(producto['precio']),
                    'cantidad': 1
                }
                flash(f"Añadiste {producto['nombre']} al carrito", 'success')
            session['carrito'] = carrito
        else:
            flash(f"No encontramos el producto", 'danger')
    else:
        flash(f"No conectamos con la basedata", 'danger')
    return redirect(url_for('index'))


@app.route('/pago') 
def pago():
    if 'user' in session:
        return render_template('13-PAGO.html')
    else:
        flash('⚠️ Debe logearse para realizar una compra')
        return redirect(url_for('login'))
    

@app.route('/factura') 
def factura():
    if 'user' in session:
        return render_template('11-FACTURA.html')
    else:
        flash('⚠️ Debe logearse para realizar una compra')
        return redirect(url_for('login'))

@app.route('/producto') 
def producto():
    return render_template('08-PRODUCT.html')

@app.route('/signup_a', methods=['GET', 'POST'])
def signup_a():
 if request.method == 'POST':
        name = request.form ['name']
        email = request.form ['email']
        password = request.form ['password']
        tipo = request.form ['tipo']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO signup (name, email, password, tipo) VALUES (%s, %s, %s, %s)', (name, email, password, tipo))
        mysql.connection.commit()
        flash('¡Usuario creado!')
        return redirect(url_for('signup_a'))
 return render_template('14-signup_a.html')

@app.route('/cambio_contraseña')
def cambio_contraseña():
    return render_template('05-CAMBIO_DE_CONTRASEÑA.html')

#Subir productos

@app.route('/subir_producto', methods= ['GET','POST'])
def subir_producto():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        descripcion = request.form ['descripcion']
        precio = request.form ['precio']
        cantidad = request.form ['cantidad']
        imagen = request.files.get ['imagen']
        if imagen and imagen.filename:
            if not allowed_file(imagen.filename):
                flash('Solo están permitidos archivos JPG y PNG')
                return redirect(url_for('subir_producto'))
            
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre, descripcion, precio, cantidad, imagen) VALUES (%s, %s, %s, %s, %s)', (nombre, descripcion, precio, cantidad, imagen))
        mysql.connection.commit()
        flash('✅ ¡Producto subido!')
        return redirect(url_for('inventario'))
    return render_template('subir_producto.html')

# Seguridad

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
    
@app.route('/homeadmin')
def homeadmin():
    return render_template('homeadmin.html')


if __name__=='__main__':
 app.run(debug=True)