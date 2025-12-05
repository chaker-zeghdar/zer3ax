"""
Flask API for Chatbot
Clean REST API for integration with frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import Chatbot
from config import GREETING, SETTINGS
import os

app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = Chatbot()

# Store conversation sessions (in production, use Redis or database)
sessions = {}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": chatbot.service,
        "model": chatbot.config["model_name"],
        "tools_enabled": SETTINGS["enable_tools"]
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint
    
    Request:
        {
            "message": "User message",
            "session_id": "optional-session-id",
            "conversation_history": [] (optional)
        }
    
    Response:
        {
            "response": "AI response",
            "success": true,
            "session_id": "session-id"
        }
    """
    try:
        data = request.json
        
        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required",
                "success": False
            }), 400
        
        user_message = data["message"]
        session_id = data.get("session_id", "default")
        conversation_history = data.get("conversation_history", [])
        
        # Get or create session chatbot
        if session_id not in sessions:
            sessions[session_id] = Chatbot()
        
        session_bot = sessions[session_id]
        
        # Use external history if provided
        if conversation_history:
            session_bot.conversation_history = conversation_history
        
        # Get response
        response = session_bot.chat(user_message)
        
        return jsonify({
            "response": response,
            "success": True,
            "session_id": session_id,
            "service": chatbot.service
        })
        
    except Exception as e:
        if SETTINGS["debug_mode"]:
            print(f"API Error: {e}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation history"""
    try:
        data = request.json or {}
        session_id = data.get("session_id", "default")
        
        if session_id in sessions:
            sessions[session_id].reset()
        
        return jsonify({
            "success": True,
            "message": "Conversation reset"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    session_id = request.args.get("session_id", "default")
    
    if session_id in sessions:
        history = sessions[session_id].get_history()
    else:
        history = []
    
    return jsonify({
        "history": history,
        "success": True
    })


@app.route('/api/greeting', methods=['GET'])
def greeting():
    """Get greeting message"""
    return jsonify({
        "greeting": GREETING,
        "success": True
    })


if __name__ == "__main__":
    port = int(os.getenv("CHATBOT_PORT", 5001))
    print(f"\n🚀 Chatbot API running on http://localhost:{port}")
    print(f"📊 Service: {chatbot.service}")
    print(f"🤖 Model: {chatbot.config['model_name']}")
    print(f"🛠️  Tools enabled: {SETTINGS['enable_tools']}\n")
    
    app.run(host="0.0.0.0", port=port, debug=SETTINGS["debug_mode"])
