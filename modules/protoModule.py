from comm.asyncClient import AsyncClient

class ProtoModule:
    def __init__(self, loop, addr, port, subscriptions):
        self.loop = loop
        self.client = AsyncClient(addr, port, self.msg_received, subscriptions, loop)
        self.loop.call_soon(self.tick)

    def tick(self):
        raise NotImplementedError()

    def msg_received(self, msg, msg_type):
        raise NotImplementedError()

    def subscribe(self, msg_types):
        self.client.subscribe(msg_types)

    def write(self, msg, msg_type):
        self.client.write(msg, msg_type)
    
    def run(self):
        try:
            with self.client:
                self.loop.run_forever()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        self.loop.stop()
