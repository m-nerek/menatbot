from threading import Timer

def resultChecker(message):
    '''
    Checks the reaction amount for yesses and nos to a poll
    '''
    nays = get(message.reactions, ":x:") ### gets nos list
    yays = get(message.reactions, ":white_check_mark") ### gets yesses list
    if yays.count > nays.count: ### compares and returns
        return f'yays win by {yays.count - nays.count} votes'
    elif yays.count > nays.count:
        return f'nays win by {nays.count - yays.count} votes'
    else:
        return "no result"

async def newPoll(message):
    '''
    Checks for a new poll message, makes it a proper poll according to server rulings (thanks benis) and calls resultChecker to return a result
    of the poll in a days time'''
    if message.channel.contains("polls"): ###checks only for messages in polls
        await message.add_reaction(":x:") ### adds 2 reactions no and yes in that order
        await message.add_reaction(":white_check_mark:")
        t = Timer(86400, resultChecker(message)) ###starts the 24 hour timer threaded to not hold up rest of bot.
        return t.start()
