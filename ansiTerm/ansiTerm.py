from ansiCommander import AnsiCommander as Ansi

class AnsiTerm:
    def __init__(self, useColor = True):
        self.useColor = useColor
        self.undo_stack = []
        self.states = Ansi.getDefaultStates()
        self.styles = {}

    def setStyle(self, name, states):
        self.styles[name] = states;

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

    def fmt(self, string, states):
        return "%s%s%s" % (self.pushState(states), string, self.popStates())

    def fmt_r(self, string, states):
        return "%s%s%s" % (self.pushResetState(states), string, self.popStates())
