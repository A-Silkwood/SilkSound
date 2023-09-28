# SilkSound
### Setup
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

### How to run
1. Run `main.py` in the virtual environment
    - Invite the bot to your server and enjoy