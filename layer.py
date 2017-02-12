# -*- coding: utf-8 -*-

# apenas adicionando um comentario para teste do controle de versao
import os, subprocess, time, subprocess

from yowsup.layers.interface import YowInterfaceLayer  # Reply to the message
from yowsup.layers.interface import ProtocolEntityCallback  # Reply to the message
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity  # Body message
from yowsup.layers.protocol_presence.protocolentities import AvailablePresenceProtocolEntity  # Online
from yowsup.layers.protocol_presence.protocolentities import UnavailablePresenceProtocolEntity  # Offline
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity  # Name presence
from yowsup.layers.protocol_chatstate.protocolentities import \
    OutgoingChatstateProtocolEntity  # is writing, writing pause
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.common.tools import Jid  # is writing, writing pause

# Log, but only creates the file and writes only if you kill by hand from the console (CTRL + C)
# import sys
# class Logger(object):
#    def __init__(self, filename="Default.log"):
#        self.terminal = sys.stdout
#        self.log = open(filename, "a")
#
#    def write(self, message):
#        self.terminal.write(message)
#        self.log.write(message)
# sys.stdout = Logger("/1.txt")
# print "Hello world !" # this is should be saved in yourlogfilename.txt
# ------------#------------#------------#------------#------------#------------

allowedPersons = ['555195592474', '555192576902', '555193918145']  # Filter the senders numbers
ap = set(allowedPersons)

name = "NAMEPRESENCE"
filelog = "/root/.yowsup/Not allowed.log"


############ Classes para escutar e enviar mensagens de texto e controlar status #############################

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.3)
            self.toLower(messageProtocolEntity.ack())  # Set received (double v)
            time.sleep(0.2)
            self.toLower(PresenceProtocolEntity(name=name))  # Set name Presence
            time.sleep(0.2)
            self.toLower(AvailablePresenceProtocolEntity())  # Set online
            time.sleep(0.3)
            self.toLower(messageProtocolEntity.ack(True))  # Set read (double v blue)
            time.sleep(0.4)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set is writing
            time.sleep(2)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set no is writing
            time.sleep(0.1)
            self.onTextMessage(messageProtocolEntity)  # Send the answer
            time.sleep(0.5)
            self.toLower(UnavailablePresenceProtocolEntity())  # Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        #  print entity.ack()
        self.toLower(entity.ack())

    # # invencao minha
    #     def image_send(self, number, path, caption=None):
    #         self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)

    def media_send(self, number, path, mediaType, caption=None):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path,
                                                                                         successEntity, originalEntity,
                                                                                         caption)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity,
                                                                                    originalEntity)
            self._sendIq(entity, successFn, errorFn)


    def onTextMessage(self, messageProtocolEntity):
        namemitt = messageProtocolEntity.getNotify()
        message = messageProtocolEntity.getBody().lower()
        recipient = messageProtocolEntity.getFrom()
        textmsg = TextMessageProtocolEntity

        if messageProtocolEntity.getFrom(False) in ap:
            if message.upper() == 'FALA PUTO':
                answer = "Puto é tu " + namemitt + " "
                self.toLower(textmsg(answer, to=recipient))
                self.toLower(textmsg(answer, to=recipient))
                print(recipient[2:12] + ":" + message)
                print(answer)

            elif message == 'temperature':
                t = subprocess.check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1]
                ts = t
                answer = 'My temperature is ' + ts + ' °C'
                self.toLower(textmsg(answer, to=recipient))
                print(recipient[2:12] + ":" + message)
                print(answer)

            elif message == 'filmes':
                lista_filmes_dir = os.listdir('/home/joao/filmes')
                for i in lista_filmes_dir:
                    answer = i
                    self.toLower(textmsg(answer, to=recipient))
                    time.sleep(0.5)
                time.sleep(2)
                self.toLower(textmsg("Escolhe um arrombado, escreve dir na frente faz favor", to=recipient))

            elif message[0:3] == 'dir':
                dir_filme = str('/home/joao/filmes/') + str(message[3:]) + str('/')
                lista_filmes_arq = os.listdir(dir_filme)
                for i in lista_filmes_arq:
                    answer = i
                    self.toLower(textmsg(answer, to=recipient))
                    time.sleep(1)
                self.toLower(textmsg("Agora escreve o nome do arquivo com mov na frente, anda logo", to=recipient))

            elif message[0:3] == 'mov':
                base_comando = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py'
                dir_filme = str('/home/joao/filmes/') + str(message[3:-4]) + str('/') + str(message[3:])
                dir_legenda = str('/home/joao/filmes/') + str(message[3:-4]) + str('/') + str(message[3:-4]) + ".vtt"
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py' + ' -subtitles ' + dir_legenda + ' ' + dir_filme
                time.sleep(4)
                self.toLower(textmsg("Mandei pro chromecast, agora reza pra funcionar", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'pause':
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py -pause'
                self.toLower(textmsg("Pausei, vai mijar", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'play':
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py -continue'
                self.toLower(textmsg("Dei o play", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'stop':
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py -stop'
                self.toLower(textmsg("Já era", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'aumenta':
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py -volup'
                self.toLower(textmsg("Já era", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'abaixa':
                comando_final = 'python /home/joao/Development/stream2chromecast/stream2chromecast.py -voldown'
                self.toLower(textmsg("Já era", to=recipient))
                subprocess.Popen(comando_final, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

            elif message == 'restart':
                answer = "Ah! " + namemitt + ", seu bobinho, achou que eu ia cair né."
                self.toLower(textmsg(answer, to=recipient))
                print(recipient[2:12] + ":" + message)
                print(answer)
                time.sleep(1)
                self.toLower(UnavailablePresenceProtocolEntity())
                time.sleep(1)
            #                os.system('reboot')

            elif message.upper() == 'MANDA NUDES':
                answer = "Ok " + namemitt + ", seu safadinho. La vai."
                self.toLower(textmsg(answer, to=recipient))
                # image_send(recipient,"/home")
                print(recipient[2:12] + ":" + message)
                print(answer)
                time.sleep(1)
                self.toLower(UnavailablePresenceProtocolEntity())
                time.sleep(1)

            else:
                answer = "Deculpe " + namemitt + ", Eu ainda não entendo essa palavra"
                self.toLower(textmsg(answer, to=recipient))
                print(recipient[2:12] + ":" + message)
                print(answer)

        else:
            answer = "Oi " + namemitt + ", Desculpe, não quero ser rude, mas você não está na lista de pessoas autorizadas desse numero"
            time.sleep(20)
            self.toLower(textmsg(answer, to=recipient))
            print(recipient + ":" + message)
            print(answer)
            out_file = open(filelog, "a")
            out_file.write(
                "------------------------" + "\n" + "Sender:" + "\n" + namemitt + "\n" + "Number sender:" + "\n" + recipient + "\n" + "Message text:" + "\n" + message + "\n" + "------------------------" + "\n" + "\n")
            out_file.close()
