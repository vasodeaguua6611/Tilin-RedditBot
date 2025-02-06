# Tilin Reddit Bot

A Reddit bot that responds to mentions of MY FUFFY BOY RALSEI in comments (He's my boyfriend fr) with love emojis. Built with Python and Tkinter.

## IMPORTANT: FOR LAZY PPL WHO AREN'T BOTHERING TO READ THE SRC

This bot is super customizable! You can make it respond to literally ANY word or phrase you want - not just Ralsei stuff. Go wild with it! Or not. It's all in the code's variables lmao.

## Features

- GUI interface for bot control
- Real-time activity monitoring
- Automatic comment detection and response
- Custom theme with background image support

## Credits

Huge shoutout to:

- Gabriel/Xuyaxaki - Main dev & Ralsei enthusiast
- Akoza - eldiablo
- Peppy - dios

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/Tilin-RedditBot.git
cd Tilin-RedditBot
```

2. Install dependencies:

```bash
pip install praw pillow
```

3. Set up your Reddit API credentials:

   - Go to https://www.reddit.com/prefs/apps
   - Create a new application
   - Select "script" as the application type
   - Note your client_id and client_secret

4. Configure the bot:

   - Copy `config.example.py` to `config.py`
   - Fill in your Reddit credentials in `config.py`

5. Run the bot:

```bash
python bot-1.py
```

## Configuration

Create a `config.py` file with your Reddit API credentials:

```python
username = "your_reddit_username"
password = "your_reddit_password"
client_id = "your_client_id"
client_secret = "your_client_secret"
```

## Usage

1. Start the application
2. Click "Start Bot" to begin monitoring
3. The bot will automatically respond to comments containing "Ralsei" or "Kris" (Or anything you imput IN THE CODE, I AIN'T UPDATING TS)
4. Monitor activity in the log window
5. Click "Stop Bot" to end monitoring

## Customization

- Drop your own bg image in `assets/background.png`
- Change the trigger words to whatever you want in `bot_loop()` - fr fr, make it yours!
- Mess with the GUI colors in `configure_styles()` if you're feeling fancy

## License

This project is licensed under the MIT License - see the LICENSE file for details.
