"""
Signal module (信号模块)
Implements Drum (击鼓) and Gong (鸣金) signals,
inspired by ancient Chinese warfare communication.
"""

from typing import Any, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum


class SignalType(str, Enum):
    """Signal types (信号类型) — inspired by ancient Chinese warfare."""
    DRUM = "drum"       # 击鼓 — start/advance
    GONG = "gong"        # 鸣金 — stop/retreat
    HORN = "horn"        # 号角 — gather/assemble (future)
    FLAG = "flag"        # 旗帜 — direction/command (future)


class Signal(BaseModel):
    """
    Signal (信号) — base class for all signals.
    Inspired by ancient Chinese warfare communication.
    """
    
    signal_type: SignalType = Field(..., description="Type of signal")
    sender: Optional[str] = Field(default=None, description="Sender name (e.g., 'Marshal')")
    recipient: Optional[str] = Field(default=None, description="Recipient name (e.g., 'Agent-X')")
    message: Optional[str] = Field(default=None, description="Optional message attached to the signal")
    timestamp: Optional[float] = Field(default=None, description="Timestamp of the signal")
    
    class Config:
        use_enum_values = True
    
    def send(self) -> str:
        """
        Send the signal (placeholder implementation).
        
        Returns:
            str: Signal sent message.
        """
        emoji = "🥁" if self.signal_type == SignalType.DRUM else "🔔"
        recipient_str = f" to {self.recipient}" if self.recipient else ""
        msg = f"{emoji} {self.signal_type.upper()} signal sent{recipient_str}"
        if self.message:
            msg += f": {self.message}"
        return msg
    
    def __str__(self) -> str:
        return self.send()
    
    def __repr__(self) -> str:
        return f"Signal(type='{self.signal_type}', sender='{self.sender}', recipient='{self.recipient}')"


class Drum(Signal):
    """
    Drum signal (击鼓) — start or advance.
    In ancient China, drum signals meant: advance, attack, start.
    """
    
    def __init__(self, **kwargs):
        kwargs["signal_type"] = SignalType.DRUM
        super().__init__(**kwargs)
    
    def send(self) -> str:
        """
        Send drum signal (击鼓).
        
        Returns:
            str: Drum signal message.
        """
        recipient_str = f" to '{self.recipient}'" if self.recipient else ""
        msg = f"🥁 Drum{recipient_str}"
        if self.message:
            msg += f": {self.message}"
        return msg


class Gong(Signal):
    """
    Gong signal (鸣金) — stop or retreat.
    In ancient China, gong signals meant: stop, retreat, cease fighting.
    """
    
    def __init__(self, **kwargs):
        kwargs["signal_type"] = SignalType.GONG
        super().__init__(**kwargs)
    
    def send(self) -> str:
        """
        Send gong signal (鸣金).
        
        Returns:
            str: Gong signal message.
        """
        recipient_str = f" to '{self.recipient}'" if self.recipient else ""
        msg = f"🔔 Gong{recipient_str}"
        if self.message:
            msg += f": {self.message}"
        return msg


# Helper functions (辅助函数)

def drum(sender: Optional[str] = None, recipient: Optional[str] = None, message: Optional[str] = None) -> str:
    """
    Helper function to send a drum signal (击鼓).
    
    Args:
        sender (Optional[str]): Sender name.
        recipient (Optional[str]): Recipient name.
        message (Optional[str]): Optional message.
        
    Returns:
        str: Drum signal message.
    """
    d = Drum(sender=sender, recipient=recipient, message=message)
    return d.send()


def gong(sender: Optional[str] = None, recipient: Optional[str] = None, message: Optional[str] = None) -> str:
    """
    Helper function to send a gong signal (鸣金).
    
    Args:
        sender (Optional[str]): Sender name.
        recipient (Optional[str]): Recipient name.
        message (Optional[str]): Optional message.
        
    Returns:
        str: Gong signal message.
    """
    g = Gong(sender=sender, recipient=recipient, message=message)
    return g.send()
