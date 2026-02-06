#!/bin/bash
# Install Daily Market Intelligence Dashboard as a standalone Linux app

set -e

APP_DIR="/home/mattz/.openclaw/workspace/daily-intel-dashboard"
APP_SCRIPT="$APP_DIR/app/market_dashboard.py"
DESKTOP_FILE="$APP_DIR/app/daily-market-intel.desktop"
INSTALL_DIR="$HOME/.local/share/applications"
ICON_SOURCE="$APP_DIR/app/icon.png"

echo "📊 Installing Daily Market Intelligence Dashboard..."

# Check Python dependencies
echo "Checking dependencies..."
if ! python3 -c "import requests, bs4, tkinter" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install --user --break-system-packages requests beautifulsoup4
fi

# Create icon (simple PNG)
echo "Creating app icon..."
if [ ! -f "$ICON_SOURCE" ]; then
    # Create a simple colored square as icon using Python
    python3 << 'EOF'
from PIL import Image, ImageDraw

img = Image.new('RGB', (64, 64), color='#1a1a2e')
draw = ImageDraw.Draw(img)
# Draw a simple chart icon
draw.rectangle([10, 20, 54, 50], fill='#e94560', outline='#e94560')
draw.rectangle([20, 15, 35, 45], fill='#4ecca3', outline='#4ecca3')
draw.rectangle([40, 25, 50, 45], fill='#ffc107', outline='#ffc107')
img.save('/home/mattz/.openclaw/workspace/daily-intel-dashboard/app/icon.png')
print("Icon created")
EOF
fi

# Install .desktop file
echo "Installing desktop launcher..."
mkdir -p "$INSTALL_DIR"
cp "$DESKTOP_FILE" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/daily-market-intel.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$INSTALL_DIR"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📊 You can now launch the app from:"
echo "   • Ubuntu Activities: Search 'Daily Market Intelligence'"
echo "   • Command line: python3 $APP_SCRIPT"
echo ""
echo "📁 App location: $APP_DIR"
echo "🔧 Desktop file: $INSTALL_DIR/daily-market-intel.desktop"
echo ""

# Make the script executable
chmod +x "$APP_SCRIPT"
