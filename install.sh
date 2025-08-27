echo "Installing started..."
apt install yt-dlp -y
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
echo "[TELEGRAM]" > config.ini
echo "token = " >> config.ini
echo "my_chat = " >> config.ini
touch cookies.txt
echo "Add telegram bot token and your chat id to config.ini and browser cookies to cookies.txt"