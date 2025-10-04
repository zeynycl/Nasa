document.addEventListener('DOMContentLoaded', () => {
    // Enter tuşuna basıldığında mesajı gönderme
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

    if (userText === "") return; // Boş mesaj gönderme

    // 1. Kullanıcı mesajını ekle
    appendMessage(userText, 'user-message');

    // 2. Input alanını temizle
    userInput.value = '';

    // 3. Yapay Zeka (Bot) cevabını simüle et (Gerçek AI entegrasyonu burada yapılır)
    simulateBotResponse(userText);

    // 4. Sohbeti en alta kaydır
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
    // Basit bir simülasyon yanıtı.
    let botResponseText = `"${userQuery}" hakkında gPlant veritabanı aranıyor...`;

    if (userQuery.toLowerCase().includes("gül")) {
        botResponseText = "Gül (Rosa), iyi drenajlı toprak ve bol güneş ışığı ister. Siyah leke hastalığına karşı düzenli kontrol önemlidir.";
    } else if (userQuery.toLowerCase().includes("sulama")) {
        botResponseText = "Genel olarak, toprağın üst yüzeyi kuruduğunda sulama yapın. Aşırı sulama kök çürümesine yol açabilir.";
    }

    // Cevabın biraz gecikmeli gelmesi için setTimeout kullanıldı
    setTimeout(() => {
        appendMessage(botResponseText, 'bot-message');
        scrollToBottom(document.getElementById('chatContainer'));
    }, 1000); // 1 saniye bekleme
}

function scrollToBottom(element) {
    // Yeni mesaj geldiğinde otomatik olarak en alta kaydırma
    element.scrollTop = element.scrollHeight;
}