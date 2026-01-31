from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class GlyphMCPResponse(BaseModel, Generic[T]):
    success: bool = False
    context: List[str] = Field(default_factory=list)
    result: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def add_context(self, message: str) -> None:
        """Add a context message (comment gathered during run)"""
        self.context.append(message)