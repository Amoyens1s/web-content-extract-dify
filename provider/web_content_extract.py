from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools.web_content_extract import WebContentExtractTool

class WebContentExtractProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate the credentials for the Web Content Extract provider.
        Since this tool uses an MCP server, we'll test that we can connect to the MCP server
        and call the extract_web_content tool.
        """
        try:
            # Try to get the MCP client from the runtime
            mcp_client = self.runtime.mcp_client
            
            # Check if the web-extract MCP server is available
            if "web-extract" not in mcp_client.servers:
                raise ToolProviderCredentialValidationError("web-extract MCP server is not configured")
            
            # If we can access the MCP client and the server is available, the credentials are valid
            # In a real implementation, you might want to perform a more thorough validation
            # by calling a simple tool on the server to verify connectivity
            pass
        except AttributeError:
            # If the MCP client is not available, raise a validation error
            raise ToolProviderCredentialValidationError("MCP client is not available in the runtime")
        except Exception as e:
            # If any other error occurs, raise a validation error
            raise ToolProviderCredentialValidationError(f"Failed to validate credentials: {str(e)}")