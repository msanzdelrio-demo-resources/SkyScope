#!/bin/bash
# Installation script for Git hooks
# Run this script from the project root directory

set -e  # Exit on error

echo "🔧 Installing Git hooks for SkyScope..."
echo ""

# Check if .git directory exists
if [ ! -d ".git" ]; then
    echo "❌ Error: .git directory not found"
    echo "   This script must be run from the project root directory"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Install pre-commit hook
if [ -f ".git-hooks/pre-commit" ]; then
    echo "📋 Installing pre-commit hook..."
    cp .git-hooks/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "   ✅ pre-commit hook installed"
else
    echo "⚠️  Warning: .git-hooks/pre-commit not found"
fi

echo ""
echo "✅ Git hooks installation complete!"
echo ""
echo "Installed hooks:"
ls -la .git/hooks/ | grep -v "\.sample$" | grep -E "pre-commit" || echo "   (none)"
echo ""
echo "The pre-commit hook will now:"
echo "  • Block commits with hardcoded secrets"
echo "  • Prevent .env file commits"
echo "  • Scan for API keys in frontend code"
echo "  • Warn about security TODOs"
echo ""
echo "To test the hook, try committing a file with a hardcoded secret."
echo "To bypass temporarily (not recommended): git commit --no-verify"
echo ""
