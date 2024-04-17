import discord
from discord.ext import commands
import asyncio
import random

import config_selfbot
import fr_en

def random_cooldown(minimum, maximum):
    cooldown = random.randint(minimum*100000,maximum*100000) / 100000
    return cooldown

class UtilsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.id == self.bot.user.id:
            try:
                attachments_urls = [attachment.url for attachment in message.attachments]
                self.sniped_messages[message.channel.id] = {
                    'author': message.author,
                    'content': message.content,
                    'images': attachments_urls if message.attachments else fr_en.empty[config_selfbot.lang]
                }
            except Exception:
                return

    @commands.command()
    async def clear(self, ctx):
        message_split = ctx.message.content.split()
        try:
            str_amount = message_split[1]
        except Exception:
            str_amount = "20"

        try:
            amount = int(str_amount) + 1
        except Exception:
            await ctx.message.edit(fr_en.spam_invalid[config_selfbot.lang])
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()
            return
        
        if ctx.guild is None:
            async for message in ctx.channel.history(limit=amount):
                if message.author.id == self.bot.user.id:
                    await message.delete()
                    await asyncio.sleep(random_cooldown(0.4, 1.9))
        else:
            def is_me(m):
                return m.author.id == self.bot.user.id
            await ctx.channel.pruge(limit=amount, check=is_me, oldest_first=True)

        await ctx.channel.send(f"> 🌌 **{config_selfbot.selfbot_name}**", delete_after=1.4)

    @commands.command()
    async def snipe(self, ctx):
        sniped_message = self.sniped_messages.get(ctx.channel.id)
        if sniped_message:
            images_text = ", ".join(sniped_message['images']) if not sniped_message['images'] == fr_en.empty[config_selfbot.lang] else None
            await ctx.message.edit(f"""__**🔫 Sniper:**__

🗣️ {fr_en.author[config_selfbot.lang]}: {sniped_message['author']}
📩 Message: {sniped_message['content']}
🖼️ Images: {images_text}""")
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()
        else:
            await ctx.message.edit(fr_en.error_no_message_snipe[config_selfbot.lang])
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()

    @commands.command()
    async def hype(self, ctx):
        house = ctx.message.content.split()[1]
        if house == "balance":
            await self.bot.user.edit(house=discord.HypeSquadHouse.balance)
            await ctx.message.edit(f"🪄 HypeSquad {fr_en.hype_command[config_selfbot.lang]} ``{house}``")
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()
        elif house == "bravery":
            await self.bot.user.edit(house=discord.HypeSquadHouse.bravery)
            await ctx.message.edit(f"🪄 HypeSquad {fr_en.hype_command[config_selfbot.lang]} ``{house}``")
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()
        elif house == "brilliance":
            await self.bot.user.edit(house=discord.HypeSquadHouse.brilliance)
            await ctx.message.edit(f"🪄 HypeSquad {fr_en.hype_command[config_selfbot.lang]} ``{house}``")
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()
        else:
            await ctx.message.edit(fr_en.hype_fail[config_selfbot.lang])
            await asyncio.sleep(config_selfbot.deltime)
            await ctx.message.delete()

    @commands.command()
    async def ping(self, ctx):
        await ctx.message.edit(f"🏓 Pong ! (Ping: **{round(self.bot.latency * 1000)}ms**)")
        await asyncio.sleep(config_selfbot.deltime)
        await ctx.message.delete()

    @commands.command()
    async def bio(self, ctx):
        message_split = ctx.message.content.split()
        new_bio = ctx.message.content.replace(f"{message_split[0]} ", "")
        await self.bot.user.edit(bio=new_bio)
        await ctx.message.edit(f"📖 Bio {fr_en.bio_command[config_selfbot.lang]} \"`{new_bio}`\"")
        await asyncio.sleep(config_selfbot.deltime)
        await ctx.message.delete()