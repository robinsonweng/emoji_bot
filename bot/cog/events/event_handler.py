import re
from discord.ext import commands
from classes.database import SqliteConnect as db_connect


class EventHandler(commands.Cog, name="handling event"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return

        msg_emojis = re.findall(r'<:\w*:\d*>', msg.content)
        msg_emojis = set(e.split(':')[2].replace('>', '') for e in msg_emojis)
        guild_emo = [str(e.id) for e in msg.guild.emojis]

        guild_id = msg.guild.id
        user_id = msg.author.id

        if not msg_emojis:
            return

        for emo in msg_emojis:
            if emo not in guild_emo:
                print(f'emoji: {emo} not in guild')
            # add emoji by guild id
            with sqlite_conn() as session:
                session.execute(f'INSERT INTO `{guild_id}`(user_id, emoji_id)\
                                  VALUES ({user_id},{emo})')
            print(f"msg: {emo}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # logging level:
        if user.bot:
            return
        if reaction.emoji == '\u25c0' or reaction.emoji == '\u25b6':
            return

        guild_emoji = [e.id for e in user.guild.emojis]
        try:
            if reaction.emoji.id not in guild_emoji:
                print(
                    f'{reaction.emoji} not in guild {reaction.message.guild}'
                )
                return
        except AttributeError:
            return

        guild_id = user.guild.id
        user_id = user.id

        with db_connect() as session:
            session.execute(f'INSERT INTO `{guild_id}`(user_id, emoji_id)\
                                VALUES ({user_id}, {reaction.emoji.id})')
        print(f'reaction: {reaction.emoji}')

    @commands.Cog.listener()
    async def on_group_join(channel, user):
        with db_connect() as session:
            session.execute(f"CREATE TABLE IF NOT EXISTS `{channel.guild.id}` \
                                (user_id int,\
                                timestmp DATETIME DEFAULT\
                                (datetime('now','localtime')),\
                                emoji_id int)")


def setup(bot):
    bot.add_cog(EventHandler(bot))
