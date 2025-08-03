from collections.abc import Generator
from typing import Any
import subprocess
import json
import logging

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

logger = logging.getLogger(__name__)

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
            # Build command to call web-content-extract CLI
            cmd = ["npx", "web-content-extract", url]
            
            # Add SEO flag if requested
            if include_seo:
                cmd.append("--seo")
            
            # Always use JSON format for consistent parsing
            cmd.append("--json")
            
            logger.info(f"Executing command: {' '.join(cmd)}")
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            # Check if command was successful
            if result.returncode != 0:
                error_msg = f"Command failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr}"
                yield self.create_text_message(f"Error extracting content: {error_msg}")
                return
            
            # Parse the JSON output
            output_data = json.loads(result.stdout)
            
            # Process the result based on the requested format
            if format_type == "json":
                yield self.create_json_message(output_data)
            else:
                # For markdown format, extract the content
                content = output_data.get("content", "")
                if include_seo and output_data.get("seo"):
                    # Add SEO metadata as front matter or in the content
                    seo_info = output_data.get("seo", {})
                    title = output_data.get("title", seo_info.get("title", ""))
                    if title:
                        content = f"# {title}\n\n{content}"
                    
                    # Add other SEO metadata
                    description = seo_info.get("description", "")
                    if description:
                        content = f"{content}\n\n---\nDescription: {description}"
                
                yield self.create_text_message(content)
                
        except subprocess.TimeoutExpired:
            yield self.create_text_message("Error: Content extraction timed out (30 seconds)")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Error parsing JSON output: {str(e)}")
        except FileNotFoundError:
            yield self.create_text_message("Error: npx or web-content-extract not found. Please ensure Node.js is installed.")
        except Exception as e:
            yield self.create_text_message(f"Error extracting content: {str(e)}")