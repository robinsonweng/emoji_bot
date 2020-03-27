import asyncio


async def page_swich(self, ctx, pages, timeout=60):
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
                                                     timeout=timeout,
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
                if i < len(pages)-1:
                    i += 1
                    await msg.edit(embed=pages[i])
