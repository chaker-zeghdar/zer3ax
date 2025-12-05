import { useState } from 'react';
import { Card, Input, Button, Typography, Space, Avatar } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import chatbotConfig from '../config/chatbot-prompt';
import chatbotTools from '../config/chatbot-tools';
import './Chatbot.css';

const { Title, Text } = Typography;
const { TextArea } = Input;

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: chatbotConfig.initialGreeting,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
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

    // Process bot response using config and tools
    setTimeout(() => {
      const response = processUserMessage(currentInput);
      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMessage]);
    }, 1000);
  };

  // Process user message and generate response
  const processUserMessage = (message) => {
    const lowerMessage = message.toLowerCase();

    // Handle plant search queries
    if (lowerMessage.includes('search') || lowerMessage.includes('find plant')) {
      const searchTerm = message.replace(/search|find plant|for/gi, '').trim();
      const results = chatbotTools.searchPlants.execute(searchTerm);
      
      if (results.length > 0) {
        return `I found ${results.length} plant(s) matching "${searchTerm}":\n\n${results.slice(0, 3).map(p => 
          `• ${p.name} (${p.scientificName}) - ${p.zone} zone`
        ).join('\n')}`;
      }
      return `I couldn't find any plants matching "${searchTerm}". Try searching by common name, scientific name, or zone.`;
    }

    // Handle zone queries
    if (lowerMessage.includes('zone') || lowerMessage.includes('northern') || 
        lowerMessage.includes('plateau') || lowerMessage.includes('sahara')) {
      let zone = 'Northern';
      if (lowerMessage.includes('plateau')) zone = 'High Plateau';
      if (lowerMessage.includes('sahara')) zone = 'Sahara';
      
      const stats = chatbotTools.getZoneStatistics.execute(zone);
      return `${zone} zone has ${stats.plantCount} plants in our database. Common traits include: ${stats.commonTraits.slice(0, 3).map(t => t.trait).join(', ')}.`;
    }

    // Handle prediction/hybridization queries
    if (lowerMessage.includes('predict') || lowerMessage.includes('hybrid')) {
      return chatbotConfig.responseTemplates.hybridizationQuestion.replace(
        '{response}',
        'you can use our Predict feature to analyze compatibility between plant species. It considers genetic traits, climate zones, and historical success rates.'
      );
    }

    // Handle trait queries
    if (lowerMessage.includes('trait')) {
      return 'Traits are genetic characteristics that can be passed to hybrid offspring. Key traits include drought resistance, yield potential, disease resistance, and adaptability to specific climates.';
    }

    // Handle help/general queries
    if (lowerMessage.includes('help') || lowerMessage.includes('what can you do')) {
      return chatbotConfig.responseTemplates.generalHelp;
    }

    // Default fallback response
    return chatbotConfig.responseTemplates.fallback;
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
                resize: 'none'
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
