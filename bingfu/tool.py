"""
Tool module (工具/兵器模块)
Defines the Tool class — represents weapons or instruments an Agent can use.
"""

from typing import Any, Callable, Optional
from pydantic import BaseModel, Field


class Tool(BaseModel):
    """
    Tool (工具/兵器) — something an Agent can use to perform tasks.
    Inspired by ancient Chinese warfare weapons.
    """
    
    name: str = Field(..., description="Tool name (e.g., 'Sword', 'Compass')")
    description: Optional[str] = Field(default=None, description="Tool description")
    function: Optional[Callable] = Field(
        default=None,
        exclude=True,  # Exclude from serialization
        description="Optional function to execute"
    )
    
    class Config:
        arbitrary_types_allowed = True
    
    def use(self, *args, **kwargs) -> Any:
        """
        Use the tool (call its function if available).
        
        Returns:
            Any: Result of the function call, or a placeholder message.
            
        Raises:
            NotImplementedError: If no function is attached.
        """
        if self.function is None:
            return f"🔧 Tool '{self.name}' has no function attached (placeholder)."
        
        try:
            return self.function(*args, **kwargs)
        except Exception as e:
            return f"❌ Error using tool '{self.name}': {e}"
    
    @classmethod
    def create(cls, name: str, func: Callable, description: Optional[str] = None) -> "Tool":
        """
        Create a Tool with a function.
        
        Args:
            name (str): Tool name.
            func (Callable): The function to attach.
            description (Optional[str]): Tool description.
            
        Returns:
            Tool: A new Tool instance.
        """
        return cls(name=name, description=description, function=func)
    
    def __str__(self) -> str:
        func_status = "✅ Has function" if self.function else "⚠️ No function"
        return f"Tool(name='{self.name}', description='{self.description}', status={func_status})"
    
    def __repr__(self) -> str:
        return self.__str__()
