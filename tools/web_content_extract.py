from collections.abc import Generator
from typing import Any
import subprocess
import json
import logging
import os
import shutil

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
            # Log the parameters for debugging
            logger.info(f"WebContentExtractTool called with URL: {url}, include_seo: {include_seo}, format: {format_type}")
            
            # Check if Node.js and npx are available
            node_path = shutil.which("node")
            npx_path = shutil.which("npx")
            
            if not node_path:
                yield self.create_text_message("Error: Node.js not found in the system. Please ensure Node.js is installed and available in PATH.")
                return
                
            if not npx_path:
                yield self.create_text_message("Error: npx not found in the system. Please ensure Node.js/npm is installed and available in PATH.")
                return
            
            # Log Node.js and npx paths for debugging
            logger.info(f"Node.js path: {node_path}")
            logger.info(f"npx path: {npx_path}")
            
            # Build command to call web-content-extract CLI
            cmd = ["npx", "web-content-extract", url]
            
            # Add SEO flag if requested
            if include_seo:
                cmd.append("--seo")
            
            # Always use JSON format for consistent parsing
            cmd.append("--json")
            
            # Log the command being executed
            logger.info(f"Executing command: {' '.join(cmd)}")
            
            # Set environment variables to ensure proper execution
            env = os.environ.copy()
            env["PATH"] = os.environ.get("PATH", "")
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                env=env
            )
            
            # Log command execution results for debugging
            logger.info(f"Command execution completed. Return code: {result.returncode}")
            logger.info(f"STDOUT: {result.stdout[:500]}...")  # Log first 500 characters of stdout
            if result.stderr:
                logger.info(f"STDERR: {result.stderr}")
            
            # Check if command was successful
            if result.returncode != 0:
                error_msg = f"Command failed with return code {result.returncode}"
                if result.stderr:
                    error_msg += f": {result.stderr}"
                yield self.create_text_message(f"Error extracting content: {error_msg}")
                return
            
            # Check if stdout is empty
            if not result.stdout.strip():
                yield self.create_text_message("Error: Command executed successfully but returned empty output.")
                return
            
            # Parse the JSON output
            try:
                output_data = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                yield self.create_text_message(f"Error parsing JSON output. Raw output: {result.stdout[:500]}... Error: {str(e)}")
                return
            
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
        except FileNotFoundError as e:
            yield self.create_text_message(f"Error: npx or web-content-extract not found. Please ensure Node.js is installed. Detailed error: {str(e)}")
        except json.JSONDecodeError as e:
            yield self.create_text_message(f"Error parsing JSON output: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in WebContentExtractTool: {str(e)}", exc_info=True)
            yield self.create_text_message(f"Error extracting content: {str(e)}")