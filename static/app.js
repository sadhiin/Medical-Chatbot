document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    const clearChat = document.getElementById('clearChat');
    const typingIndicator = document.querySelector('.typing-indicator');
    const emojiButton = document.getElementById('emojiButton');
    const emojiPicker = document.querySelector('.emoji-picker');
    const themeToggle = document.getElementById('themeToggle');

    // Emoji picker functionality
    emojiButton.addEventListener('click', () => {
        emojiPicker.classList.toggle('active');
    });

    document.querySelectorAll('.emoji-button').forEach(button => {
        button.addEventListener('click', () => {
            userInput.value += button.textContent;
            emojiPicker.classList.remove('active');
            userInput.focus();
        });
    });

    // Close emoji picker when clicking outside
    document.addEventListener('click', (e) => {
        if (!emojiButton.contains(e.target) && !emojiPicker.contains(e.target)) {
            emojiPicker.classList.remove('active');
        }
    });

    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        appendMessage('user', message);
        userInput.value = '';
        userInput.style.height = 'auto';

        // Show typing indicator
        typingIndicator.classList.add('active');
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            // Simulate network delay for demo purposes
            // await new Promise(resolve => setTimeout(resolve, 1000));

            // Send message to FastAPI backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Hide typing indicator
            typingIndicator.classList.remove('active');

            // Add bot response (make sure we're using the correct property)
            if (data && data.response) {
                appendMessage('bot', data.response);
            } else {
                appendMessage('bot', 'Sorry, I received an invalid response format.');
            }
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.classList.remove('active');
            appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
        }
    });

    clearChat.addEventListener('click', function() {
        // Store the original typing indicator before clearing
        const originalTypingIndicator = typingIndicator;

        // Clear chat container
        chatContainer.innerHTML = '';

        // Add back welcome message
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message bot-message';
        welcomeMessage.innerHTML = `
            <p class="text-gray-100">Hello! I'm your medical information assistant. Please note that I can provide general medical information but cannot provide diagnosis or replace professional medical advice. How can I help you today?</p>
            <div class="message-time">Just now</div>
        `;

        // Add back typing indicator
        chatContainer.appendChild(welcomeMessage);
        chatContainer.appendChild(originalTypingIndicator);
    });

    function appendMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        messageDiv.innerHTML = `
            <p class="text-gray-100">${content}</p>
            <div class="message-time">${time}</div>
        `;

        chatContainer.insertBefore(messageDiv, typingIndicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });

    // Simple theme toggle (you can expand this)
    let isDark = true;
    themeToggle.addEventListener('click', () => {
        isDark = !isDark;
        document.body.style.backgroundColor = isDark ? '#1a1a2e' : '#f0f2f5';
    });
});
