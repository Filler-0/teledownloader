echo "Installing started..."
python3 -m pip install -r requirements
echo "[TELEGRAM]" > config.ini
echo "token = " >> config.ini
echo "my_chat = " >> config.ini
echo "Add telegram bot token and your chat id to config.ini"