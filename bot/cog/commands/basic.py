import discord
import asyncio
from discord.ext import commands


class Basic(commands.Cog, name="basic commands"):
    def __init__(self, bot):
        self.bot = bot

    async def page_swich(self, ctx, pages):
        msg = await ctx.send(embed=pages[0])

        await msg.add_reaction('\u25c0')
        await msg.add_reaction('\u25b6')

        def check(reaction, user):
            if not user.bot:
                return True

        i = 0
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add',
                                                         timeout=60,
                                                         check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                break
            else:
                if reaction.emoji == '\u25c0':
                    if i > 0:
                        i -= 1
                        await msg.edit(embed=pages[i])
                if reaction.emoji == '\u25b6':
                    if i < 2:
                        i += 1
                        await msg.edit(embed=pages[i])

    @commands.command()
    async def ping(self, ctx):
        """目前網路品質
        """
        await ctx.send(f'延遲: {self.bot.latency*1000}ms')

    @commands.command()
    async def embed(self, ctx):
        """翻頁訊息測試
        """
        page1 = discord.Embed(
            title='Page 1/3',
            description='Description',
            colour=discord.Colour.orange()
        )
        page2 = discord.Embed(
            title='Page 2/3',
            description='Description',
            colour=discord.Colour.orange()
        )
        page3 = discord.Embed(
            title='Page 3/3',
            description='Description',
            colour=discord.Colour.orange()
        )

        pages = [page1, page2, page3]

        await self.page_swich(ctx, pages)


def setup(bot):
    bot.add_cog(Basic(bot))
