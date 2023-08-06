# This file is placed in the Public Domain.


'command'


import time


from ..command import Command


def __dir__():
    return (
            'cmd',
           )


starttime = time.time()


def cmd(event):
    event.reply(','.join(sorted(Command.cmds)))
