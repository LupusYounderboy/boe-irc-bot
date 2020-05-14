#!/usr/bin/python3
import  miniirc, sys, re, random, json

IP = ''
PORT = 6697
PREFIX = '!'
NICK = "Boe"
PASSWORD = ""
CHANNELS = ["#italy"]

MAX_LENGHT=50
USERNAME_PLACEHOLDER="#username#"
CHANNEL_PLACEHOLDER="#channel#"
AFTER_PLACEHOLDER="#after#"
BOT_PLACEHOLDER="#bot#"
JSON_FILE='boe.json'

irc = miniirc.IRC(IP, PORT, NICK, CHANNELS, ident=NICK, realname=NICK,ns_identity="{} {}".format(NICK,PASSWORD),auto_connect=True,ssl=True, verify_ssl=False, debug=False, persist=True, ping_interval=20,quit_message="Bye")

with open(JSON_FILE) as json_file:
    command_db = json.load(json_file)

@irc.Handler('NOTICE', colon=False)
def notice(irc, hostmask, args):
	username = hostmask[0]
	if 'NickServ' in username and "identify via" in args[1]:
		irc.quote("PRIVMSG","NICKSERV :RELEASE",NICK,PASSWORD)
		irc.quote("NICK",NICK)
		irc.quote("PRIVMSG","NICKSERV :IDENTIFY",PASSWORD)

@irc.Handler('PRIVMSG', colon=False)
def handler(irc, hostmask, args):
    username = hostmask[0]
    channel  = args[0]
    text     = args[1].split(' ')
    command  = text.pop(0)
    if not command.startswith(PREFIX):
        return
    command = command[len(PREFIX):]
    after_command = text

    if command in command_db and channel in CHANNELS and len("".join(text)) < MAX_LENGHT:
        command_value = command_db.get(command)

        if isinstance(command_value, list):
            command_value = random.choice(command_value)

        command_value = command_value.replace(USERNAME_PLACEHOLDER,username)
        command_value = command_value.replace(CHANNEL_PLACEHOLDER,channel)
        command_value = command_value.replace(BOT_PLACEHOLDER,NICK)

        if AFTER_PLACEHOLDER in command_value:
            if len(after_command) == 0:
                return
            if len(after_command) == 2:
                command_value = command_value.replace(AFTER_PLACEHOLDER," and ".join(after_command))
            else:
                command_value = command_value.replace(AFTER_PLACEHOLDER,", ".join(after_command))

        if '\n' in command_value:
            lines = command_value.split('\n')
            for line in lines:
                irc.msg(channel, line)
        else:
            irc.msg(channel, command_value)

if __name__ == '__main__':
	irc.connect()

