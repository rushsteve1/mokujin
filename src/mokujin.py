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

@tree.command(name="data",description="Get frame data from a move of a character")
async def self(interaction: discord.Interaction, character: str, move: str):

    character_name = tkfinder.correct_character_name(character)

    if character_name is not None:
        character = tkfinder.get_character_detail(character_name)
        move_type = util.get_move_type(move.lower())

        if move_type:
            result = util.display_moves_by_type(character, move_type)
        else:
            result = util.display_moves_by_input(character, move)

    else:
        result = {"embed": embed.error_embed(f'Character {character} does not exist.')}

    await interaction.response.send_message(embed=result["embed"],ephemeral=True)

@tree.command(name="feedback",description="Send feedback incase of wrong data")
async def self(interaction: discord.Interaction, message: str):

    today = datetime.datetime.strptime(datetime.datetime.now().isoformat(),"%Y-%m-%dT%H:%M:%S.%f")
    age = today - interaction.user.created_at.replace(tzinfo=None)
    print (age.days)
    if age.days < 120:
        return
    else:
        try:
            feedback_message = "{} ;{} ;{} ;{}\n".format(str(interaction.user.name), interaction.user.id, interaction.guild, message)
            channel = client.get_channel(feedback_channel_id)
            await channel.send(feedback_message)
            result = {"embed": embed.success_embed("Feedback sent")}
        except Exception as e:
            result = {"embed": embed.error_embed("Feedback couldn't be sent caused by: " + e)}

        await interaction.response.send_message(embed=result["embed"],ephemeral=True)

client.run(discord_token)
