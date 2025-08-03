from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class WebContentExtractTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Extract parameters
        url = tool_parameters.get("url")
        include_seo = tool_parameters.get("include_seo", True)
        format_type = tool_parameters.get("format", "markdown")
        
        # Validate URL parameter
        if not url:
            yield self.create_text_message("Error: URL parameter is required")
            return
        
        try:
            # Use the MCP client to call the web-content-extract-mcp server
            # The server should be configured in the Dify environment
            mcp_client = self.runtime.mcp_client
            
            # Prepare the parameters for the MCP tool call
            mcp_params = {
                "url": url,
                "includeSeo": include_seo,
                "format": format_type
            }
            
            # Call the extract_web_content tool on the web-extract MCP server
            result = mcp_client.call_tool("web-extract", "extract_web_content", mcp_params)
            
            # Process the result based on the requested format
            if format_type == "json":
                yield self.create_json_message(result)
            else:
                # For markdown format, the result should already be in the correct format
                yield self.create_text_message(result.get("content", ""))
                
        except Exception as e:
            yield self.create_text_message(f"Error extracting content: {str(e)}")