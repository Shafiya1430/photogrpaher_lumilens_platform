// ==================== CHATBOT FUNCTIONALITY ====================

function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    if (chatbotWindow.style.display === 'none' || chatbotWindow.style.display === '') {
        chatbotWindow.style.display = 'flex';
    } else {
        chatbotWindow.style.display = 'none';
    }
}

function sendChatbotMessage() {
    const inputField = document.getElementById('chatbot-input-field');
    const message = inputField.value.trim();

    if (message === '') return;

    // Add user message to chat
    const messagesContainer = document.getElementById('chatbot-messages');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.innerHTML = `<p>${message}</p>`;
    messagesContainer.appendChild(userMessageDiv);

    // Clear input
    inputField.value = '';

    // Send message to backend
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'bot-message';
            botMessageDiv.innerHTML = `<p>${data.response}</p>`;
            messagesContainer.appendChild(botMessageDiv);

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
        });

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function () {
    const inputField = document.getElementById('chatbot-input-field');
    if (inputField) {
        inputField.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendChatbotMessage();
            }
        });
    }
});
// ==================== BOOKING CHAT & CALL ====================

let currentBookingId = null;
let chatInterval = null;

function openChatModal(bookingId, name) {
    currentBookingId = bookingId;
    document.getElementById('chat-recipient').innerText = name;
    document.getElementById('chat-modal').style.display = 'block';

    // Initial load
    loadChatMessages(bookingId);

    // Poll for new messages every 3 seconds
    chatInterval = setInterval(() => loadChatMessages(bookingId), 3000);
}

function closeChatModal() {
    document.getElementById('chat-modal').style.display = 'none';
    clearInterval(chatInterval);
}

function loadChatMessages(bookingId) {
    fetch(`/chat/${bookingId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const history = document.getElementById('chat-history');
                history.innerHTML = '';
                data.messages.forEach(msg => {
                    const msgDiv = document.createElement('div');
                    msgDiv.className = `chat-msg ${msg.sender === 'bot' ? 'received' : 'sent'}`; // Simplified logic for demo
                    // In real app, we'd check against session name
                    msgDiv.innerHTML = `<div class="msg-bubble"><strong>${msg.sender}:</strong> ${msg.message}</div>`;
                    history.appendChild(msgDiv);
                });
                history.scrollTop = history.scrollHeight;
            }
        });
}

function sendMessage() {
    const input = document.getElementById('chat-message-input');
    const message = input.value.trim();
    if (!message || !currentBookingId) return;

    const formData = new FormData();
    formData.append('message', message);

    fetch(`/send-message/${currentBookingId}`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                input.value = '';
                loadChatMessages(currentBookingId);
            }
        });
}

function openCallModal(name) {
    document.getElementById('call-name').innerText = `Calling ${name}...`;
    document.getElementById('call-avatar').innerText = name[0];
    document.getElementById('call-modal').style.display = 'block';

    setTimeout(() => {
        document.getElementById('call-status').innerText = 'Connected';
    }, 2000);
}

function closeCallModal() {
    document.getElementById('call-modal').style.display = 'none';
    document.getElementById('call-status').innerText = 'Connecting...';
}

// Close modals when clicking outside
window.onclick = function (event) {
    const chatModal = document.getElementById('chat-modal');
    const callModal = document.getElementById('call-modal');
    if (event.target == chatModal) closeChatModal();
    if (event.target == callModal) closeCallModal();
}
