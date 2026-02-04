#!/bin/bash

# Complete Railway Deployment Script
# Run this script to deploy BibleWay backend to Railway

set -e  # Exit on error

echo "🚂 BibleWay Backend - Railway Deployment"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI is not installed!${NC}"
    echo ""
    echo "Install with:"
    echo "  npm install -g @railway/cli"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Railway CLI is installed${NC}"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Railway${NC}"
    echo "Logging in..."
    railway login
    echo ""
fi

echo -e "${GREEN}✅ Logged in to Railway${NC}"
echo ""

# Check if project is linked
if ! railway status &> /dev/null; then
    echo -e "${YELLOW}⚠️  No Railway project linked${NC}"
    echo ""
    echo "Choose an option:"
    echo "  1) Create new project"
    echo "  2) Link existing project"
    read -p "Enter choice (1 or 2): " choice
    echo ""

    if [ "$choice" = "1" ]; then
        echo "Creating new Railway project..."
        railway init
    else
        echo "Linking to existing project..."
        railway link
    fi
    echo ""
fi

echo -e "${GREEN}✅ Project linked${NC}"
echo ""

# Upload environment variables
echo "📤 Uploading environment variables..."
if [ -f .env ]; then
    ./upload-env-to-railway.sh
    echo ""
else
    echo -e "${RED}❌ .env file not found!${NC}"
    exit 1
fi

# Deploy
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "⏳ Waiting for deployment to complete..."
sleep 5

# Show logs
echo ""
echo "📋 Recent logs:"
railway logs --tail 50

echo ""
echo "🔄 Running database migrations..."
railway run python manage.py migrate

echo ""
echo "📦 Collecting static files..."
railway run python manage.py collectstatic --noinput

echo ""
echo "🔍 Indexing Elasticsearch chapters..."
railway run python manage.py index_chapters

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""

# Get domain
DOMAIN=$(railway domain 2>/dev/null || echo "No domain configured")
echo "🌐 Your application is available at:"
echo "   $DOMAIN"
echo ""

echo "📝 Next steps:"
echo "  1. Create superuser: railway run python manage.py createsuperuser"
echo "  2. Configure custom domain: railway domain add api.bibleway.io"
echo "  3. Set up Cloudflare DNS CNAME record"
echo "  4. Test your API: https://api.bibleway.io/admin/"
echo ""

echo -e "${GREEN}🎉 Deployment successful!${NC}"
