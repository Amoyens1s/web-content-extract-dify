#!/usr/bin/env python3
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Dify plugin framework
from dify_plugin import Plugin

# Import our provider
from provider.web_content_extract import WebContentExtractProvider

# Create the plugin instance
plugin = Plugin(
    provider=WebContentExtractProvider(),
    tools=[
        "tools/web_content_extract.yaml"
    ]
)

# Run the plugin
if __name__ == "__main__":
    plugin.run()