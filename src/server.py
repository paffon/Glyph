if __name__ == "__main__":
    try:
        from mcp_object import mcp

        from prompts.compact_conversation import compact_conversation

        from tools.init_assistant_dir import init_assistant_dir
        from tools.md_to_dict import md_to_dict

        print("Starting MCP server...")

        mcp.run()
    except KeyboardInterrupt:
        print("MCP server stopped by user.")
        pass
