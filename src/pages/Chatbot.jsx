import { useState } from 'react';
import { Card, Input, Button, Typography, Space, Avatar } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import './Chatbot.css';

const { Title, Text } = Typography;
const { TextArea } = Input;

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "👋 Hello! I'm your AI Plant Breeding assistant. Ask me anything about plants, zones, or traits!",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: inputValue,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages([...messages, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    // Call Python chatbot API with keyword-based method
    try {
      console.log('Sending message to API:', currentInput);
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: currentInput,
          conversation_history: messages.map(m => ({
            role: m.type === 'user' ? 'user' : 'assistant',
            content: m.text
          }))
        })
      });

      const data = await response.json();
      console.log('Received response from API:', data);
      
      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: data.response || "I'm having trouble connecting to the API. Please make sure the Python server is running on port 5001.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      console.log('Bot message:', botMessage);
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: "⚠️ Cannot connect to chatbot API. Please start the Python server with: python src/config/chatbot_v2/api.py",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', height: 'calc(100vh - 100px)' }}>
      {/* Page Header */}
      <div style={{ marginBottom: 24 }}>
        <Title level={2} style={{ 
          color: '#2C3E50', 
          fontWeight: 700, 
          marginBottom: 8,
          fontSize: '2rem',
          letterSpacing: '-0.02em'
        }}>
          AI Chatbot
        </Title>
        <Text style={{ color: '#7F8C8D', fontSize: '15px', fontWeight: 400 }}>
          Ask questions about plant breeding, predictions, and recommendations.
        </Text>
      </div>

      {/* Chat Container */}
      <Card
        bordered={false}
        style={{
          background: '#FFFFFF',
          borderRadius: 16,
          border: '1px solid #E1E8ED',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
          height: 'calc(100% - 100px)',
          display: 'flex',
          flexDirection: 'column'
        }}
        bodyStyle={{
          padding: 0,
          height: '100%',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Messages Area */}
        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message-wrapper ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">
                <Avatar
                  icon={message.type === 'user' ? <UserOutlined /> : <RobotOutlined />}
                  style={{
                    backgroundColor: message.type === 'user' ? '#3498DB' : '#27AE60',
                    flexShrink: 0
                  }}
                />
                <div className="message-bubble">
                  <Text style={{ color: '#2C3E50', fontSize: 14 }}>{message.text}</Text>
                  <Text style={{ color: '#95A5A6', fontSize: 11, marginTop: 4, display: 'block' }}>
                    {message.timestamp}
                  </Text>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="chat-input-container">
          <Space.Compact style={{ width: '100%' }}>
            <TextArea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              autoSize={{ minRows: 1, maxRows: 4 }}
              style={{
                fontSize: 14,
                borderRadius: '10px 0 0 10px',
                resize: 'none',
              }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={handleSend}
              style={{
                height: 'auto',
                minHeight: 40,
                backgroundColor: '#27AE60',
                borderColor: '#27AE60',
                borderRadius: '0 10px 10px 0'
              }}
            >
              Send
            </Button>
          </Space.Compact>
        </div>
      </Card>
    </div>
  );
};

export default Chatbot;
