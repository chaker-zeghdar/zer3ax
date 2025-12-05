"""
Custom Tools/Functions for Chatbot
Define your domain-specific tools here
"""

from typing import Dict, Any, List, Callable


class ToolRegistry:
    """Registry for chatbot tools/functions"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_definitions: List[Dict] = []
    
    def register(self, name: str, description: str, parameters: Dict):
        """
        Register a new tool
        
        Args:
            name: Tool name
            description: What the tool does
            parameters: Parameter schema
        """
        def decorator(func: Callable):
            self.tools[name] = func
            self.tool_definitions.append({
                "name": name,
                "description": description,
                "parameters": parameters
            })
            return func
        return decorator
    
    def execute(self, name: str, **kwargs) -> Any:
        """Execute a tool by name"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        return self.tools[name](**kwargs)
    
    def get_definitions(self) -> List[Dict]:
        """Get all tool definitions for AI"""
        return self.tool_definitions


# Initialize tool registry
tool_registry = ToolRegistry()


# ========================================
# EXAMPLE TOOLS - Customize for your needs
# ========================================

@tool_registry.register(
    name="get_current_time",
    description="Get the current date and time",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    }
)
def get_current_time() -> str:
    """Get current time"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool_registry.register(
    name="calculate",
    description="Perform basic mathematical calculations",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
            }
        },
        "required": ["expression"]
    }
)
def calculate(expression: str) -> float:
    """Safe calculator"""
    try:
        # Only allow basic math operations for safety
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression, {"__builtins__": {}})
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ========================================
# ADD YOUR CUSTOM TOOLS HERE
# ========================================

# Example template for custom tool:
"""
@tool_registry.register(
    name="your_tool_name",
    description="What your tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)
def your_tool_name(param1: str) -> Any:
    # Your implementation here
    return result
"""
