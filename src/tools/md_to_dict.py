from typing import Dict, List, Any
from markdown_it import MarkdownIt

from mcp_object import mcp
from response import GlyphMCPResponse


class MarkdownSection:
    """Represents a hierarchical section of a markdown document."""
    
    def __init__(self, level: int, title: str, content: str = ""):
        self.level = level
        self.title = title
        self.content = content
        self.children: List[MarkdownSection] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert section to dictionary format."""
        result = {
            "level": self.level,
            "title": self.title,
            "content": self.content.strip()
        }
        if self.children:
            result["subsections"] = [child.to_dict() for child in self.children]
        return result


def _parse_markdown_hierarchy(tokens) -> List[MarkdownSection]:
    """Parse markdown tokens into a hierarchical structure."""
    sections = []
    stack: List[MarkdownSection] = []
    content_buffer = []
    pending_header = None
    
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            # Save any accumulated content to the current section
            if stack and content_buffer:
                stack[-1].content += "".join(content_buffer).strip()
                content_buffer = []
            
            # Extract level from tag (h1 -> 1, h2 -> 2, etc.)
            level = int(token.tag[1])
            pending_header = {"level": level}
            
        elif token.type == "inline" and pending_header:
            # This is the header text
            title = token.content
            new_section = MarkdownSection(pending_header["level"], title)
            
            # Pop sections from stack that are at same or deeper level
            while stack and stack[-1].level >= new_section.level:
                stack.pop()
            
            # Add new section to parent or root
            if stack:
                stack[-1].children.append(new_section)
            else:
                sections.append(new_section)
            
            stack.append(new_section)
            pending_header = None
            
        elif token.type not in ["heading_open", "heading_close"]:
            # Accumulate content
            if token.content:
                content_buffer.append(token.content)
    
    # Save final content
    if stack and content_buffer:
        stack[-1].content += "".join(content_buffer).strip()
    
    return sections


@mcp.tool()
def md_to_dict(file_path: str) -> GlyphMCPResponse[Dict[str, Any]]:
    """
    Parses a Markdown file into a hierarchical dictionary structure.
    
    Args:
        file_path: Path to the .md file. Absolute path is required.
        
    Returns:
        A hierarchical dictionary where each section contains:
        - level: header level (1-6)
        - title: header text
        - content: text content under this header
        - subsections: list of nested sections (if any)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        md = MarkdownIt()
        tokens = md.parse(md_text)
        
        sections = _parse_markdown_hierarchy(tokens)
        
        result = {
            "sections": [section.to_dict() for section in sections]
        }

        return GlyphMCPResponse[Dict[str, Any]](success=True, result=result)
    except Exception as e:
        return GlyphMCPResponse[Dict[str, Any]](success=False, context=[f"Error: {str(e)}"])