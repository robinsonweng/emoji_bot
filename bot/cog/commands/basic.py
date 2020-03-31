import discord
import asyncio
from discord.ext import commands
from classes.bully import random_failed
from classes.page import page_swich


class Basic(commands.Cog, name="basic commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(random_failed)
    async def ping(self, ctx):
        """目前網路品質
        """
        await ctx.send(f'延遲: {self.bot.latency*1000}ms')

    @commands.command()
    @commands.check(random_failed)
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

        await page_swich(self, ctx, pages)

    @commands.command()
    # @commands.check(random_failed)
    async def vote(self, ctx, topic, *option):
        """command for multi option vote
        """
        if len(option) >= 10:
            await ctx.send('超出投票種類上限!')

        des = ''
        for i, p in enumerate(option):
            des += f'{i+1}. {p}\n'

        voter = ctx.author.nick
        url = ctx.author.avatar_url
        em = discord.Embed(
            title=f'{topic}',
            description=f'{des}',
            colour=discord.Colour.green()
        )
        em.set_footer(
            text=f'by {voter} | 投票時間為90秒',
            icon_url=f'{url}'
        )

        msg = await ctx.send(embed=em)
        num_emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣',
                     '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        for i, emo in enumerate(option):
            await msg.add_reaction(num_emoji[i])

        def check(reaction, user):
            if not user.bot and reaction.emoji in num_emoji[:i+1]:
                return True

        amount = dict.fromkeys(num_emoji[:i+1])

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add',
                                                         timeout=2,
                                                         check=check)
            except asyncio.TimeoutError:
                desrip = ""
                for i, ((k, v), p) in enumerate(zip(amount.items(), option)):
                    if v is None:
                        v = 0
                    desrip += f'{i+1}. {p}: 共{v}票\n'

                    if ctx.author.nick:
                        voter = ctx.author.nick
                    else:
                        voter = ctx.author.name

                    url = ctx.author.avatar_url
                embed = discord.Embed(
                    title=f'{topic}: 投票結果',
                    description=f'{desrip}',
                    colour=discord.Colour.red()
                )
                embed.set_footer(
                    text=f'by {voter} | 投票結果',
                    icon_url=f'{url}'
                )
                await msg.edit(embed=embed)
                break
            else:
                amount[reaction.emoji] = reaction.count - 1


def setup(bot):
    bot.add_cog(Basic(bot))
