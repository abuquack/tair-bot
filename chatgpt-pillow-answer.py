import discord
from discord.ext import commands
from PIL import Image

bot = commands.Bot(command_prefix="!")

@bot.command()
async def send_image(ctx):
    # Open and save the image using Pillow
    img = Image.open("example.png")
    img.save("temp_image.png")

    # Send the image to Discord
    await ctx.send(file=discord.File("temp_image.png"))

bot.run("YOUR_BOT_TOKEN")
