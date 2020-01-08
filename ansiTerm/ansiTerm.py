from .ansiCommander import AnsiCommander as Ansi
import re
import os

class AnsiTerm:
    pattern = re.compile(r'\<!(\s*[a-zA-Z0-9]+|\/)\s*\>')

    def __init__(self):
        self.useColor = True
        self.undo_stack = []
        self.states = Ansi.getDefaultStates()
        self.styles = {}

    def setStyle(self, name, states):
        self.styles[name] = states


    def pushState(self, states):
        """ Returns the escape string which activates the state change.
        states is a list of 2-tuples, each specifying like ('fg-color',
        'light-red'). Each attribute is added to a changelist, which is then
        applied and pushed to the stack. Repeated attribute names override.
        """
        if self.useColor == False:
            return ""

        if type(states) is str:
            appliedStates = self.styles[states]
        else:
            appliedStates = states

        changelist, undolist = Ansi.makeSetAndUndoCommands(self.states, appliedStates)
        Ansi.applyChangesToStateSet(self.states, changelist)
        self.undo_stack.append(undolist)
        return Ansi.makeCommandFromStates(changelist)

    def pushResetStates(self, states):
        """ Returns the escape string which resets the terminal state and then applies an optional state set.
        states is a list of 2-tuples, each specifying like ('fg-color',
        'dark-yellow'). This effectively resets all colors and attributes,
        and then applies the profile elements as in push_states().
        """
        if states is string:
            states = self.styles[states]

        return pushStates(ColorTerminal.getDefaultStates() + states)

    def popStates(self, num_states = 1):
        """
        This reverts state to how it was before the corresponding push.
        Returns the escape string which activates the state change.
        """
        if self.useColor == False:
            return ""

        assert len(self.undo_stack) >= num_states

        changes = []
        for i in range(0, num_states):
            pop = self.undo_stack.pop()
            Ansi.applyChangesToStateSet(self.states, pop)
            change = Ansi.makeCommandFromStates(pop)
            if change:
                changes.append(change)

        if len(self.undo_stack) == 0:
            changes.append(Ansi.all_off)

        if len(changes) > 0:
            return ''.join(changes)
        else:
            return ''

    
    def getStates(self, string):
        # Parse the tag to get state data from it.
        # We currently only support style names.
        if string == '/':
            return self.popStates()
        else:
            return self.pushState(string)


    def print(self, string):    # TODO: duck the system print function
        built = ''
        matches = [m for m in AnsiTerm.pattern.finditer(string)]
        if len(matches) > 0:
            lastEnd = 0
            for idx, match in enumerate(matches):
                states = match.group().strip()[2:-1]
                if states == '/':
                    built = ''.join([
                        built,
                        string[lastEnd:match.start()],
                        self.popStates()])
                else:
                    built = ''.join([
                        built,
                        string[lastEnd:match.start()],
                        self.pushState(states)])
                lastEnd = match.end()
            built = ''.join([built, string[lastEnd:]])
        else:
            built = string

        print (built)
    
    def makePath(self, path):
        d, p = os.path.split(path)
        if d != "" and not d.endswith(os.sep):
            d = ''.join([d, os.sep])
        return f'<!pathDir>{d}<!/><!pathBasename>{p}<!/>'

ansiTerm = AnsiTerm()
