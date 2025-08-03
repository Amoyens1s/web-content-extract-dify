# Web Content Extract Dify Plugin

This is a Dify plugin that integrates with the [web-content-extract-mcp](https://github.com/Amoyens1s/web-content-extract-mcp) MCP server to extract clean content from web pages.

## Features

- Extracts main content from web pages using Mozilla Readability
- Converts content to Markdown or JSON format
- Extracts comprehensive SEO metadata
- Integrates seamlessly with Dify applications through the Model Context Protocol (MCP)

## Prerequisites

This plugin requires the [web-content-extract-mcp](https://github.com/Amoyens1s/web-content-extract-mcp) server to be configured in your Dify environment. The MCP server can be installed and run in two ways:

1. Direct installation:

   ```bash
   npm install -g web-content-extract-mcp
   web-content-extract-mcp
   ```

2. Using npx (no installation required):
   ```bash
   npx web-content-extract-mcp
   ```

## Installation Options

### Option 1: Self-hosted Dify (Recommended)

If you're using a self-hosted Dify instance, you can configure the MCP server directly in your Dify environment:

1. Install the web-content-extract-mcp server:

   ```bash
   npm install -g web-content-extract-mcp
   ```

2. Configure the MCP server in your Dify environment by adding the following to your MCP settings:
   ```json
   {
     "mcpServers": {
       "web-extract": {
         "command": "npx",
         "args": ["web-content-extract-mcp"],
         "disabled": false
       }
     }
   }
   ```

### Option 2: Dify SaaS

If you're using Dify's SaaS offering, direct MCP server configuration may not be available. In this case, you have two options:

1. Request MCP server support from Dify team
2. Use an alternative approach where the plugin directly calls the web-content-extract library (requires Node.js environment)

## Installation

To install this plugin in Dify:

1. Package the plugin using the Dify plugin development tools
2. Upload the packaged plugin to your Dify instance
3. Configure the plugin with your desired settings
4. Ensure the web-content-extract-mcp server is configured in your MCP settings (for self-hosted instances)

## Usage

Once installed, this plugin provides a tool that can be used in Dify workflows to extract content from web pages. The tool accepts the following parameters:

- `url` (required): The URL of the web page to extract content from
- `include_seo` (optional, default: true): Whether to include SEO metadata in the output
- `format` (optional, default: "markdown"): The output format, either "markdown" or "json"

## Development

This plugin follows the Dify plugin development guidelines. For more information on developing Dify plugins, refer to the [Dify documentation](https://docs.dify.ai/zh-hans/plugins/quick-start/develop-plugins/tool-plugin).
