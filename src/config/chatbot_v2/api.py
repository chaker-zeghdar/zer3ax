"""
Flask API for Chatbot
Clean REST API for integration with frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from tools import answer_question

app = Flask(__name__)
CORS(app)

print("\n🚀 Chatbot API starting...")
print("🧠 Using keyword-based method with plant breeding knowledge")
print("🛠️  Pattern matching + comprehensive breeding data\n")


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Keyword-based method",
        "tools_enabled": True
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint - Uses keyword-based method from tools.py
    """
    try:
        data = request.json
        
        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required",
                "success": False
            }), 400
        
        user_message = data["message"]
        
        # Use keyword-based answer_question from tools.py
        response = answer_question(user_message)
        
        return jsonify({
            "response": response,
            "success": True,
            "service": "Keyword-based method"
        })
        
    except Exception as e:
        print(f"API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"I encountered an error: {str(e)}",
            "success": False
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation history (not used in keyword method but kept for compatibility)"""
    return jsonify({
        "success": True,
        "message": "Conversation reset"
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history (not used in keyword method but kept for compatibility)"""
    return jsonify({
        "history": [],
        "success": True
    })


@app.route('/api/greeting', methods=['GET'])
def greeting():
    """Get greeting message"""
    return jsonify({
        "greeting": "👋 Hello! I'm your AI Plant Breeding assistant. Ask me anything!",
        "success": True
    })


if __name__ == "__main__":
    port = 5001
    print(f"\n🚀 Chatbot API running on http://localhost:{port}")
    print(f"🧠 Service: Keyword-based method")
    print(f"🛠️  Pattern matching with plant breeding expertise")
    print(f"✅ Fast, predictable responses!\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)
