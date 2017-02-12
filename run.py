from yowsup.common                             import YowConstants
from yowsup.env                                import YowsupEnv
from yowsup.layers                             import YowLayerEvent
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.stacks                             import YowStackBuilder

from james.layer import EchoLayer

#Uncomment to log
#import logging
#logging.basicConfig(level=logging.DEBUG)

CREDENTIALS = ("555189335583", "cvXzxFn6600SvIBW4bsDsH+lOAk=") #replace with your phone and password

if __name__==  "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)       #setting credentials
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))          #sending the connect signal
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])           #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())  #info about us as WhatsApp client

    stack.loop( timeout = 0.3, discrete = 0.3 )                                       #this is the program mainloop
