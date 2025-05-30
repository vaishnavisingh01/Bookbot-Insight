css = """
<style>
    /* Modern Dark Theme with Gradient and Glassmorphism */
body {
    background: linear-gradient(135deg, #0f0f17, #1a1a2e);
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #e0e0e0;
}

.chat-container {
    max-width: 800px;
    width: 100%;
    background: rgba(30, 30, 47, 0.85);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 1.2rem;
}

.chat-container:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.35);
}

.chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1.2rem;
    position: relative;
    animation: fadeIn 0.4s ease-out;
    padding: 0.8rem;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
    flex-direction: row-reverse;
}

.avatar {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 3px 5px rgba(0, 0, 0, 0.15);
    flex-shrink: 0;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.message {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.6;
    word-wrap: break-word;
    transition: all 0.3s ease;
}

.chat-message.bot .message {
    background: linear-gradient(145deg, #40495f, #333a4d);
    border-bottom-left-radius: 5px;
    margin-left: 0.8rem;
    color: #e0e0e0;
}

.chat-message.user .message {
    background: linear-gradient(145deg, #2d3444, #242a36);
    border-bottom-right-radius: 5px;
    margin-right: 0.8rem;
    text-align: right;
    color: #e0e0e0;
}

/* Adapted for Streamlit */
.stChatInputContainer {
    background: rgba(15, 15, 25, 0.7);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem;
}

.stChatInput {
    background: rgba(43, 49, 62, 0.85) !important;
    border: 1px solid rgba(90, 100, 120, 0.5) !important;
    color: #e0e0e0 !important;
    border-radius: 24px !important;
}

.stChatInput:focus {
    border-color: #6b70a0 !important;
    box-shadow: 0 0 8px rgba(107, 112, 160, 0.4) !important;
}

/* Streamlit button styling */
.stButton > button {
    background: linear-gradient(145deg, #4CAF50, #45a049) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2) !important;
    background: linear-gradient(145deg, #45a049, #4CAF50) !important;
}

/* Code blocks and other elements */
pre {
    background: rgba(15, 15, 25, 0.7) !important;
    border-radius: 8px !important;
    padding: 12px !important;
    overflow-x: auto !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

code {
    color: #a6e3a1 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Streamlit sidebar customization */
.css-1d391kg, .css-1lcbmhc {
    background: rgba(22, 22, 35, 0.9) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #1e1e2f;
}
::-webkit-scrollbar-thumb {
    background: #575b7a;
    border-radius: 8px;
}
</style>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdn-icons-png.flaticon.com/512/5231/5231019.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""