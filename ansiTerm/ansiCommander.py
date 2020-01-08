class AnsiCommander:
    dk_black_fg = '\033[30m'
    dk_red_fg = '\033[31m'
    dk_green_fg = '\033[32m'
    dk_yellow_fg = '\033[33m'
    dk_blue_fg = '\033[34m'
    dk_magenta_fg = '\033[35m'
    dk_cyan_fg = '\033[36m'
    dk_white_fg = '\033[37m'

    lt_black_fg = '\033[90m'
    lt_red_fg = '\033[91m'
    lt_green_fg = '\033[92m'
    lt_yellow_fg = '\033[93m'
    lt_blue_fg = '\033[94m'
    lt_magenta_fg = '\033[95m'
    lt_cyan_fg = '\033[96m'
    lt_white_fg = '\033[97m'

    dk_black_bg = '\033[40m'
    dk_red_bg = '\033[41m'
    dk_green_bg = '\033[42m'
    dk_yellow_bg = '\033[43m'
    dk_blue_bg = '\033[44m'
    dk_magenta_bg = '\033[45m'
    dk_cyan_bg = '\033[46m'
    dk_white_bg = '\033[47m'

    lt_black_bg = '\033[100m'
    lt_red_bg = '\033[101m'
    lt_green_bg = '\033[102m'
    lt_yellow_bg = '\033[103m'
    lt_blue_bg = '\033[104m'
    lt_magenta_bg = '\033[105m'
    lt_cyan_bg = '\033[106m'
    lt_white_bg = '\033[107m'

    all_off = '\033[0m'
    bold = '\033[1m'
    italic = '\033[3m'
    underline = '\033[4m'
    blink = '\033[5m'
    inverse = '\033[7m'
    hidden = '\033[8m'
    strike = '\033[9m'

    unbold = '\033[22m'
    unitalic = '\033[23m'
    ununderline = '\033[24m'
    unblink = '\033[25m'
    uninverse = '\033[27m'
    unhidden = '\033[28m'
    unstrike = '\033[29m'

    @staticmethod
    def systemColor(color_value, foreground):
        """ Decodes a color string like 'lt-red' into a color-selector string like '91'.
        """
        if color_value.startswith("dk-"):
            is_light = False
        elif color_value.startswith("lt-"):
            is_light = True
        else:
            raise Exception("Color format incorrect: \"%s\"" % color_value)

        if foreground:
            if not is_light:
                selector = '3'
            else:
                selector = '9'
        else:
            if not is_light:
                selector = '4'
            else:
                selector = '10'

        color_value = color_value[3:]
        if color_value == "black":
            color = '0'
        elif color_value == "red":
            color = '1'
        elif color_value == "green":
            color = '2'
        elif color_value == "yellow":
            color = '3'
        elif color_value == "blue":
            color = '4'
        elif color_value == "magenta":
            color = '5'
        elif color_value == "cyan":
            color = '6'
        elif color_value == "white":
            color = '7'

        return "%s%s" % (selector, color)

    @staticmethod
    def rgbColor(r, g, b, foreground):
        """Returns the ANSI/VT100 256-color escape code, in the RGB color
        range. r, g, and b can have values of 0-5."""
        num = 16    # the rgb numbers start at 16
        num += 36 * r
        num += 6 * g
        num += b
        if foreground:
            return "38;5;%d" % num
        else:
            return "48;5;%d" % num

    @staticmethod
    def grayColor(gray, foreground):
        """Returns the ANSI/VT1oo 256-color escape code, in the grayscale range.
        gray can have a value of 0-24."""
        if foreground:
            return "38;5;%d" % (gray + 232)
        else:
            return "48;5;%d" % (gray + 232)

    @staticmethod
    def getDefaultStates():
        return { }
        return {
            'fg-color' : 'system-lt-white',
            'bg-color' : 'system-dk-black',
            'bold' : 'off',
            'italic' : 'off',
            'under' : 'off',
            'blink' : 'off',
            'inverse' : 'off',
            'hidden' : 'off',
            'strike' : 'off'
        }

    @staticmethod
    def makeCommandlet(state):
        """ Make a code like '91' or '48;5;21' from a state like ( 'fg-color', 'system-lt-red') or ('bg-color', 'rgb-005').
        """
        state_type, state_value = state
        if state_type == "fg-color":
            color = True
            foreground = True
        elif state_type == "bg-color":
            color = True
            foreground = False
        elif state_type == "bold":
            color = False
            bold = True
        elif state_type == "italic":
            color = False
            italic = True
        elif state_type == "underline":
            color = False
            underline = True
        elif state_type == "blink":
            color = False
            blink = True
        elif state_type == "inverse":
            color = False
            inverse = True
        elif state_type == "hidden":
            color = False
            hidden = True
        elif state_type == "strike":
            color = False
            strike = True

        def select(state_value, on, off):
            if state_value == "on":
                return on
            elif state_value == 'off':
                return off
            else:
                raise Exception("Binary format incorrect: \"%s\"" % state_value)

        if color:
            if state_value.startswith("system-"):
                color = state_value[7:]

                if foreground:
                    return AnsiCommander.systemColor(color, foreground)
                else:
                    return AnsiCommander.systemColor(color, foreground)

            elif state_value.startswith("rgb-"):
                rgb_value = state_value[4:]
                r, g, b = [int(c) for c in rgb_value[0:3]]
                for c in [r, g, b]:
                    if c < 0 or c > 6:
                        raise Exception("Color format incorrect: \"%s\"" % state_value)

                if foreground:
                    return AnsiCommander.rgbColor(r, g, b, foreground)
                else:
                    return AnsiCommander.rgbColor(r, g, b, foreground)

            elif state_value.startswith("gs-"):
                gray_value = state_value[3:]
                gray = int(gray_value)
                if gray < 0 or gray > 24:
                    raise Exception("Color format incorrect: \"%s\"" % state_value)
                if foreground:
                    return AnsiCommander.grayColor(gray, foreground)
                else:
                    return AnsiCommander.grayColor(gray, foreground)

        elif bold:
            return select(state_value, '1', '22')

        elif italic:
            return select(state_value, '3', '23')

        elif underline:
            return select(state_value, '4', '24')

        elif blink:
            return select(state_value, '5', '25')

        elif inverse:
            return select(state_value, '7', '27')

        elif hidden:
            return select(state_value, '8', '28')

        elif strike:
            return select(state_value, '9', '29')

        else:
            raise Exception("Invalid state \"%s\"" % state_type)

    @staticmethod
    def makeCommandFromCommandlets(commandlets):
        """ Returns an ANSI terminal command like "\033[91;40;5;21m" from an iterable of commandlets like ['91, 40;5;21'].
        """
        cmd = ";".join(str(cmdl) for cmdl in commandlets)
        return "\033[%sm" % cmd

    @staticmethod
    def makeCommandFromStates(states):
        """ Returns an ANSI terminal command like "\033[91;40;5;21m" from an iterable of states like [( 'fg-color', 'system-lt-red'), ('bg-color', 'rgb-005')].
        """
        commandlets = [AnsiCommander.makeCommandlet(state) for state in states]
        return AnsiCommander.makeCommandFromCommandlets(commandlets)

    @staticmethod
    def applyChangesToStateSet(baseStates, newStates):
        for state in newStates:
            if state[1] != 'none':
                baseStates[state[0]] = state[1]

    @staticmethod
    def makeSetAndUndoCommands(baseStates, newStates):
        """ Returns the changelists for setting and undoing a set of state changes to an established state. Use this for getting the minimal ANSI command string for getting to the desired state, and for storing the command to undo this change in an undo buffer.
        baseStates is a map of string to string, like
            { 'fg-color' -> 'system-lt-red' }.
        newStates is an iterable of state tuples, like
            [('fg-color', 'system-lt-red'), ('bg-color', 'rgb-005')].
            Each is applied in turn to the baseStates and any necessary change states are recorded, as well as the command to undo it.
        """
        changelist = [] # holds ('fg-color', 'system-dk-blue') tuples, at most one for each state type.
        undolist = [] # holds like changelist
        seen = set() # holds like 'fg-color'
        state_types = set(baseStates) # 'fg-color', 'bg-color', 'underline', 'bold'...

        # For each state setting, if we haen't encountered its state type yet, and if it is
        # different than the current state, then record its action and how to undo it.
        for state_type, state_value in newStates.items():
            if state_type in seen:
                continue

            seen.add(state_type)

            if state_type in state_types:
                make_undo = True
                current_value = baseStates[state_type]
            else:
                make_undo = False

            if (state_type not in state_types or
                state_value != current_value):
                changelist.append( (state_type, state_value) )
                if make_undo:
                    undolist.append( (state_type, current_value) )

        return changelist, undolist
