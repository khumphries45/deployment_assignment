import base64, os


class SessionStore:

    def __init__(self):
        #It's just an empty dictionary so you can store ID's
        self.sessionStore = {}
        return

    def generateSessionId(self):
        randnum = os.urandom(32)
        rstr = base64.b64encode(randnum).decode("utf-8")
        #base 64 is string with 64 characters in it has numbers and characters
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessionStore[sessionId] = {}
        return sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessionStore:
            return self.sessionStore[sessionId]
        else:
            return None
