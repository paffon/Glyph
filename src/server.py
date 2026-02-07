if __name__ == "__main__":
    try:
        from mcp_object import mcp

        # Prompts (consolidated)
        from prompts.prompts import (
            create_design_log_prompt,
            create_operation_doc_prompt,
            planning_prompt,
            implementation_prompt,
            code_review_prompt,
            sync_lessons_learned_prompt,
            compact_conversation_prompt
        )

        # Skills/Knowledge (consolidated)
        from skills.knowledge import (
            get_glyph_overview,
            get_principles,
            get_example,
            read_asset_exact,
            
        )

        # Tools (action tools)
        from tools.init_assistant_dir import init_assistant_dir
        from tools.add_design_log import add_design_log
        from tools.add_operation import add_operation
        from tools.persist_artifact import persist_artifacts
        from tools.reference_graph import update_reference_graph, get_references_from, find_references_to
        from tools.static_code_analysis import static_code_analysis

        print("Starting MCP server...")

        mcp.run()
    except KeyboardInterrupt:
        print("MCP server stopped by user.")
        pass
