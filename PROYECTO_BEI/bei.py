from flask import Flask, render_template, request, jsonify, redirect, session,  url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER']= '../static/uploads'
app.config['ALLOWED_EXTENSIONS'] = 'png', 'jpg', 'jpeg'
app.config['MAX_CONTENT_LENGTH']= 2 * 1024 * 1024 #significa: (2mB x 1024px 1024px)

#Conexión a mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'syntax'
app.config['MYSQL_PASSWORD'] = 'syntaxis'
app.config['MYSQL_DB'] = 'bei'
mysql = MySQL(app)

app.secret_key = 'mysecretkey' # configuraciones para la conexión
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Estados de la conversación
conversations = {}

@app.route('/')#Ruta para el home index.html
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    vista_productos = cur.fetchall()
    return render_template('index.html', producto = vista_productos)

# Ruta para el chatbot solo la accion no hay html
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    user_id = request.remote_addr  # Usamos la IP como ID de usuario para esta aplicación

    # Reiniciar la conversación si el mensaje está vacío (cuando se accede a la página)
    if not user_message:
        # Si el usuario es nuevo, iniciamos la conversación
        if user_id not in conversations:
            conversations[user_id] = {
                'step': 0,
                'order': {}
            }
            bot_response = "¡Hola! Bienvenido/a a nuestra tienda de bolsas ecológicas Bei. ¿En qué puedo ayudarte hoy? (comprar bolsas)"
        else:
            # Si el usuario ya tiene una conversación, reiniciamos
            conversations[user_id]['step'] = 0
            bot_response = "¡Hola de nuevo! ¿En qué puedo ayudarte hoy? (comprar bolsas)"
    else:
        # Si el usuario tiene una conversación en curso
        if user_id not in conversations:
            conversations[user_id] = {
                'step': 0,
                'order': {}
            }
        
        step = conversations[user_id]['step']
        order = conversations[user_id]['order']

        # Preguntas y respuestas
        if step == 0:
            if 'comprar' in user_message.lower():
                bot_response = "¿Qué tipo de bolsa ecológica estás buscando? (algodón, yute, papel reciclado)"
                conversations[user_id]['step'] = 1
            else:
                bot_response = "Lo siento, solo te puedo ayudar a comprar bolsas ecológicas. ¿Te gustaría hacer un pedido (comprar)?"
                conversations[user_id]['step'] = 0  # Reinicia si la respuesta es diferente
        elif step == 1:
            order['tipo'] = user_message
            bot_response = "¿Cuántas bolsas te gustaría comprar?"
            conversations[user_id]['step'] = 2
        elif step == 2:
            order['cantidad'] = user_message
            bot_response = "Perfecto. ¿Qué tamaño prefieres? (pequeño, mediano, grande)"
            conversations[user_id]['step'] = 3
        elif step == 3:
            order['tamaño'] = user_message
            bot_response = "Genial. ¿Te gustaría personalizar las bolsas con un logo o diseño?"
            conversations[user_id]['step'] = 4
        elif step == 4:
            order['personalización'] = user_message
            bot_response = "¿Tienes alguna preferencia de color para las bolsas?"
            conversations[user_id]['step'] = 5
        elif step == 5:
            order['color'] = user_message
            bot_response = "Gracias. ¿Te gustaría recibir el pedido en casa o recogerlo en tienda?"
            conversations[user_id]['step'] = 6
        elif step == 6:
            order['entrega'] = user_message
            bot_response = "Por último, ¿qué método de pago prefieres? (nequi, daviplata, efectivo)"
            conversations[user_id]['step'] = 7
        elif step == 7:
            order['pago'] = user_message
            bot_response = (f"Gracias por tu pedido. Has solicitado {order['cantidad']} bolsas de tamaño {order['tamaño']} del tipo {order['tipo']} "
                            f"con personalización: {order['personalización']}, color: {order['color']}, y entrega: {order['entrega']}. "
                            f"Método de pago: {order['pago']}. ¿Deseas salir del Beibot?")
            conversations[user_id]['step'] = 8
        elif step == 8:#secuencias de los pasos
            if user_message.lower() in ['sí', 'si', 's', 'yes']:  # Aceptar diferentes variantes de "sí" al responder
                bot_response = "¡Hasta luego! Cerrando el Beibot..."
                conversations.pop(user_id)  # Eliminar la conversación después de la despedida
            else:
                bot_response = "Ok, seguiré aquí si necesitas más ayuda."

    return jsonify({'response': bot_response})

    

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
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    # if 'user' in session:
    return render_template('09-CARRITO.html')
    # else:
    #     flash('⚠️ Debe logearse para ver su carrito')
    return render_template('09-CARRITO.html')


@app.route('/añadir_al_carrito/<int:product_id>')
def añadir_al_carrito(product_id):
    connection = MySQL()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (product_id))
        producto = cursor.fetchone()
        cursor.close()
        connection.close()

        if producto:
            carrito = session.get('carrito', {})
            if str(product_id) in carrito:
                if carrito[str(product_id)]['cantidad'] < producto['cantidad']:
                    carrito[str(product_id)]['cantidad'] += 1
                    flash(f"añadiste {producto['nombre']}' en el carrito", 'success')
                else:
                    flash(f"no tenemos suficiente cantidad de{['nombre']}", 'warning')
            else:
                carrito[str(product_id)] = {
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
    return redirect(url_for('index'), carrito = producto)



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
        imagen = request.files.get ('imagen')
        disponibilidad = request.form ['disponibilidad']
        if imagen and imagen.filename:
            if not allowed_file(imagen.filename):
                flash('Solo se permiten archivos JPG, JPEG, PNG')
                return redirect(url_for('subir_producto'))
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

        else:
            imagen_filename = None
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre, descripcion, precio, cantidad, imagen, disponibilidad) VALUES (%s, %s, %s, %s, %s, %s)', 
                    (nombre, descripcion, precio, cantidad, imagen_filename, disponibilidad))
        mysql.connection.commit()
        flash(f'✅ El producto {nombre} ¡ha sido añadido a la tienda!')
        return redirect(url_for('inventario'))
    return render_template('subir_producto.html')

def allowed_file(filename):
    allowed_extensions = {'jpg'}
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions

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


if __name__ == '__main__':
    app.run(debug=True)