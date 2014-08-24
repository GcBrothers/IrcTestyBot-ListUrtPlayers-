# -*- coding: cp1252 -*-
import irclib
import ircbot
import socket
import string
import time

class myIRCBot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.quakenet.org", 6667)],
                                           "testyBot", "Test pour Bot IRC")
    def on_welcome(self, serv, ev):
        serv.join("#LcD")
        serv.privmsg("#LcD", "TestyBot is now enabled o/")
        #serv.kick("#LcD", "alphaPlayer", "Les insultes ne sont pas autorisées ici !")
        #serv.privmsg(self, "@alphaPlayer", "test")
    def on_pubmsg(self, serv, ev):
        canal = ev.target()
        message = ev.arguments()[0].lower()
        author = irclib.nm_to_n(ev.source())
        if "salut" in message:
            serv.privmsg("#LcD", "Hey ! How are you ?")
        if "noob" in message:
            serv.kick("#LcD", author, "Noob Yourself.")
        elif message[0] == "!":
            serv.privmsg("#LcD", "Commande détectée")
            if message == "!players":
                serv.privmsg("#LcD", "En cours de construction")
                connexionServeur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                #connexionServeur.bind(('tdm.tagazok-urt.fr', 27960))
                print "Sending Data"
                connexionServeur.sendto("\xFF\xFF\xFF\xFF\x02getstatus\x0a\x00", ('tdm.tagazok-urt.fr', 27960))
                data, addr = connexionServeur.recvfrom(10240)
                #print data
                datas = string.split(data, "\\", 116)
                clientsToPurge = datas[116]
                datas = string.split(clientsToPurge, "\n")

                i = 1
                while datas[i]:
                    client = string.split(datas[i], " ")
                    serv.privmsg("#LcD", "%s a %s kills (%s de ping)"%(client[2], client[0], client[1]))
                    i = i + 1
                    time.sleep(0.7)
                connexionServeur.close()
                serv.privmsg("#LcD", "Done.")
        
if __name__ == "__main__":
    print 'Working'
    myIRCBot().start()
