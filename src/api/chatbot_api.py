"""
Flask API for Chatbot

This provides a REST API endpoint for the chatbot functionality.
The React frontend can call this API to get chatbot responses.

SETUP:
1. Install Flask: pip install flask flask-cors
2. Run the server: python chatbot_api.py
3. The API will be available at http://localhost:5000

ENDPOINTS:
- POST /api/chat - Send a message and get a response
- GET /api/config - Get chatbot configuration
- GET /api/tools - Get available tools
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.chatbot_prompt import chatbot_config, get_response_template
from config.chatbot_tools import chatbot_tools, execute_tool
from services.ai_service import GeminiService, get_ai_service

# Try to import Claude service
try:
    from services.claude_service import ClaudeChatbotService
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  Claude service not available (anthropic package not installed)")

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize AI services (priority order: Claude > Gemini > Fallback)
claude_service = None
gemini_service = None

# Try Claude first
if CLAUDE_AVAILABLE:
    try:
        claude_service = ClaudeChatbotService()
        print("✅ Claude AI service initialized successfully")
    except Exception as e:
        print(f"⚠️  Claude service initialization failed: {e}")

# Try Gemini as fallback
if not claude_service:
    try:
        gemini_service = GeminiService()
        print("✅ Gemini AI service initialized successfully")
    except Exception as e:
        gemini_service = None
        print(f"⚠️  Gemini service not available: {e}")
        print("   Install with: pip install google-generativeai")

if not claude_service and not gemini_service:
    print("🟡 Using flexible fallback response system")


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages.
    
    Request body:
    {
        "message": "user message",
        "conversation_history": [
            {"type": "user", "text": "previous message"},
            {"type": "bot", "text": "previous response"}
        ]
    }
    
    Response:
    {
        "response": "bot response",
        "success": true
    }
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        
        if not user_message:
            return jsonify({
                "error": "Message is required",
                "success": False
            }), 400
        
        # Use flexible chatbot logic (prioritize: Claude > Gemini > Fallback)
        if claude_service:
            response = claude_service.chat(user_message, conversation_history)
            service_name = "Claude AI (Sonnet 4)"
        elif gemini_service:
            response = gemini_service.chat(user_message, conversation_history)
            service_name = "Gemini AI"
        else:
            from services.ai_service import simple_chat_response
            response = simple_chat_response(user_message)
            service_name = "Flexible Data-Driven Fallback"
        
        return jsonify({
            "response": response,
            "success": True,
            "service": service_name
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get chatbot configuration.
    
    Response:
    {
        "initial_greeting": "...",
        "personality": {...},
        "platform_context": {...}
    }
    """
    return jsonify({
        "initial_greeting": chatbot_config["initial_greeting"],
        "personality": chatbot_config["personality"],
        "platform_context": chatbot_config["platform_context"],
        "success": True
    })


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """
    Get available chatbot tools.
    
    Response:
    {
        "tools": [
            {
                "name": "...",
                "description": "...",
                "parameters": {...}
            }
        ]
    }
    """
    tools_list = []
    for tool_name, tool_data in chatbot_tools.items():
        tools_list.append({
            "name": tool_data["name"],
            "description": tool_data["description"],
            "parameters": tool_data["parameters"]
        })
    
    return jsonify({
        "tools": tools_list,
        "success": True
    })


@app.route('/api/tool/<tool_name>', methods=['POST'])
def execute_tool_endpoint(tool_name):
    """
    Execute a specific tool.
    
    Request body:
    {
        "parameters": {
            "param1": "value1",
            "param2": "value2"
        }
    }
    
    Response:
    {
        "result": {...},
        "success": true
    }
    """
    try:
        data = request.json
        parameters = data.get('parameters', {})
        
        if tool_name not in chatbot_tools:
            return jsonify({
                "error": f"Tool '{tool_name}' not found",
                "success": False
            }), 404
        
        result = execute_tool(tool_name, **parameters)
        
        return jsonify({
            "result": result,
            "success": True
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Zer3aZ Chatbot API",
        "claude_available": claude_service is not None,
        "gemini_available": gemini_service is not None,
        "active_service": "Claude AI" if claude_service else "Gemini AI" if gemini_service else "Fallback"
    })


@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """
    Generate a detailed breeding analysis report.
    
    Request body:
    {
        "plant_a_id": 1,
        "plant_b_id": 2
    }
    
    Response:
    {
        "report": "...",
        "success": true
    }
    """
    try:
        data = request.json
        plant_a_id = data.get('plant_a_id')
        plant_b_id = data.get('plant_b_id')
        
        if plant_a_id is None or plant_b_id is None:
            return jsonify({
                "error": "Both plant_a_id and plant_b_id are required",
                "success": False
            }), 400
        
        # Generate report using Gemini if available
        if gemini_service:
            report = gemini_service.generate_report(plant_a_id, plant_b_id)
        else:
            # Fallback to structured data
            report_data = execute_tool("generate_detailed_report", 
                                      plant_a_id=plant_a_id, 
                                      plant_b_id=plant_b_id)
            import json
            report = json.dumps(report_data, indent=2)
        
        return jsonify({
            "report": report,
            "success": True,
            "service": "Gemini AI" if gemini_service else "Structured Data"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


if __name__ == '__main__':
    print("Starting Zer3aZ Chatbot API...")
    print("API available at: http://localhost:5001")
    print("\nEndpoints:")
    print("  POST /api/chat - Send chat messages")
    print("  GET  /api/config - Get chatbot config")
    print("  GET  /api/tools - List available tools")
    print("  POST /api/tool/<name> - Execute a tool")
    print("  POST /api/generate-report - Generate breeding report")
    print("  GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
