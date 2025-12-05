/**
 * AI Service Integration Example
 * 
 * This file demonstrates how to integrate the chatbot with an actual AI service
 * like OpenAI GPT, Anthropic Claude, or any other LLM API.
 * 
 * INSTRUCTIONS:
 * 1. Install the AI SDK: npm install openai (or your preferred AI SDK)
 * 2. Add your API key to environment variables (.env file)
 * 3. Uncomment and customize the implementation below
 * 4. Import and use in Chatbot.jsx
 */

import chatbotConfig from '../config/chatbot-prompt';
import chatbotTools from '../config/chatbot-tools';

/**
 * Example: OpenAI Integration
 * Uncomment and configure when ready to use
 */

/*
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.VITE_OPENAI_API_KEY,
});

export const callOpenAI = async (userMessage, conversationHistory = []) => {
  try {
    // Prepare messages with system prompt
    const messages = [
      {
        role: 'system',
        content: chatbotConfig.systemPrompt
      },
      ...conversationHistory.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.text
      })),
      {
        role: 'user',
        content: userMessage
      }
    ];

    // Prepare tools/functions for the AI
    const tools = Object.values(chatbotTools).map(tool => ({
      type: 'function',
      function: {
        name: tool.name,
        description: tool.description,
        parameters: {
          type: 'object',
          properties: tool.parameters,
          required: Object.keys(tool.parameters)
        }
      }
    }));

    // Call OpenAI API
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: messages,
      tools: tools,
      tool_choice: 'auto',
      temperature: 0.7,
      max_tokens: 500
    });

    const assistantMessage = response.choices[0].message;

    // Handle tool calls if AI wants to use them
    if (assistantMessage.tool_calls) {
      const toolResults = [];
      
      for (const toolCall of assistantMessage.tool_calls) {
        const toolName = toolCall.function.name;
        const toolArgs = JSON.parse(toolCall.function.arguments);
        
        // Execute the tool
        const tool = chatbotTools[toolName];
        if (tool) {
          const result = tool.execute(toolArgs);
          toolResults.push({
            tool_call_id: toolCall.id,
            output: JSON.stringify(result)
          });
        }
      }

      // Get final response with tool results
      const finalResponse = await openai.chat.completions.create({
        model: 'gpt-4-turbo-preview',
        messages: [
          ...messages,
          assistantMessage,
          ...toolResults.map(result => ({
            role: 'tool',
            tool_call_id: result.tool_call_id,
            content: result.output
          }))
        ]
      });

      return finalResponse.choices[0].message.content;
    }

    return assistantMessage.content;
  } catch (error) {
    console.error('OpenAI API Error:', error);
    return chatbotConfig.responseTemplates.fallback;
  }
};
*/

/**
 * Example: Anthropic Claude Integration
 * Uncomment and configure when ready to use
 */

/*
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.VITE_ANTHROPIC_API_KEY,
});

export const callClaude = async (userMessage, conversationHistory = []) => {
  try {
    // Prepare messages
    const messages = conversationHistory.map(msg => ({
      role: msg.type === 'user' ? 'user' : 'assistant',
      content: msg.text
    }));

    messages.push({
      role: 'user',
      content: userMessage
    });

    // Prepare tools for Claude
    const tools = Object.values(chatbotTools).map(tool => ({
      name: tool.name,
      description: tool.description,
      input_schema: {
        type: 'object',
        properties: tool.parameters,
        required: Object.keys(tool.parameters)
      }
    }));

    const response = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      system: chatbotConfig.systemPrompt,
      messages: messages,
      tools: tools
    });

    // Handle tool use
    if (response.content.some(block => block.type === 'tool_use')) {
      const toolResults = [];
      
      for (const block of response.content) {
        if (block.type === 'tool_use') {
          const tool = chatbotTools[block.name];
          if (tool) {
            const result = tool.execute(block.input);
            toolResults.push({
              type: 'tool_result',
              tool_use_id: block.id,
              content: JSON.stringify(result)
            });
          }
        }
      }

      // Get final response with tool results
      const finalResponse = await anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        system: chatbotConfig.systemPrompt,
        messages: [
          ...messages,
          { role: 'assistant', content: response.content },
          { role: 'user', content: toolResults }
        ]
      });

      return finalResponse.content[0].text;
    }

    return response.content[0].text;
  } catch (error) {
    console.error('Claude API Error:', error);
    return chatbotConfig.responseTemplates.fallback;
  }
};
*/

/**
 * Generic AI Service Call
 * Use this pattern for any AI service
 */
export const callAI = async (userMessage, conversationHistory = []) => {
  // Replace with your preferred AI service
  // return await callOpenAI(userMessage, conversationHistory);
  // return await callClaude(userMessage, conversationHistory);
  
  // For now, return a simple response
  console.log('AI Service not configured. Using fallback response.');
  return chatbotConfig.responseTemplates.fallback;
};

export default callAI;
