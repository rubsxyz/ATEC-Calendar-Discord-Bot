<p align="center">
    <img alt="Version" src="https://img.shields.io/github/v/tag/rubsxyz/ATEC-Calendar-Discord-Bot?label=Version%3A" />
    </a>
  <a href="#" target="_blank">
    <img alt="License: Apache-2.0" src="https://img.shields.io/github/license/rubsxyz/ATEC-Calendar-Discord-Bot" />
  </a>
    <a><img alt="Is Mantained?" src="https://img.shields.io/badge/Mantained:-yes-green.svg" />
  </a>
</p>

<h1 align="center">
ATEC Discord Bot
</h1>

<p align="center">
 <img src="https://github.com/rubsxyz/ATEC-Calendar-Discord-Bot/blob/main/images/favicon.png?raw=true" width="400">
</p>

# Atec Send Calendar to Discord!

This repository hosts a bot that automates the process of logging into the ATEC training server, capturing a screenshot of your personal calendar, and posting it to a specified Discord channel.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Issues](#issues)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## ✨ Features

- **Automated login to the ATEC training server.**
- **Navigation to the personal calendar page.**
- **Capture of the calendar as a .png screenshot.**
- **Automated posting of the screenshot to a specified Discord server.**

## ⚠️ Requirements

- **Python 3.6+**
- **`selenium`**
- **`pillow`**
- **`discord.py`**
- **`aiohttp`**
- **`python-dotenv`**
- **Google Chrome**
- **ChromeDriver**

## 🛑 Installation

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

    To create a Discord bot and get the token, follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html).

5. **Ensure ChromeDriver is in Your PATH:**

    Make sure that ChromeDriver is installed and added to your system PATH. You can download ChromeDriver from [here](https://developer.chrome.com/docs/chromedriver/downloads).

## ⚙️ Usage

To run the script, execute:

```bash
python main.py
```

##  The script will:

1. **Log into the ATEC training server using the provided credentials.**
2. **Navigate to the personal calendar page.**
3. **Capture a screenshot of the calendar.**
4. **Send the screenshot to the specified Discord channel.**

## Logging

The script logs its actions and any errors encountered in a `bot.log` file in the root directory. This file is overwritten each time the script runs.

## 🔨 Troubleshooting

- **Login Issues:** Ensure that your username and password are correctly entered in the `.env` file.
- **Discord Bot Issues:** Ensure that your Discord bot token and channel ID are correctly entered in the `.env` file and that your bot has permission to post in the specified channel.
- **ChromeDriver Issues:** Ensure that ChromeDriver is correctly installed and added to your system PATH.

## Project Structure

```
ATEC-Calendar-Discord-Bot/
│
├── src/
│ ├── init.py
│ ├── calendar_interaction.py
│ ├── config.py
│ ├── discord_bot.py
│ ├── web_interaction.py
│
├── img/ (created at first run)
│ └── (Captured images are stored here)
│
├── .env (read Installation)
├── .gitignore
├── LICENSE.txt
├── README.md 
├── bot.log (created at first run)
├── main.py
└── requirements.txt
```

## 🤝 Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 🛑 Issues

If you encounter any issues, please open a new issue in the [Issues](https://github.com/rubsxyz/ATEC-Calendar-Discord-Bot/issues) section of the repository.

## 📢 Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [Pillow (PIL Fork)](https://python-pillow.org/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## License

>This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE.txt) file for details.
