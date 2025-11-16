const messageForm = document.getElementById('messageForm');
const messageInput = document.getElementById('messageInput');
const chatContainer = document.getElementById('chatContainer');
const sendButton = document.getElementById('sendButton');

messageForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userMessage = messageInput.value.trim();
    if (!userMessage) return;
    
    // Add user message to chat
    addMessage(userMessage, 'user');
    
    // Clear input
    messageInput.value = '';
    
    // Disable send button
    sendButton.disabled = true;
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        // Send message to server
        const formData = new FormData();
        formData.append('msg', userMessage);
        
        const response = await fetch('/get', {
            method: 'POST',
            body: formData
        });
        
        const botResponse = await response.text();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add bot response to chat
        addMessage(botResponse, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    } finally {
        // Re-enable send button
        sendButton.disabled = false;
        messageInput.focus();
    }
});

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${text}`;
    
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return messageDiv;
}

function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    
    const typingContent = document.createElement('div');
    typingContent.className = 'message-content';
    
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingContent.appendChild(typingIndicator);
    typingDiv.appendChild(typingContent);
    chatContainer.appendChild(typingDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return typingDiv;
}

// Focus input on load
messageInput.focus();
