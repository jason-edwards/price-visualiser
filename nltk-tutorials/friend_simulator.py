from bs4 import BeautifulSoup
import bs4
from datetime import datetime
from whatever import shit_talk
import argparse

# Create a text file containing raw message texts. Newlines are created for each message but each message may have their own newlines.
def friend_threads(friendname, fbmessagesrawhtml, afterdate=None):
    print("Making soup.")
    soup = BeautifulSoup(fbmessagesrawhtml, "lxml")

    print("Searching for relevant threads.")
    filteredthreads = []
    threadtags = soup.find_all("div", {"class":"thread"})
    for t in threadtags:
        threadparticipants = t.contents[0]
        if friendname in threadparticipants:
            filteredthreads.append(t)
    print("Found %d threads" % len(filteredthreads))

    print("Finding messages.")
    earliestmessage = datetime.now()
    earliestmessagecontents = ''
    matchingmessages = []
    updateearliestmessage = False
    for t in filteredthreads:
        print("Messages: %d" % len(matchingmessages))
        messageheaders = t.find_all("div", {"class":"message"})

        for h in messageheaders:
            usertag = h.find("span", {"class":"user"})
            if usertag.contents[0] and usertag.contents[0] != friendname:
                continue
            
            datetag = h.find("span", {"class":"meta"})
            messagedate = datetime.strptime(datetag.contents[0], "%A, %B %d, %Y at %I:%M%p UTC+10")
            if messagedate < earliestmessage:
                earliestmessage = messagedate
                updateearliestmessage = True
            if afterdate and afterdate > messagedate:
                continue

            message = h.find_next('p')
            if message and message.name == 'p' and len(message.contents) > 0:
                matchingmessages.append(message.contents[0])
                if updateearliestmessage:
                    earliestmessagecontents = message.contents[0]
                    updateearliestmessage = False

    print("Found %d messages in total." % len(matchingmessages))
    print("Earliest message sent on %s: '%s'" % (str(earliestmessage), str(earliestmessagecontents)))
    
    if len(matchingmessages) > 0:
        print("Writing messages to file.")
        with open("Shit %s Says.txt" % friendname, 'w', encoding='utf8') as f:
            for s in matchingmessages:
                f.write(str(s))
                f.write('\n')
    else:
        print("No messages found for %s" % friendname)


# Run stuff
argparser = argparse.ArgumentParser()
argparser.add_argument("friend", type=str, help="Person's first name and last name with the first letter of each name capitalised.")
argparser.add_argument("-s", "--seed", type=str, help="Seed word.")
argparser.add_argument("-g", "--gen", action="store_true", help="Generate corpus data.")
argparser.add_argument("-m", "--mute", action="store_true", help="Don't shit talk.")
argparser.add_argument("-r", "--randomness", type=int, help="How random each word selection should be. 1 means use top word.")
argparser.add_argument("-l", "--length", type=int, help="Length of shit talking.")
args = argparser.parse_args()

friendname = args.friend
seedword = args.seed
filepath = "messages.htm"

fbmessagesrawhtml = ""
with open(filepath, encoding='utf8') as f:
    fbmessagesrawhtml = f.read()

startofthisyear = datetime(2016, 1, 1, 0)

randomness = args.randomness if args.randomness else 5
outputlength = args.length if args.length else 50

if args.gen:
    friend_threads(friendname, fbmessagesrawhtml)
if args.seed:
    shit_talk(friendname, seedword, randomness, outputlength)