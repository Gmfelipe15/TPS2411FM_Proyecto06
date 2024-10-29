const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatLog = document.getElementById("chat-log");
const chatbotContainer = document.getElementById("chatbot-container");
const closeChatbotButton = document.getElementById("close-chatbot");

// Función para inicializar el chat
function initializeChat() {
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "message="
    })
    .then(response => response.json())
    .then(data => {
        const response = data.response;
        chatLog.innerHTML += `<p><strong>Beibot:</strong> ${response}</p>`;
        chatLog.scrollTop = chatLog.scrollHeight;  // Desplazar el chat hacia abajo
    });
}

// Enviar saludo automático al cargar la página
window.addEventListener("load", initializeChat);

sendButton.addEventListener("click", (e) => {
    e.preventDefault();
    const message = userInput.value;
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `message=${message}`
    })
    .then(response => response.json())
    .then(data => {
        const response = data.response;
        chatLog.innerHTML += `<p><strong>Tú:</strong> ${message}</p><p><strong>Chatbot:</strong> ${response}</p>`;
        userInput.value = "";

        // Si el chatbot indica que la conversación ha terminado y el usuario desea salir
        if (response.includes("¡Hasta luego!")) {
            setTimeout(() => {
                chatbotContainer.style.display = 'none'; // Ocultar el chatbot
            }, 2000);  // Cerrar después de 2 segundos para dar tiempo a leer la despedida
        }

        chatLog.scrollTop = chatLog.scrollHeight;  // Desplazar el chat hacia abajo
    });
});

// Respuesta inteligente para peticiones no acordes
if (!response) {
    chatLog.innerHTML += `<p><strong>Beibot:</strong> Lo siento, no puedo ayudar con eso. ¿Puedes preguntar algo diferente?</p>`;
}

chatLog.scrollTop = chatLog.scrollHeight;  // Desplazar el chat hacia abajo

// Minimizar el chatbot
minimizeChatbotButton.addEventListener("click", () => {
if (isMinimized) {
chatbotContainer.style.height = 'auto'; // Restaurar el tamaño
minimizeChatbotButton.textContent = '-'; // Cambiar el texto del botón
} else {
chatbotContainer.style.height = '50px'; // Minimizar el tamaño
chatLog.style.display = 'none'; // Ocultar el log del chat
minimizeChatbotButton.textContent = '+'; // Cambiar el texto del botón
}
isMinimized = !isMinimized; // Alternar el estado
});

// Cerrar el chatbot manualmente
closeChatbotButton.addEventListener("click", () => {
    chatbotContainer.style.display = 'none';
});
