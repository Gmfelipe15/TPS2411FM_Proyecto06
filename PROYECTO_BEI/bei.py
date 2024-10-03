from flask import Flask, render_template, request, redirect, session,  url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os
"""UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
"""
app = Flask(__name__)
"""app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']= 2 * 1024 * 1024 #significa: (2mB x 1024px 1024px)"""

#Conexión a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'syntax'
app.config['MYSQL_PASSWORD'] = 'syntaxis'
app.config['MYSQL_DB'] = 'bei'
mysql = MySQL(app)

app.secret_key = 'mysecretkey' # configuraciones para la conexión
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')#Ruta para el home index.html
def index():
   return render_template('index.html')

@app.route('/signup', methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  # encripta la contraseña
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT email FROM signup WHERE email = %s', (email,))
        
        if cur.fetchone():
            flash('⚠️ Este email ya está registrado')
            return redirect(url_for('signup'))
        cur.execute('INSERT INTO signup (name, email, password, direccion, telefono) VALUES (%s, %s, %s, %s, %s)', 
                    (name, email, password, direccion, telefono))
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
        cur.execute('SELECT * FROM signup WHERE email = %s', (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[3], password):  
            session['logged_in'] = True  
            session['user_id'] = user[0]  
            session['tipo'] = user[6]  #No sé si se refiere a otro tipo de rol, o al rol que se debe llamar tipo, si no funciona entonces cambiarlo a "tipo"
            
            if session['tipo'] == 1:  #Aquí lo mismo
                flash('Inicio de sesión exitoso como administrador')
                return redirect(url_for('homeadmin'))  
            else:
                if session['tipo'] == 0:
                 flash('Inicio de sesión exitoso')
                return redirect(url_for('index')) 
        else:
            flash('⚠️ Nombre o contraseña incorrectos')
            return redirect(url_for('login'))
    
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
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('mostrar_usuarios')) #Al terminar de editar redireccionará a la tabla de usuarios esto poniendo el def que se puso anteriormente

@app.route('/eliminar_usuario/<string:id>')
def eliminar(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM signup WHERE id = {0}'.format(id))
   mysql.connection.commit()
   flash('Usuario removido satisfactoriamente')
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
def signup_a():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  
        #tipo = 0  anterior variable de tipo
        tipo = request.form['tipo'] #No se define la variable sino que según el formulario, le da el valor (1 ó 0) :p
        cur = mysql.connection.cursor()
        cur.execute('SELECT email FROM signup WHERE email = %s', (email,))
        if cur.fetchone():
            flash('⚠️ Este email ya está registrado como administrador')
            return redirect(url_for('signup_a'))

        cur.execute('INSERT INTO signup (name, email, password, tipo) VALUES (%s, %s, %s, %s)', (name, email, password, tipo))
        mysql.connection.commit()
        flash('✅ Cuenta de administrador creada satisfactoriamente')
        return redirect(url_for('login'))  
    
    return render_template('14-signup_a.html')


@app.route('/cambio_contraseña')
def cambio_contraseña():
    return render_template('05-cambibibi.html')

@app.route('/codigo_verificacion')
def codigo_verificacion():
    return render_template('04-CODIGO_DE_VERIFICACION.html')

@app.route('/verificación_exitosa')
def verificacion_exitosa():
    return render_template('06-VERIFICACION_EXITOSA.html')

@app.route('/subir_producto', methods= ['GET','POST'])
def subir_producto():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        descripcion = request.form ['descripcion']
        precio = request.form ['precio']
        cantidad = request.form ['cantidad']
        imagen = request.form ['imagen']
        disponibilidad = request.form ['disponibilidad']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre, descripcion, precio, cantidad, imagen, disponibilidad) VALUES (%s, %s, %s, %s, %s, %s)', (nombre, descripcion, precio, cantidad, imagen, disponibilidad))
        mysql.connection.commit()
        flash(f'✅ El producto {nombre} ¡ha sido añadido a la tienda!')
        return redirect(url_for('inventario'))
    return render_template('subir_producto.html')

@app.route('/eliminar_producto/<string:id>')
def eliminar_p(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
   mysql.connection.commit()
   flash('Producto removido satisfactoriamente')
   return redirect(url_for('inventario'))

@app.route('/inventario')
def inventario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    datos_p = cur.fetchall()
    print('datos')
    return render_template('10-INVENTARIO.html', producto = datos_p)

# Seguridad

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  
    session.pop('user_id', None)    
    flash('Sesión cerrada exitosamente')  
    return redirect(url_for('index'))

@app.route('/homeadmin')
def homeadmin():
    return render_template('homeadmin.html')


if __name__=='__main__':
 app.run(debug=True)
