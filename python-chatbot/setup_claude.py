"""
Setup script for Zer3aZ Chatbot with Claude AI

This script helps you install dependencies and configure your API keys.
"""

import os
import subprocess
import sys


def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def setup_api_keys():
    """Guide user through API key setup"""
    print("\n🔑 API Key Setup")
    print("=" * 60)
    
    env_file = "../.env"
    env_content = []
    
    # Check if .env exists
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.readlines()
        print(f"✓ Found existing .env file")
    else:
        print("  Creating new .env file...")
    
    # Claude API Key
    print("\n1. ANTHROPIC API KEY (Claude AI - Recommended)")
    print("   Get your key at: https://console.anthropic.com/")
    current_claude = os.getenv("ANTHROPIC_API_KEY", "")
    if current_claude:
        print(f"   Current: {current_claude[:10]}...{current_claude[-4:]}")
        update = input("   Update? (y/N): ").lower() == 'y'
    else:
        update = True
    
    if update:
        new_key = input("   Enter your Anthropic API key: ").strip()
        if new_key:
            # Update or add to env_content
            found = False
            for i, line in enumerate(env_content):
                if line.startswith("ANTHROPIC_API_KEY="):
                    env_content[i] = f"ANTHROPIC_API_KEY={new_key}\n"
                    found = True
                    break
            if not found:
                env_content.append(f"ANTHROPIC_API_KEY={new_key}\n")
            print("   ✅ Claude API key configured!")
    
    # Gemini API Key (fallback)
    print("\n2. GEMINI API KEY (Google AI - Alternative/Fallback)")
    print("   Get your key at: https://makersuite.google.com/app/apikey")
    current_gemini = os.getenv("GEMINI_API_KEY", "")
    if current_gemini:
        print(f"   Current: {current_gemini[:10]}...{current_gemini[-4:]}")
        update = input("   Update? (y/N): ").lower() == 'y'
    else:
        update = input("   Add Gemini key? (y/N): ").lower() == 'y'
    
    if update:
        new_key = input("   Enter your Gemini API key: ").strip()
        if new_key:
            found = False
            for i, line in enumerate(env_content):
                if line.startswith("GEMINI_API_KEY="):
                    env_content[i] = f"GEMINI_API_KEY={new_key}\n"
                    found = True
                    break
            if not found:
                env_content.append(f"GEMINI_API_KEY={new_key}\n")
            print("   ✅ Gemini API key configured!")
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"\n✅ Configuration saved to {env_file}")


def test_api():
    """Test the API connection"""
    print("\n🧪 Testing API...")
    
    try:
        # Import and test
        sys.path.insert(0, '../src')
        
        print("\n  Testing Claude...")
        try:
            from services.claude_service import ClaudeChatbotService
            claude = ClaudeChatbotService()
            response = claude.chat("Hello, are you working?")
            print(f"  ✅ Claude: {response[:50]}...")
        except Exception as e:
            print(f"  ⚠️  Claude: {e}")
        
        print("\n  Testing Gemini...")
        try:
            from services.ai_service import GeminiService
            gemini = GeminiService()
            response = gemini.chat("Hello")
            print(f"  ✅ Gemini: {response[:50]}...")
        except Exception as e:
            print(f"  ⚠️  Gemini: {e}")
            
    except Exception as e:
        print(f"  ❌ Test failed: {e}")


def main():
    print("=" * 60)
    print("  Zer3aZ Chatbot Setup - Claude AI Integration")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("\n❌ Error: Please run this script from the python-chatbot directory")
        print("   cd python-chatbot && python setup_claude.py")
        return
    
    # Step 1: Install dependencies
    if input("\n📦 Install/update dependencies? (Y/n): ").lower() != 'n':
        if not install_dependencies():
            return
    
    # Step 2: Setup API keys
    if input("\n🔑 Configure API keys? (Y/n): ").lower() != 'n':
        setup_api_keys()
    
    # Step 3: Test API
    if input("\n🧪 Test API connection? (Y/n): ").lower() != 'n':
        test_api()
    
    print("\n" + "=" * 60)
    print("  ✅ Setup Complete!")
    print("=" * 60)
    print("\n📚 Next steps:")
    print("   1. Start the API: cd .. && python src/api/chatbot_api.py")
    print("   2. Start React frontend: npm run dev")
    print("   3. Open http://localhost:5173")
    print("\n💡 The chatbot will use Claude AI (if configured), then fall back to Gemini")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
