# c2dc
Command and control made in python with discord api.

## Compile
> python -m nuitka --mingw64 .\main.py --standalone --onefile --windows-disable-console - - enable-static
- Antivirus and browser will detect it as virus.

## Obfuscate 
> Trying to figure out how to avoid AV detection


# Commands

    help - Help command
    cd - Change directory
    ls - List directory
    upload <link> - Upload file
    cmd - Execute cmd.exe command
    shell - Execute powershell.exe command
    exit - Exit the session
    screenshot - Take a screenshot
    persist <name> - Create a registry key to Run the file.exe
    getNC - Download Netcat
    useNC <ip> <port> - Use Netcat

## Usage
- Change Variable DISCORD_TOKEN and guild_id to your own
  
- Execute the code in python or compile the code to .exe in the target machine
  
- Get This in your server:
![image](https://github.com/qqqt/c2dc/assets/162643613/0a615931-8a63-495b-9e38-0ba40ec3ff27)
