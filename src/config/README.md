# Chatbot Configuration

This directory contains the independent configuration files for the Zer3aZ AI Chatbot.

## Files

### 1. `chatbot-prompt.js`
Contains the system prompt and personality settings for the chatbot.

**What you can customize:**
- System prompt - Defines the chatbot's expertise and behavior
- Initial greeting message
- Personality settings (name, tone, expertise)
- Response templates for common scenarios
- Platform context and features

**Example modification:**
```javascript
// Change the initial greeting
initialGreeting: "Welcome! I'm here to help with plant breeding.",

// Update the system prompt
systemPrompt: `You are a specialized agricultural AI...`,
```

### 2. `chatbot-tools.js`
Defines the tools and functions the chatbot can use to interact with data.

**Available tools:**
- `searchPlants` - Search for plants by name or characteristics
- `getPlantDetails` - Get detailed info about a specific plant
- `calculateTraitSimilarity` - Compare traits between plants
- `getPlantsByZone` - Filter plants by climate zone
- `predictHybridization` - Simulate hybridization prediction
- `getZoneStatistics` - Get stats about a climate zone
- `getRecommendations` - Get plant recommendations based on criteria

**Adding a new tool:**
```javascript
export const yourNewTool = (params) => {
  // Your tool logic here
  return result;
};

// Register in chatbotTools object
export const chatbotTools = {
  // ... existing tools
  yourNewTool: {
    name: "yourNewTool",
    description: "What your tool does",
    parameters: {
      param1: "type - description"
    },
    execute: yourNewTool
  }
};
```

## How It Works

1. **Prompt Configuration** (`chatbot-prompt.js`)
   - Loaded when the chatbot initializes
   - Used for the initial greeting and response templates
   - Provides context about the platform and expertise

2. **Tools** (`chatbot-tools.js`)
   - Functions that can be called based on user queries
   - Integrate with the platform's data (plants, zones, predictions)
   - Return structured data that can be formatted into responses

3. **Chatbot Component** (`pages/Chatbot.jsx`)
   - Imports both configuration files
   - Uses the `processUserMessage` function to analyze user input
   - Calls appropriate tools based on detected intents
   - Formats responses using the configuration templates

## Customization Examples

### Change the chatbot personality
Edit `chatbot-prompt.js`:
```javascript
personality: {
  name: "AgriBot",
  tone: "casual and friendly",
  expertise: "farming and agriculture",
  responseStyle: "simple and direct"
}
```

### Add a new response template
Edit `chatbot-prompt.js`:
```javascript
responseTemplates: {
  // ... existing templates
  weatherQuery: "The weather conditions in {zone} are {conditions}",
}
```

### Create a custom tool
Edit `chatbot-tools.js`:
```javascript
export const getWeatherInfo = (zone) => {
  // Implementation
  return weatherData;
};

// Add to chatbotTools registry
```

### Extend message processing
Edit `pages/Chatbot.jsx` in the `processUserMessage` function:
```javascript
// Add new intent detection
if (lowerMessage.includes('weather')) {
  const zone = detectZone(lowerMessage);
  const weather = chatbotTools.getWeatherInfo.execute(zone);
  return formatWeatherResponse(weather);
}
```

## Best Practices

1. **Keep prompts clear and specific** - The system prompt should clearly define the chatbot's role
2. **Use response templates** - Create reusable templates for common response types
3. **Document tools thoroughly** - Each tool should have a clear description and parameter list
4. **Test incrementally** - After modifying config, test the chatbot behavior
5. **Separate concerns** - Keep prompts in prompt config, logic in tools, UI in components

## Integration with AI Services

To connect with an actual AI service (OpenAI, Claude, etc.):

1. Create a new file `src/services/ai-service.js`
2. Implement API calls using the system prompt from `chatbot-prompt.js`
3. Pass available tools to the AI service
4. Update `Chatbot.jsx` to use the AI service instead of the simple message processor

Example structure:
```javascript
import chatbotConfig from '../config/chatbot-prompt';
import chatbotTools from '../config/chatbot-tools';

export const callAI = async (userMessage, conversationHistory) => {
  const response = await fetch('AI_API_ENDPOINT', {
    method: 'POST',
    body: JSON.stringify({
      systemPrompt: chatbotConfig.systemPrompt,
      messages: conversationHistory,
      tools: Object.values(chatbotTools),
      userMessage
    })
  });
  return response.json();
};
```

## Troubleshooting

- **Chatbot not responding**: Check console for errors in tool execution
- **Wrong responses**: Review intent detection logic in `processUserMessage`
- **Tools not working**: Verify tool is registered in `chatbotTools` object
- **Prompt not applied**: Ensure `chatbotConfig` is properly imported
