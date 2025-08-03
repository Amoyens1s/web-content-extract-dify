from typing import Any

from dify_plugin import ToolProvider
from tools.web_content_extract import WebContentExtractTool

class WebContentExtractProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate the credentials for the Web Content Extract provider.
        Since this tool now uses the web-content-extract CLI directly,
        we don't need to validate MCP server connectivity.
        """
        # No validation needed as the tool uses CLI directly
        # In the future, we could check if Node.js and npx are available
        pass