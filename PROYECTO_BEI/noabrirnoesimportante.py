from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'syntax',
    'password': 'syntax',
    'database': 'bei',
}

@app.route('/')
def formulario():
    return render_template('01-SIGN_UP.html')

def insertar_usuario(name, email, password, direccion, telefono):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO signup (name, email, password, direccion, telefono) VALUES (%s, %s, %s, %s, %s)', (name, email, password, direccion, telefono))
        conn.commit()
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        flash('Error al insertar usuario')
    finally:
        conn.close()



def obtener_usuarios():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, direccion, telefono FROM signup')
        usuarios = cursor.fetchall()
        return usuarios
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Error al obtener los usuarios.')
        return []
    finally:
        conn.close()
        

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    name = request.form ['name']
    email = request.form ['email']
    password = request.form ['password']
    direccion = request.form ['direccion']
    telefono = request.form ['telefono']

    if not name or not email or not password:
        flash('Los campos son obligatorios')
        return redirect(url_for('01-SIGN_UP'))
    insertar_usuario(name, email, password, direccion, telefono)
    return redirect(url_for('exito')) #HACER UN TEMplate de EXITO



@app.route('/usuarios')
def mostrar_usuarios():
    usuarios = obtener_usuarios()
    return render_template('usuarios.html', usuarios=usuarios) #Template tabla de usuarios



@app.route('/eliminar_usuario/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM signup WHERE id = %s', (id,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        flash('Error al eliminar usuario')
    finally:
        conn.close()
    return redirect(url_for('mostrar_usuarios'))


@app.route('/actualizar_usuario/<int:id>', methods=['GET'])
def mostrar_formulario_actualizar_usuario(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT name, email, password, direccion, telefono FROM signup WHERE id = %s', (id,))
        usuario = cursor.fetchone()
    except mysql.connector.Error as error:
        print(f'Error: {error}')
        flash('Error al obtener datos de usuario')
        usuario = None
    finally:
        conn.close()
    if usuario:
        return render_template('actualizar_usuario.html', id=id, nombre=usuario[0], email=usuario[1]) #Esto debe redirigir a la tabla de usuarios
    else:
        return redirect(url_for('mostrar_usuarios'))

    
@app.route('/actualizar_usuario/<int:id>', methods=['POST'])
def actualizar_usuario(id):

    nuevo_nombre = request.form['nuevo_nombre']
    nuevo_email = request.form['nuevo_email']
    nueva_contrasena = request.form['nueva_contrasena']
    nueva_direccion = request.form ['nueva_direccion']
    nuevo_telefono = request.form['nuevo_telefono']

    if not nuevo_nombre or not nuevo_email or not nueva_contrasena or not nueva_direccion or not nuevo_telefono:
        flash('Los campos son obligatorios')
        return redirect(url_for('mostrar_formulario_actualizar_usuario'), id=id)

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('UPDATE signup SET nombre =%s, email =%s, contrasena =%s direccion =%s, telefono =%s, WHERE id =%s', (nuevo_nombre, nuevo_email, nueva_contrasena, nueva_direccion, nuevo_telefono, id,))
        usuario = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        flash('Error al obtener datos de usuario')
    finally:
        conn.close()
    return redirect(url_for('mostrar_usuarios'))

@app.route('/exito')
def exito():
    return render_template('exito.html')

if __name__=='__main__':
 app.run(debug=True)