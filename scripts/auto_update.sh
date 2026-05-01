#!/bin/bash
# Auto-update OpenRouter free models data
# Runs daily at 21:00 Beijing time (13:00 UTC)

cd ~/openrouter-free-dashboard

# Backup current models.json
cp data/models.json data/models.json.bak 2>/dev/null || true

# Run fetch script
python3 fetch_models.py > /tmp/fetch_output.txt 2>&1

# Check if models.json changed
if ! diff -q data/models.json data/models.json.bak > /dev/null 2>&1; then
    # Files differ - new models detected
    echo "New models detected, committing..."
    
    # Get list of new models
    NEW_MODELS=$(python3 -c "
import json
try:
    old = json.load(open('data/models.json.bak'))
    new = json.load(open('data/models.json'))
    old_ids = set(m['id'] for m in old['models'])
    new_ids = set(m['id'] for m in new['models'])
    added = new_ids - old_ids
    if added:
        models = [m for m in new['models'] if m['id'] in added]
        for m in models:
            print(f\"- {m['name']} ({m['id']})\")
except:
    pass
")
    
    # Commit and push
    git add data/models.json
    git commit -m "Auto-update: New models detected ($(date -u +%Y-%m-%d\ %H:%M\ UTC))"
    git push origin main 2>&1
    
    # Send Telegram notification with new model list
    if [ -n "$NEW_MODELS" ]; then
        echo "New models found: $NEW_MODELS"
        # Notification will be sent by Hermes cron job deliver feature
        echo "$NEW_MODELS" > /tmp/new_models.txt
    fi
else
    echo "No new models, skipping commit"
fi

# Cleanup
rm -f data/models.json.bak
