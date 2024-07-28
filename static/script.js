let currentChatId = null;

async function loadChats() {
    try {
        const response = await fetch('/chats');
        if (!response.ok) throw new Error('Failed to fetch chats');
        const chats = await response.json();
        const chatHistory = document.getElementById('chat-history');
        chatHistory.innerHTML = '';
        chats.forEach(chat => {
            const chatElement = document.createElement('li');
            chatElement.textContent = chat.title;
            chatElement.onclick = () => loadChat(chat.id);
            chatElement.dataset.chatId = chat.id;
            chatHistory.appendChild(chatElement);
        });
        if (chats.length > 0) {
            loadChat(chats[0].id);
        } else {
            createNewChat();
        }
    } catch (error) {
        console.error('Error loading chats:', error);
    }
}

async function loadChat(chatId) {
    try {
        currentChatId = chatId;
        const response = await fetch(`/chat/${chatId}`);
        if (!response.ok) throw new Error('Failed to fetch chat messages');
        const messages = await response.json();
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = '';
        messages.forEach(message => {
            appendMessageToChatBox(message.sender, message.content, message.sender === 'bot');
        });
        const chatTitle = document.getElementById('chat-title');
        chatTitle.textContent = messages.length > 0 ? messages[0].content.slice(0, 30) : "Выберите чат";

        document.querySelectorAll('#chat-history li').forEach(li => {
            li.classList.toggle('active', li.dataset.chatId == chatId);
        });
    } catch (error) {
        console.error('Error loading chat:', error);
    }
}

async function createNewChat() {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) throw new Error('Failed to create new chat');
        const newChat = await response.json();
        loadChats();
        loadChat(newChat.id);
    } catch (error) {
        console.error('Error creating new chat:', error);
    }
}

async function deleteCurrentChat() {
    if (currentChatId) {
        try {
            const response = await fetch(`/chat/${currentChatId}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete chat');
            loadChats();
        } catch (error) {
            console.error('Error deleting chat:', error);
        }
    }
}

async function sendMessage() {
    try {
        const inputElement = document.getElementById('prompt-input');
        const message = inputElement.value.trim();

        if (message === "" || !currentChatId) return;

        appendMessageToChatBox("user", message);
        inputElement.value = '';

        const response = await fetch(`/chat/${currentChatId}/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error('Failed to send message');
        const data = await response.json();
        appendMessageToChatBox("bot", data.bot_response.content, true);

        const chatTitle = document.getElementById('chat-title');
        chatTitle.textContent = message.slice(0, 30);
        loadChats();
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function appendMessageToChatBox(sender, message, isHTML = false) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    if (isHTML) {
        messageElement.innerHTML = marked.parse(message);
    } else {
        const paragraph = document.createElement('p');
        paragraph.innerHTML = marked.parse(message);
        messageElement.appendChild(paragraph);
    }

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById('prompt-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

window.onload = loadChats;
