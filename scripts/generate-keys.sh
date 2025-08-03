#!/bin/bash

# Script to generate signing keys for Dify plugin
# This script should only be run by project maintainers who need to sign releases

echo "Generating Dify plugin signing keys..."

# Check if dify command is available
if ! command -v dify &> /dev/null
then
    echo "Error: dify command not found. Please install Dify CLI first."
    echo "You can install it with: go install github.com/langgenius/dify-cli@latest"
    exit 1
fi

# Generate key pair
KEY_NAME="web-content-extract-plugin"
dify signature generate --filename ${KEY_NAME}

echo ""
echo "Keys generated successfully!"
echo "Private key: ${KEY_NAME}.private.pem (KEEP THIS SECRET!)"
echo "Public key: ${KEY_NAME}.public.pem"
echo ""
echo "IMPORTANT SECURITY NOTES:"
echo "1. NEVER commit the private key to the repository"
echo "2. Add the private key to your .gitignore file"
echo "3. For GitHub Actions, add the private key content to repository secrets"
echo "4. Keep the private key in a secure location"
echo ""
echo "For more information, see README_SIGNING.md"