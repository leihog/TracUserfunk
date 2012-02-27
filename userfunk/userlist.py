# -*- coding: utf-8 -*-

from datetime import datetime
import inspect
import re
import sys
import time

from trac.core import *
from trac.wiki.api import IWikiMacroProvider
from trac.wiki.macros import WikiMacroBase
from trac.wiki.formatter import Formatter, system_message, format_to_html

import texttime

class UserlistMacro(WikiMacroBase):
    """
    Produces a list of users with their 
    names, email, time of last login and the elapsed time
    since their last login.

    Usage:
    {{{
    [[Userlist]]
    }}}
    """

    def expand_macro(self, formatter, name, content):
        content = format_to_html(self.env, formatter.context, self.make_table())
        content = '<div class="component-list">%s</div>' % content
        return content

    def make_table(self):
        tab =  "||'''User'''"
        tab += "||'''Name'''"
        tab += "||'''Email'''"
        tab += "||'''Last login'''"
        tab += "||'''How long ago'''"
        tab += "||\n"

        for k, user in self.get_users().iteritems():
            tab += "|| %s " % user['username']
            tab += "|| %s " % user['name']
            tab += "|| %s " % user['email']
            tab += "|| %s " % user['last_login']
            tab += "|| %s " % user['how_long_ago']
            tab += "||\n"

        return tab

    def get_last_login(self, username):
        cursor = self.env.get_db_cnx().cursor()
        cursor.execute("SELECT last_visit FROM session WHERE sid=%s AND authenticated=%s", (username, 1))
        row = cursor.fetchone()
        if not row:
            return { 'uid': username, 'last_login': '', 'how_long_ago': ''};

        when = time.localtime(int(row[0]))
        last = datetime.fromtimestamp(int(row[0]))
        now = datetime.fromtimestamp(time.time())
        how_long = now - last
        last_date = time.strftime("%Y/%m/%d %H:%M:%S", when)

        ago = "%s" % texttime.stringify(how_long)

        return { 'last_login': last_date, 'how_long_ago': ago }

    def get_users(self):

        users = {}
        try:
            from acct_mgr.api import AccountManager, get_user_attribute
            acct_mgr = AccountManager(self.env)
            for username in acct_mgr.get_users():
                users[username] = { 'username': username }

            for username, status in get_user_attribute(self.env, username=None, authenticated=None).iteritems():
                user = users.get(username)
                if user is not None and 1 in status:
                    user['name'] = status[1].get('name')
                    user['email'] = status[1].get('email')
                    user.update(self.get_last_login(username))

        except:
            for username, name, email in self.env.get_known_users():
                user = { 'username': username, 'name': name, 'email': email }
                user.update(self.get_last_login(username))
                users[username] = user

        return users

