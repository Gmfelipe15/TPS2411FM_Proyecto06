from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Estados de la conversación
conversations = {}

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
