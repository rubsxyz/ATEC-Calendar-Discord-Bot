# Atec Send Calendar to Discord

This repository sends a .png of an ATEC calendar image to any Discord server.

## Features

- **Automated login to the ATEC training server.**
- **Navigation to the personal calendar page.**
- **Capture of the calendar as a .png screenshot.**
- **Automated posting of the screenshot to a specified Discord server.**

## Requirements

- **Python 3.6+**
- **`selenium`**
- **`pillow`**
- **`discord.py`**
- **`aiohttp`**
- **`python-dotenv`**
- **Google Chrome**
- **ChromeDriver**

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/rubsxyz/ATEC-Calendar-Discord-Bot.git
    cd atec_send_calendar_discord
    ```

2. **Set Up a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the root directory of the project with the following content:

    ```plaintext
    LOGIN_URL=https://trainingserver.atec.pt/trainingserver/
    USERNAME=your_username
    PASSWORD=your_password
    DISCORD_TOKEN=your_discord_token
    CHANNEL_ID=your_discord_channel_id
    ```

    Replace `your_username`, `your_password`, `your_discord_token`, and `your_discord_channel_id` with your actual ATEC login credentials and Discord bot token and channel ID.

5. **Ensure ChromeDriver is in Your PATH:**

    Make sure that ChromeDriver is installed and added to your system PATH. You can download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

To run the script, execute:

```bash
python main.py
```

The script will:

1. **Log into the ATEC training server using the provided credentials.**
2. **Navigate to the personal calendar page.**
3. **Capture a screenshot of the calendar.**
4. **Send the screenshot to the specified Discord channel.**

## Logging

The script logs its actions and any errors encountered in a `bot.log` file in the root directory. This file is overwritten each time the script runs.

## Troubleshooting

- **Login Issues:** Ensure that your username and password are correctly entered in the `.env` file.
- **Discord Bot Issues:** Ensure that your Discord bot token and channel ID are correctly entered in the `.env` file and that your bot has permission to post in the specified channel.
- **ChromeDriver Issues:** Ensure that ChromeDriver is correctly installed and added to your system PATH.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [Pillow (PIL Fork)](https://python-pillow.org/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)


