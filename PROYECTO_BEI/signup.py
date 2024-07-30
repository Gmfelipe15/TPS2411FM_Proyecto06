from flask import Flask, render_template, request, redirect, url_for, flash #,config
from flask_mysqldb import MySQL
import mysql.connector

#from app import obtener_usuarios

app = Flask(__name__)

#Conexión a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'syntax'
app.config['MYSQL_PASSWORD'] = 'syntax'
app.config['MYSQL_DB'] = 'bei'
mysql = MySQL(app)

# configuraciones para la conexión
app.secret_key = 'mysecretkey'

#Código original de poner la tabla de usuarios con el mismo formulario, no borrar hasta que salga todo bien
""""
@app.route('/')
def signup():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM signup')
    datos = cur.fetchall()
    print('datos')
    return render_template('01-SIGN_UP.html', signup = datos)
"""

    
@app.route('/') #Ruta para el home signup
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
      return redirect(url_for('signup')) #Redirecciona al signup de nuevo después de hacer el submit
    #Para empezar a guardar datos
      


@app.route('/editar_usuarios/<id>') #función para que en la tabla se logre editar información de la basedatos
def obtener_usuario(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM signup WHERE id = %s', (id))
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
        cur = mysql.connection.cursor()
        cur.execute('UPDATE signup SET name = %s, email = %s, password = %s, direccion = %s, telefono = %s WHERE id = %s', (name, email, password, direccion, telefono, id))
        mysql.connection.commit()
        flash('Contacto actualizado satisfactoriamente')
        return redirect(url_for('signup')) #Al terminar de editar redireccionará al formulario del signup y se actualizará la info.

@app.route('/eliminar_usuario/<string:id>')
def eliminar(id):
   cur = mysql.connection.cursor()
   cur.execute('DELETE FROM signup WHERE id = {0}'.format(id))
   mysql.connection.commit()
   flash('Contacto removido satisfactoriamente')
   return redirect(url_for('mostrar_usuarios'))

if __name__=='__main__':
 app.run(debug=True)