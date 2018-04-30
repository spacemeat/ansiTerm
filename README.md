# A Python library for controlling ANSI terminal codes, for setting color and effects to the command line terminal.

Includes:

*   Easy ANSI encodings for various color and effect states.

*   Style management. Name state groups and set styles by name.

*   A stack-based state manager. Efficiently encode state changes when applying a style or state group, and easily back out of the change when desired. This is great for nested markup.

    For instance, a tool you're writing may produce warning text with a bright yellow hue. In that warning might be a file path, with the directory in dark blue and the file in bright blue. With the stack based approach, you just push a color state, and then pop that state when it's time to switch back:

        print ('{warn}{warnLabel} Could not open file {dir}{name}: Not found.'.format(
            warn = t.pushState('warning'),
            warnLabel = t.fmt('Warning :', 'warnLabel'),
            dir = t.fmt(os.path.dirname(path), 'pathdir'),
            name = t.fmt(os.path.name(path), 'pathname')
        )

        
