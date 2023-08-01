# Guide on Setting Up the Discord Bot

## Overview

1. Head over to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Go to the Bot tab and create a new bot.
3. Copy the bot token and paste it in the .env file.
4. Scroll down and enable all intents(members, messages, etc).
5. Make the bot private(Recommended but not required).
6. Head over to the `URL Generator` tab under OAuth2  and select the bot scope and generate an invite link.
7. Paste the invite link in your browser and invite the bot to your server.

## Step 1: Create a Discord Application

Head over to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application. Give it a name and click on the `Create` button.

## Step 2: Create a Discord Bot

Head over to the bot tab and click on the `Add Bot` button. Give it a name and click on the `Create` button. Copy the bot token and paste it in the .env file. Also recommend storing this key somewhere safe. As the portal will tell you, you can't get it back if you lose it.

## Step 3: Enable Intents

Scroll down and enable all intents(members, messages, etc). This will allow the bot to access the server members and messages. Enabling the `Message Content` intent is required for the bot to work. Be sure to save your changes.

## Step 4: Make the Bot Private

Optional but recommended. You wouldn't want someone else to use your bot without your permission, right? So, make it private.

## Step 5: Invite the Bot to Your Server

Head over to the `URL Generator` tab under OAuth2  and select the bot scope and generate an invite link. Paste the invite link in your browser and invite the bot to your server.

## Step 6: Get a channel ID

Enable the developer mode in Discord, right-click the channel, and get the channel ID. Paste the channel ID in the .env file, under `BOT_HOME_CHANNEL``

You have successfully created a Discord bot and invited it to your server. Be sure to complete the remaining stepup steps in the README.md file.
