#!/usr/bin/env python3
import datetime
import logging
import os
import sys
import configurator

sys.path.insert(1, (os.path.dirname(os.path.dirname(__file__))))

import discord
from discord import app_commands
from discord.ext import commands

from functools import reduce
from src import tkfinder, util
from src.resources import embed, const
from github import Github

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927, continued by Tib#1303'

# Set logger to log errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

logfile_directory = os.path.abspath(os.path.join(base_path, "..", "log"))
logfile_path = logfile_directory + "\\logfile.log"

# Create logfile if not exists
if not os.path.exists(logfile_directory):
    os.makedirs(logfile_directory)

if not os.path.isfile(logfile_path):
    open(logfile_path, "w")

file_handler = logging.FileHandler(logfile_path)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

discord_token = config.read_config()['DISCORD_TOKEN']
feedback_channel_id = config.read_config()['FEEDBACK_CHANNEL_ID']
github_token = config.read_config()['GITHUB_TOKEN']
gh = Github(login_or_token=github_token)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced=False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced=True
        print("Bot connected")

client=aclient()
tree = app_commands.CommandTree(client)

@tree.command(name="test",description="testing")
async def self(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Hello {name}. Done")

client.run(discord_token)
