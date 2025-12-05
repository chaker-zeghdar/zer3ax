"""
Flask API for Chatbot
Clean REST API for integration with frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from tools import answer_question
import os

app = Flask(__name__)
CORS(app)

print("\n🚀 Chatbot API starting...")
print("📊 Using keyword-based intelligent answering")
print("🛠️  No external API required - works offline!\n")


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Keyword-based Intelligence",
        "tools_enabled": True
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint - Uses keyword-based answering (no external API needed)
    """
    try:
        data = request.json
        
        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required",
                "success": False
            }), 400
        
        user_message = data["message"]
        
        # Use keyword-based answering tool
        response = answer_question(user_message)
        
        return jsonify({
            "response": response,
            "success": True,
            "service": "Keyword Intelligence"
        })
        
    except Exception as e:
        print(f"API Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation history"""
    return jsonify({
        "success": True,
        "message": "Conversation reset"
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
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
    print(f"📊 Service: Keyword-based Intelligence")
    print(f"🛠️  Tools: answer_question (smart keyword matching)")
    print(f"✅ Ready to answer ANY question about plants!\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)
