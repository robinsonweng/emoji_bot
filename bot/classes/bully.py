import random


async def random_failed(ctx):
    """using command.check to fail the command randomly
    """
    # purple eye 213539811900784640
    # me 323429669464571905
    if ctx.author.id == 323429669464571905:
        rand = random.randint(0, 9)
        if rand >= 2:
            return True
        else:
            await ctx.send('?')
            return False
    else:
        return True
