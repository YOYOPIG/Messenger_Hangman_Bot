from transitions import Machine

class TocMachine(object):

    states = ['idle', 'msg received', 'finding photo']
    def __init__(self, **machine_configs):
        self.machine = Machine(model=self, states=TocMachine.states, initial='idle')
        self.machine.add_transition(trigger='recvmsg', source='idle', dest='msg received', after='enter_state1')

    def enter_state1(self):
        print("In state text received")

    def find_photo(self):
        print("Finding toxic photos hehexd")
    
    def recvmsg(self):
        print("msg recved")


fsm = TocMachine()
fsm.recvmsg()
print(fsm.machine.state)

print("End success")
input()