document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const userText = userInput.value.trim();

    if (userText === "") return; 

    
    appendMessage(userText, 'user-message');

    
    userInput.value = '';

    
    simulateBotResponse(userText);

    
    scrollToBottom(chatContainer);
}

function appendMessage(text, className) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
}

function simulateBotResponse(userQuery) {
   
    let botResponseText = `"${userQuery}" hakkında gPlant veritabanı aranıyor...`;

    if (userQuery.toLowerCase().includes("gül")) {
        botResponseText = "Gül (Rosa), iyi drenajlı toprak ve bol güneş ışığı ister. Siyah leke hastalığına karşı düzenli kontrol önemlidir.";
    } else if (userQuery.toLowerCase().includes("sulama")) {
        botResponseText = "Genel olarak, toprağın üst yüzeyi kuruduğunda sulama yapın. Aşırı sulama kök çürümesine yol açabilir.";
    }

    
    setTimeout(() => {
        appendMessage(botResponseText, 'bot-message');
        scrollToBottom(document.getElementById('chatContainer'));
    }, 1000); 
}

function scrollToBottom(element) {
    
    element.scrollTop = element.scrollHeight;
}
