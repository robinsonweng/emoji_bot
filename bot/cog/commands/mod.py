from discord.ext import commands
import asyncio


class Mod(commands.Cog, name="moderator or owner commands"):
    """Owner commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            raise commands.errors.NotOwner('You do not own this bot.')
        return True

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown the bot."""
        await ctx.send("Shutting down...")
        await asyncio.sleep(1)
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Mod(bot))
