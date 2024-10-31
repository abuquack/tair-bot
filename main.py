# اللي وده يدخل يطور معنا حياه
# ينزل إضافة LiveShare على الـ VSCode ويتفضل معنا

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import os

import discord
import PIL
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests

# Image processing libraries
# cv2
# PIL


@app_commands.command()
async def hellowrld(interaction):
    await interaction.response.send_message("خلصنا برمجة اليوم احضر معنا جلسة ثانية")


class TairClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content == "ترحيب":
            await message.reply("تتم معالجة الصورة")
            avatar_background_image = Image.open("avatar-background.jpg")
            avatar_background_image = avatar_background_image.convert("RGB")
            ##معالجة للصورة
            ## إضافة صورة الافتار في المنتصف على شكل دائرة
            ## للصورة أعلاه
            
            #user avatar
            avatar_url = message.author.avatar.url
            avatar_response = requests.get(avatar_url)
            avatar_image = Image.open(io.BytesIO(avatar_response.content)).convert("RGB")

            # Circle
            mask = Image.new("L", avatar_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + avatar_image.size, fill=255)

            # apply the mask to the image
            circular_avatar = ImageOps.fit(avatar_image, mask.size, centering=(0.5, 0.5))
            circular_avatar.putalpha(mask)

            # Resize Avatar
            avatar_size = (150, 150) 
            circular_avatar = circular_avatar.resize(avatar_size, Image.LANCZOS)

            # position of the avatar
            background_size = avatar_background_image.size
            position = ((background_size[0] - avatar_size[0]) // 2, (background_size[1] - avatar_size[1]) // 2)

            avatar_background_image.paste(circular_avatar, position, circular_avatar)
            ##
            buf = io.BytesIO()
            avatar_background_image.save(buf, format='PNG')

            buf.seek(0)

            dfile = discord.File(buf, 'tarheeb.jpg')
            # المشكلة كانت في عدم تحويل الصورة
            # إلى discord.File
            # بعد التحويل جرى الإرسال بنجاح
            await message.reply("", file=dfile)

            return

        # # will try to generate here
        # image = image.new("RGB", (500, 200), (255, 255, 255)) #white background
        # draw = ImageDraw.Draw(image)
        # # add text to the image:
        # font = ImageFont.truetype("ariel.ttf, 30") #font size
        
        if message.author == self.user:
            return
        if message.content == "مرحبا":
            await message.reply("مراحب")
            return
        # Take it here 
        # join the voice channel
        if message.content == "ادخل الصوتية":
            if message.guild.voice_client:
                await message.reply("معلش مشغول")
                return
            if not message.author.voice:
                await message.reply("خش الصوتية أول")
                return
            # DOCS regarding VoiceChannel.connect
            # https://discordpy.readthedocs.io/en/stable/api.html?highlight=voicechannel%20connect#discord.VoiceChannel.connect
            voice_protocol = await message.author.voice.channel.connect()
            
        #Leave the voice channel
        if message.content == "خروج":
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                await message.channel.send("خرج من الاجتماع!")
                return
            await message.channel.send("لست بالاجتماع")

intents = discord.Intents.default()
intents.message_content = True
# ✅ Reply to messages saying "مرحبا"

# ✅ Add slash commands

# ✅ Welcome newcomers

# ✅ Send images

# ✅ Send custom-designed images

client = TairClient(intents=intents)



client.run(os.getenv("DISCORD_BOT_TOKEN"))