import discord
from classes.bully import random_failed
from classes.page import page_swich
from classes.database import SqliteConnect as dbconnect
from discord.ext import commands


class Emoji(commands.Cog, name="for emoji caculating"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.check(random_failed)
    async def emoji(self, ctx, types=None, option=None, page=None):
        """emoji satistic\n   emoji <type> <option> <pages>
        """
        if types is None:
            url = self.bot.get_user(323429669464571905).avatar_url
            em = discord.Embed(
                title=f'指令用法:',
                description='emoji <type> <option> <pages>',
                colour=discord.Colour.red()
            )
            em.set_footer(text=f'by ひがし#9901',
                          icon_url=f'{url}')
            em.add_field(name='type:', value='排名', inline=False)
            em.add_field(name='option:', value='升,降', inline=False)
            em.add_field(name='pages:', value='數字', inline=False)
            em.add_field(name='翻頁有效時間:', value='三分鐘', inline=False)
            await ctx.send(embed=em)

        elif types == "排名":
            guild_id = ctx.guild.id
            guild_emoji_id = [emoji.id for emoji in ctx.guild.emojis]

            not_use = []
            unrank = {}
            for emoji in guild_emoji_id:
                with dbconnect() as session:
                    res = session.execute(f"SELECT COUNT(*)\
                                            FROM `{guild_id}`\
                                            WHERE emoji_id = {emoji};")\
                                            .fetchone()[0]
                    if res == 0:
                        not_use.append(emoji)
                    else:
                        unrank[emoji] = res

            if option == "升":
                ranked = dict(sorted(unrank.items(), key=lambda kv: kv[1]))
                pages = []
                line = ''
                for i, k in enumerate(ranked):
                    emoji = self.bot.get_emoji(int(k))
                    line += f'{emoji} 使用了 {ranked[k]} 次\n'
                    if i % 10 == 0 and i != 0:
                        pages.append(line)
                        line = ''
                else:
                    pages.append(line)

                p_num = len(pages)
                embeds = []
                url = self.bot.get_user(323429669464571905).avatar_url

                for i, page in enumerate(pages):
                    embeds.append(discord.Embed(
                        title=f'使用次數少的表情',
                        description=f'{page}',
                        colour=discord.Colour.orange()
                    ).set_footer(
                        text=f'by ひがし#9901 | 第{i+1}/{p_num}頁',
                        icon_url=f'{url}'))
                await page_swich(self, ctx, embeds, 180)

            elif option == "降":
                ranked = dict(sorted(unrank.items(),
                                     key=lambda kv: kv[1],
                                     reverse=True))
                pages = []
                line = ''
                for i, k in enumerate(ranked):
                    emoji = self.bot.get_emoji(int(k))
                    line += f'{emoji} 使用了 {ranked[k]} 次\n'
                    if i % 10 == 0 and i != 0:
                        pages.append(line)
                        line = ''
                else:
                    pages.append(line)

                p_num = len(pages)
                embeds = []
                url = self.bot.get_user(323429669464571905).avatar_url

                for i, page in enumerate(pages):
                    embeds.append(discord.Embed(
                        title=f'使用次數多的表情',
                        description=f'{page}',
                        colour=discord.Colour.orange()
                    ).set_footer(
                        text=f'by ひがし#9901 | 第{i+1}/{p_num}頁',
                        icon_url=f'{url}'))
                await page_swich(self, ctx, embeds, 180)


def setup(bot):
    bot.add_cog(Emoji(bot))
