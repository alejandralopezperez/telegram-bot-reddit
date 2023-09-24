# Introduction 

This project is based on the contents of `Practical Docker with Python` book chapter 3 and its [repository](https://github.com/Apress/practical-docker-with-python/tree/master/source-code).

The Python app is a simple application with a bot interface using Telegram Messenger to fetch the last 5 stories from Reddit. 

# Setting Up Telegram Messenger

A Telegram Messenger account is needed. To sign up, [download the application](https://telegram.org) for the platform of choice and install it.

## Creation of a new bot

Telegram uses a bot called BotFather as its interface for creating new bots and updating them. To get started with BotFather, in the search panel type _BotFather_. From the chat window, type `/start`. This will trigger BotFather to provide an introductory set of messages.

To use BotFather to generate a new bot, start by typing `/newbot` in Telegram Messenger, which will trigger a series of questions to answer. Due to Telegram's restrictions, the username for a bot must always end with _bot_. Along with the link to the documentation, Telegram will issue a token, which is used to identify and authorize bots. This API token must be placed as an environment variable in the .env file, defined as **NBT_ACCESS_TOKEN** in the `.env.template` file.

## Test the endpoint

Telegram Bot API provides a `/getMe` endpoint for testing the auth token. To request to Telegram API with a valid token use: 

    https://api.telegram.org/bot<NBT_ACCESS_TOKEN>/getMe

where <NBT_ACCESS_TOKEN> is the API token obtained in the previous step. In the response, Telegram identifies and authorizes the bot, which confirms that the bot token is proper.


# Newsbot app

## Create environment

To create the environment for this project using [Conda](https://docs.conda.io/en/latest/), clone the project repository,

    git clone https://mmartinprojects@dev.azure.com/mmartinprojects/learning_path/_git/learning_path
  
and navigate to the project directory

    cd learning_path
  
to create the environment from the environment.yml file, which will also install the additional Python packages specified in the requirements.txt file:

    conda env create -f environment.yml
  
This will create a new Conda environment with the necessary dependencies specified in the environment.yml file. To activate the environment run

    conda activate learning-path
    
Now, the environment is set up and ready to use for this project.

## Create the .env file

To create the `.env` file of the project, locate the `.env.template` file in the root directory of the project and rename the file to `.env`. This is the file that will hold the environment-specific variables. Add the API token as the NBT_ACCESS_TOKEN environment variable

    NBT_ACCESS_TOKEN=<NBT_ACCESS_TOKEN>

and save the .env file.

## Running newsbot

To run the newsbot, start the python script with the command:

    python newsbot/main.py

In the Telegram Messenger window of the bot, type a `/start` command, set a source subreddit with the `/source` command (e.g., `/source python`) and tell the bot to fetch some news with `/fetch`.
