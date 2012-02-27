# -*- coding: utf-8 -*-
#
# Idea and code borrowed from:
# http://code.activestate.com/recipes/498062-nicely-readable-timedelta/
#

from datetime import timedelta

unit_names = {"year" : ("year", "years"),
              "month" : ("month", "months"),
              "week" : ("week", "weeks"),
              "day" : ("day", "days"),
              "hour" : ("hour", "hours"),
              "minute" : ("minute", "minutes"),
              "second" : ("second", "seconds")}

num_repr = {1 : "one",
            2 : "two",
            3 : "three",
            4 : "four",
            5 : "five",
            6 : "six",
            7 : "seven",
            8 : "eight",
            9 : "nine",
            10 : "ten",
            11 : "eleven",
            12 : "twelve"}

def amount_to_str(amount):
    if amount in num_repr:
        return num_repr[amount]
    return str(amount)

def seconds_in_units(seconds):
    """
    Returns a tuple containing the most appropriate unit for the
    number of seconds supplied and the value in that units form.

        >>> seconds_in_units(7700)
        (2, 'hour')
    """
    unit_limits = [("year", 365 * 24 * 3600),
                   ("month", 30 * 24 * 3600),
                   ("week", 7 * 24 * 3600),
                   ("day", 24 * 3600),
                   ("hour", 3600),
                   ("minute", 60)]
    for unit_name, limit in unit_limits:
        if seconds >= limit:
            amount = int(round(float(seconds) / limit))
            return amount, unit_name
    return seconds, "second"

def stringify(td):
    """
    Converts a timedelta into a nicely readable string.

        >>> td = timedelta(days = 77, seconds = 5)
        >>> print stringify(td)
        two months
    """
    seconds = td.days * 3600 * 24 + td.seconds
    amount, unit_name = seconds_in_units(seconds)

    i18n_amount = amount_to_str(amount)
    i18n_unit = unit_names[unit_name][1]
    if amount == 1:
        i18n_unit = unit_names[unit_name][0]
    return "%s %s" % (i18n_amount, i18n_unit)

