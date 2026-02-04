#!/bin/bash

# Upload environment variables to Railway
# Usage: ./upload-env-to-railway.sh

echo "🚂 Uploading environment variables to Railway..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Make sure you're in the bibleway-be directory"
    exit 1
fi

# Read .env file line by line and set variables
while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines and comments
    if [[ -z "$line" ]] || [[ "$line" =~ ^[[:space:]]*# ]]; then
        continue
    fi

    # Extract key and value
    if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"

        # Remove leading/trailing whitespace
        key=$(echo "$key" | xargs)

        # Skip if key is empty
        if [[ -z "$key" ]]; then
            continue
        fi

        echo "Setting: $key"
        railway variables set "$key=$value"
    fi
done < .env

echo ""
echo "✅ All environment variables uploaded!"
echo ""
echo "Verify with: railway variables"
