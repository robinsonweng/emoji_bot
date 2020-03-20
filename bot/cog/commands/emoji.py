from classes.bully import random_failed
from classes.database import SqliteConnect as dbconnect
from discord.ext import commands


class Emoji(commands.Cog, name="for emoji caculating"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(random_failed)
    async def emoji(self, ctx, types=None, option=None, number=0):
        """emoji satistic
        """
        if types is None:
            await ctx.send(f'用法: emoji <type> <option> <number>')
        elif types == "排名":
            guild_id = ctx.guild.id
            guild_emoji_id = [emoji.id for emoji in ctx.guild.emojis]

            not_use = []
            rank = {}
            for emoji in guild_emoji_id:
                with dbconnect() as session:
                    res = session.execute(f"SELECT COUNT(*)\
                                            FROM `452726035138740256`\
                                            WHERE emoji_id = '{emoji}';")
                    if res.fetchone() == 0:
                        not_use.append(emoji)
                    else:
                        rank[emoji] = res.fetchone()
            print(f'emoji not use {not_use}')
            if option == "升":
                pass
            elif option == "降":
                pass


def setup(bot):
    bot.add_cog(Emoji(bot))
