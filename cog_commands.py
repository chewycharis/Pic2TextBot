from discord.ext import commands
import discord 
import time 
from datetime import datetime
from pic2text import pic2text
from pic2text import randomQuote
import asyncio


class cog_commands(commands.Cog):
    
    def __init__(self,bot:commands.Bot):
        self.bot=bot
        self.last_msg=None
        self.channels={"testingInPeace":886391513469288492 , "Pic2Text":884494740748402710}
        self.current_channel=self.channels["testingInPeace"]

    @commands.command(name="hello")
    async def hello_world(self, ctx:commands.Context):
        await ctx.send("Hello World!")
        
    @commands.command(name="interpret")
    async def convertMessage (self,ctx:commands.Context,msgID:int=None):
        if msgID:
            ctx.message = await ctx.fetch_message(msgID)

        url=await self.hasImage(ctx.message)
        if not url:
            await ctx.send("There is no picture to interpret!")
        else:
            out1=pic2text(url)
            await ctx.send("This is the converted output using tesseract...\n")
            await ctx.send(out1)
    
    @commands.command(name="interpret2")
    async def convertMessage2 (self,ctx:commands.Context,msgID:int=None):
        if msgID:
            ctx.message = await ctx.fetch_message(msgID)

        url=await self.hasImage(ctx.message)
        if not url:
            await ctx.send("There is no picture to interpret!")
        else:
            out1=pic2text(url,filter=True)
            await ctx.send("This is the converted output filtering for black and white text using tesseract...\n")
            await ctx.send(out1)

    @commands.Cog.listener("on_message")
    async def hasImage(self, message:discord.Message):
        channel=message.channel
        attachments=message.attachments
        picFormats=["png","jpg","jpeg"]
        if attachments!=[]:
            url=attachments[0].url
            if any([picFormat in url[-4:].lower() for picFormat in picFormats]): 
                return url
        return None
    
    @commands.command(name="quote")
    async def goodreadsQuotes(self, ctx:commands.Context,*args):
        if len(args)!=0:
            for i in args[1:]:
                s+=i+" "
            out=randomQuote(s)
        else:
            out=randomQuote("happiness")
        await ctx.send(out)
    
    @commands.Cog.listener("on_message")
    async def giveup(self, message:discord.Message):
        channel=message.channel
        isBot=message.author.bot
        if "give up" in message.content.lower() and not isBot:
            await channel.send("Never give up! You can do this!")

    @commands.Cog.listener("on_message")
    async def hug(self, message:discord.Message):
        channel=message.channel
        olduser=message.author            

        if "hug me" in message.content.lower():
            await channel.send("Would you like a hug?")
            try:
                reaction = await self.bot.wait_for('message',timeout=30.0,check=lambda message: message.author == olduser)
                if reaction.content.lower().startswith("y"):
                    await channel.send('Sending hugs your way... \n')
                    await channel.send("https://tenor.com/view/mochi-peachcat-mochi-peachcat-hug-pat-gif-19092449")
                elif reaction.content.lower().startswith("n"):
                    await channel.send('No hugs for you then.')
                else:
                    await channel.send("I don't get what you mean")

            except asyncio.TimeoutError:
                await channel.send("Sending you a hug anyway")
                await channel.send("https://tenor.com/view/mochi-peachcat-mochi-peachcat-hug-pat-gif-19092449")


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        channel = self.bot.get_channel(self.current_channel)
        if not channel:
            return
        await channel.send(f"Welcome, {member.mention}!")


    @commands.command(name="allcommands")
    async def allcommands(self,ctx:commands.Context):
        channel = self.bot.get_channel(self.current_channel)
        if not channel:
            return
        embed = discord.Embed(title="Pic2Text", description="I am trying to be a helpful bot :)", colour=0x87CEEB, timestamp=datetime.utcnow())
        embed.set_author(name="chewycharis", icon_url="https://i.pinimg.com/564x/26/b4/dd/26b4dd78bcf38d7cb826c2df970842be.jpg")

        commands_descript="""
        (trigger by !command_name)\n
        !hello: prints hello \n
        !interpret: converts screenshot of text messages to text; must send a photo attachment before triggering command \n
        !interpret2: similar to !interpret with filter for black and white text; must send a photo attachment before triggering command \n
        !quote: gets a random quote from goodreads based on keyword; default keyword is happiness \n
        !allcommands: prints an embed message with descriptions of all commands used by bot
        """

        hidden_commands_descript="""
        (trigger by keyword mention) \n
        hug me: gives a hug \n
        give up: returns some chicken-soupish message\n
        """
        embed.add_field(name="!Commands", value=commands_descript, inline=False)
        embed.add_field(name="Hidden Commands", value=hidden_commands_descript, inline=False)
        await channel.send(embed=embed)



def setup (bot:commands.Bot):
    bot.add_cog(cog_commands(bot))