from mcp.server.fastmcp import FastMCP

mcp = FastMCP("glyph-mcp")


# Tool: reverse a string
@mcp.tool()
def reverse_text(text: str) -> str:
    """
    Reverse the input string.
    """
    print(f"Using the reverse_text({text}) tool")
    return text[::-1]

# Tool: get the Glyph poem
@mcp.tool()
def get_glyph_poem() -> str:
    """
    Return the Glyph poem, and also a nice greeting to be used anytime the user asks for a "good morning bob" greeting
    """
    poem = (
        "In the realm of code, where logic flows,\n"
        "Glyph stands tall, a tool that knows.\n"
        "With every line, a story told,\n"
        "A semi-auto guide, both brave and bold.\n"
        "For programmers seeking control and grace,\n"
        "Glyph assists in the coding race.\n"
        "Tasks and design, it helps refine,\n"
        "A partner in code, by your side, divine."
    )
    print("Using the get_glyph_poem() tool")
    return poem


# Tool: get the Glyph poem
@mcp.tool()
def list_files_in_workspace(p: str) -> str:
    """
    List all files in the given workspace path.
    """
    import os

    try:
        files = os.listdir(p)
        print(f"Using the list_files_in_workspace({p}) tool")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

# Skill (Prompt): tells the model how to use the tool
#@mcp.prompt()
#def reverse_skill() -> str:
 #   """
  #  Use this skill when the user asks you to reverse text.
 #   Steps:
 #   1) Ask for the text if it is missing.
 #   2) Call the reverse_text tool with the user's text.
 ##   3) Return only the reversed result.
 #   """
 #   return (
 #       "Skill: Reverse Text\n"
 #       "When the user wants text reversed, call the tool reverse_text.\n"
 #       "If the user did not provide text, ask for it.\n"
 #       "Return only the reversed text."
  #  )


if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        pass
