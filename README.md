# **SilkSound** <!-- omit in toc -->

### Table of Contents <!-- omit in toc -->
- [Setup Guide](#setup-guide)
  - [Project Setup](#project-setup)
  - [Running](#running)
- [Commands](#commands)
  - [Admin](#admin)
  - [Music](#music)

## Setup Guide

### Project Setup
1. Create a `.env` file with the following variables in the root folder:
   - PROJECT_NAME: Name of the project
   - BOT_TOKEN: Your unique Discord bot token
   - ENVIRONMENT:
      - `dev` Has logs for debugging
      - `prod` Cleaner logs for regular use
2. Create a Python virtual environment and install the `requirements.txt`
    - `pip install -r requirements.txt`
3. Add `ffmpeg.exe` to the root folder
    - File can be downloaded here: [ffmpeg](https://ffmpeg.org/download.html#build-windows)

### Running
1. Run `main.py` in the virtual environment
    - Invite the bot to your server and enjoy

> Created with Python 3.11.2

## Commands
Default command prefix is `!`

### Admin
1. !reload** - Reload all modules
2. !quit** - Turn off the bot gracefully

> ** Only bot owner can execute these commands

### Music
1. !join - Join your voice channel
2. !leave - Leave your voice channel
3. !play `url` - Play audio from a Youtube video
    - url - Youtube video link