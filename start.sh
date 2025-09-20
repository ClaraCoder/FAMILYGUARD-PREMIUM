#!/data/data/com.termux/files/usr/bin/bash

cd ~/familyguard

echo "=================================================="
echo "           FAMILYGUARD PREMIUM"
echo "=================================================="
echo ""
echo "Starting FamilyGuard Premium Server..."
echo ""

# Check if database exists, if not initialize it
if [ ! -f familyguard.db ]; then
    echo "Initializing database..."
    python setup_database.py
fi

# Check if server is already running
if pgrep -f "python app.py" > /dev/null; then
    echo "Stopping existing server..."
    pkill -f "python app.py"
    sleep 2
fi

# Start the server
echo "Starting server on http://localhost:5000"
python app.py
EOL

chmod +x start.sh
