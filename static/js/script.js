// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const loadingOverlay = document.getElementById('loadingOverlay');

// Auto-resize textarea
questionInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Handle Enter key (Shift+Enter for new line)
questionInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
    }
});

// Send button click
sendButton.addEventListener('click', sendQuestion);

// Format timestamp
function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });
}

// Add user message to chat
function addUserMessage(question) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(question)}</div>
            <div class="message-time">${formatTime()}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add assistant message to chat
function addAssistantMessage(answer, sources = [], confidence = 'medium') {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message';
    
    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="sources">
                <div class="sources-title">📚 Sources:</div>
                ${sources.map(source => `<div class="source-item">• ${escapeHtml(source)}</div>`).join('')}
            </div>
        `;
    }
    
    const confidenceBadge = confidence ? 
        `<span class="confidence-badge confidence-${confidence}">
            ${confidence.charAt(0).toUpperCase() + confidence.slice(1)} Confidence
        </span>` : '';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                ${escapeHtml(answer)}
                ${confidenceBadge}
            </div>
            ${sourcesHtml}
            <div class="message-time">${formatTime()}</div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Add error message
function addErrorMessage(error) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">⚠️</div>
        <div class="message-content">
            <div class="message-text" style="background: #fee2e2; color: #991b1b;">
                Sorry, I encountered an error: ${escapeHtml(error)}
            </div>
            <div class="message-time">${formatTime()}</div>
        </div>
    `;
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show/hide loading overlay
function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

// Disable/enable input
function setInputEnabled(enabled) {
    questionInput.disabled = !enabled;
    sendButton.disabled = !enabled;
}

// Send question to backend
async function sendQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        return;
    }
    
    // Add user message
    addUserMessage(question);
    
    // Clear input
    questionInput.value = '';
    questionInput.style.height = 'auto';
    
    // Disable input and show loading
    setInputEnabled(false);
    showLoading(true);
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addAssistantMessage(
                data.answer, 
                data.sources, 
                data.confidence
            );
        } else {
            addErrorMessage(data.error || 'Unable to get answer');
        }
        
    } catch (error) {
        console.error('Error:', error);
        addErrorMessage('Failed to connect to the server. Please try again.');
    } finally {
        showLoading(false);
        setInputEnabled(true);
        questionInput.focus();
    }
}

// Initialize - focus on input
questionInput.focus();

// Example questions (optional - you can add clickable examples)
const exampleQuestions = [
    "What are the MBA admission requirements?",
    "Tell me about the MBA curriculum",
    "Who are the faculty members?",
    "What specializations are available?"
];

console.log('💡 Try these example questions:', exampleQuestions);
