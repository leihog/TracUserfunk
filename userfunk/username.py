# -*- coding: utf-8 -*-

from trac.wiki.macros import WikiMacroBase

class UsernameMacro(WikiMacroBase):
    """
    Outputs the username of the authenticated user.

    Usage:
    {{{
    [[Username]]
    }}}
    """
    def expand_macro(self, formatter, name, args):
        return formatter.req.authname;
