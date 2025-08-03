# Packaging the Web Content Extract Dify Plugin

This document explains how to package the Web Content Extract Dify Plugin for distribution.

## Prerequisites

1. Dify plugin development tools installed
2. Python environment (version ≥ 3.12)

### Installing Dify Plugin Development Tools

To package this plugin, you need to install the Dify plugin development tools first. You can download the appropriate binary for your platform from the Dify documentation or repository.

For example, on macOS with Apple Silicon:

```bash
./dify-plugin-darwin-arm64 plugin init
```

If you've renamed the binary to `dify` and placed it in your PATH:

```bash
dify plugin init
```

Note: As an AI assistant, I cannot directly execute commands on your local machine. You need to download and install the Dify plugin development tools yourself, then follow the instructions below to package the plugin.

## Packaging Steps

1. Ensure all plugin files are in place:

   - `provider/web_content_extract.yaml` - Provider configuration
   - `provider/web_content_extract.py` - Provider implementation
   - `tools/web_content_extract.yaml` - Tool configuration
   - `tools/web_content_extract.py` - Tool implementation
   - `_assets/icon.svg` - Plugin icon
   - `README.md` - Plugin documentation
   - `requirements.txt` - Plugin dependencies

2. Use the Dify plugin development tool to package the plugin:

   ```bash
   dify plugin package ./
   ```

   This command will:

   - Validate the plugin structure
   - Bundle all necessary files
   - Create a `.difypkg` file in the current directory

3. The resulting `web_content_extract.difypkg` file can be installed in Dify.

## Plugin Dependencies

The plugin requires the following dependencies:

- `dify-plugin` - The Dify plugin framework

Note: This plugin does not directly depend on the `web-content-extract` Node.js library. Instead, it communicates with the `web-content-extract-mcp` server through the Model Context Protocol (MCP).

## MCP Server Configuration

The plugin requires the `web-content-extract-mcp` server to be configured in your Dify environment. The server can be installed and run in two ways:

1. Direct installation:

   ```bash
   npm install -g web-content-extract-mcp
   web-content-extract-mcp
   ```

2. Using npx (no installation required):
   ```bash
   npx web-content-extract-mcp
   ```

The MCP server must be configured in your Dify MCP settings:

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

## Installation in Dify

1. Upload the `web_content_extract.difypkg` file to your Dify instance
2. Install the plugin through the Dify plugin management interface
3. Ensure the `web-content-extract-mcp` server is configured in your MCP settings
4. The plugin will be available for use in your Dify applications
