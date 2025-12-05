#!/usr/bin/env python3
"""
Simple test script for the chatbot configuration and tools.
Run with: python test_chatbot.py
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.chatbot_prompt import (
    chatbot_config,
    get_system_prompt,
    get_initial_greeting,
    get_response_template
)
from config.chatbot_tools import (
    chatbot_tools,
    execute_tool
)
from services.ai_service import simple_chat_response


def test_configuration():
    """Test chatbot configuration."""
    print("=" * 60)
    print("TESTING CHATBOT CONFIGURATION")
    print("=" * 60)
    
    print("\n1. System Prompt (first 200 chars):")
    print(get_system_prompt()[:200] + "...")
    
    print("\n2. Initial Greeting:")
    print(get_initial_greeting())
    
    print("\n3. Response Templates:")
    for template_name in chatbot_config["response_templates"]:
        print(f"   - {template_name}")
    
    print("\n4. Personality:")
    for key, value in chatbot_config["personality"].items():
        print(f"   {key}: {value}")
    
    print("\n✓ Configuration tests passed!\n")


def test_tools():
    """Test chatbot tools."""
    print("=" * 60)
    print("TESTING CHATBOT TOOLS")
    print("=" * 60)
    
    print("\n1. Available Tools:")
    for tool_name in chatbot_tools:
        print(f"   - {tool_name}")
    
    print("\n2. Testing search_plants:")
    results = execute_tool("search_plants", query="wheat")
    print(f"   Found {len(results)} plants matching 'wheat'")
    if results:
        print(f"   First result: {results[0]['name']} ({results[0]['scientific_name']})")
    
    print("\n3. Testing get_plants_by_zone:")
    northern_plants = execute_tool("get_plants_by_zone", zone="Northern")
    print(f"   Found {len(northern_plants)} plants in Northern zone")
    
    print("\n4. Testing get_zone_statistics:")
    stats = execute_tool("get_zone_statistics", zone="Northern")
    print(f"   Zone: {stats['zone']}")
    print(f"   Plant Count: {stats['plant_count']}")
    print(f"   Common Traits: {[t['trait'] for t in stats['common_traits'][:3]]}")
    
    print("\n5. Testing predict_hybridization:")
    prediction = execute_tool("predict_hybridization", plant_a_id=1, plant_b_id=2)
    if prediction:
        print(f"   Plants: {prediction['plant_a']} × {prediction['plant_b']}")
        print(f"   Success Rate: {prediction['success_rate']}%")
        print(f"   Compatibility: {prediction['compatibility']}")
        print(f"   Shared Traits: {prediction['shared_traits']}")
    
    print("\n✓ Tool tests passed!\n")


def test_chat_responses():
    """Test simple chat responses."""
    print("=" * 60)
    print("TESTING CHAT RESPONSES")
    print("=" * 60)
    
    test_messages = [
        "search for wheat",
        "tell me about the northern zone",
        "how do I predict hybridization?",
        "what can you help me with?",
        "hello"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        response = simple_chat_response(message)
        print(f"   Bot: {response[:150]}...")
    
    print("\n✓ Chat response tests passed!\n")


def interactive_mode():
    """Interactive chat mode for testing."""
    print("=" * 60)
    print("INTERACTIVE CHAT MODE")
    print("=" * 60)
    print("\nType your messages (type 'quit' to exit):\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        response = simple_chat_response(user_input)
        print(f"Bot: {response}\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("ZER3AZ CHATBOT - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        # Run tests
        test_configuration()
        test_tools()
        test_chat_responses()
        
        # Ask if user wants interactive mode
        print("\n" + "=" * 60)
        choice = input("\nDo you want to try interactive chat mode? (y/n): ").strip().lower()
        if choice == 'y':
            interactive_mode()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
