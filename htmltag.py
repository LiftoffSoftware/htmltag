# -*- coding: utf-8 -*-
#
#       Copyright 2013 Liftoff Software Corporation
#
# For license information see LICENSE.txt

# Meta
__version__ = '1.0.0'
__version_info__ = (1, 0, 0)
__license__ = "Apache 2.0"
__author__ = 'Dan McDougall <daniel.mcdougall@liftoffsoftware.com>'

__doc__ = """\
htmltag.py - A Python (2 *and* 3) module for wrapping whatever strings you want
in HTML tags. Example::

    >>> from htmltag import strong
    >>> print(strong("SO STRONG!"))
    <strong>SO STRONG!</strong>

What tags are supported?  All of them!  An important facet of HTML5 is the
ability to use your own custom tags.  For example::

    >>> from htmltag import foobar
    >>> foobar('Custom tag example')
    '<foobar>Custom tag example</foobar>'

To add attributes inside your tag just pass them as keyword arguments::

    >>> from htmltag import a
    >>> print(a('awesome software', href='http://liftoffsoftware.com/'))
    <a href="http://liftoffsoftware.com/">awesome software</a>

You can combine multiple tags to create a larger HTML string like so::

    >>> from htmltag import table, tr, td
    >>> print(table(
    ...     tr(td('100'), td('200'), id="row1"),
    ...     tr(td('150'), td('250'), id="row2"),
    ... ))
    <table><tr id="row1"><td>100</td><td>200</td></tr><tr id="row2"><td>150</td><td>250</td></tr></table>

.. note:: If you're going to do something like the above please use a *real* template language/module instead of `htmltag`.  You're *probably* "doing it wrong" if you end up with something like the above in your code.  For example, try Tornado's template engine (http://www.tornadoweb.org/en/stable/template.html).

Special characters that cause trouble like, '<', '>', and '&' will be
automatically converted into HTML entities.  If you are passing a string that
already has these entities escaped and don't want them double-escaped just wrap
your string in :class:`htmltag.Escaped` like so::

    >>> from htmltag import Escaped, a
    >>> txt = Escaped("<strong>I am already escaped. Don't escape me!</strong>")
    >>> a(txt, href="http://liftoffsoftware.com/")
    '<a href="http://liftoffsoftware.com/"><strong>I am already escaped. Don\\'t escape me!</strong></a>'
"""

import sys
from types import ModuleType

class Escaped(str):
    """
    A subclass of Python's built-in `str` to add a simple `__html__` method
    that lets us know this string has already been escaped.
    """
    def __html__(self):
        return self

class TagWrap(object):
    """
    Lets you wrap whatever string you want in whatever tag you want.
    """
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname

    def escape(self, string):
        """
        Converts '<', '>', and '&' into HTML entities.
        """
        html_entities = {"&": "&amp;", '<': '&lt;', '>': '&gt;'}
        return Escaped("".join(html_entities.get(c, c) for c in string))

    def wrap(self, tag, *args, **kwargs):
        """
        Returns *string* wrapped in HTML tags like so::

            >>> b = TagWrap('b')
            >>> print(b('bold text'))
            <b>bold text</b>

        To add attributes to the tag you can pass them as keyword args:

            >>> a = TagWrap('a')
            >>> print(a('awesome software', href='http://liftoffsoftware.com/'))
            <a href="http://liftoffsoftware.com/">awesome software</a>

        .. note:: Will automatically convert '<', '>', and '&' into HTML entities.
        """
        combined = ""
        for string in args:
            if not hasattr(string, '__html__'): # Indicates already escaped
                string = self.escape(string)
            combined += string.__html__()
        tagstart = tag
        if kwargs:
            tagstart += ' '
            for key, value in kwargs.items():
                tagstart = tagstart + '{key}="{value}" '.format(
                    key=key, value=value)
            tagstart = tagstart.rstrip()
        return Escaped("<{tagstart}>{combined}</{tag}>".format(
            tagstart=tagstart, combined=combined, tag=tag))

    def __call__(self, *args, **kwargs):
        return self.wrap(self.tagname, *args, **kwargs)

    def __getitem__(self, k):
        if isinstance(k, str):
            if k.startswith('__') and k.endswith("__"):
                raise AttributeError
            elif k in self.__dict__:
                return self.__dict__[k]
        raise ImportError(
            "Using IPython?  Ignore that ^ traceback stuff and try again "
            "(second time usually works to get your traceback)")

class SelfWrap(ModuleType):
    """
    This is the magic that lets us do things like::

        >>> from htmltag import span
    """
    def __init__(self, tagname, *args, **kwargs):
        self.tagname = tagname
        # This is necessary for reload() to work and so we don't overwrite
        # these values with instances of TagWrap:
        no_override = [
            'Escaped', 'SelfWrap', '__author__', '__builtins__', '__doc__',
            '__license__', '__name__', '__package__', '__version__',
            '__version_info__'
        ]
        for attr in no_override:
            setattr(self, attr, getattr(tagname, attr, None))
        self.__path__ = [] # Required for Python 3.3

    def __getattr__(self, name): # "from htmltag import a" <--*name* will be 'a'
        # This is how Python looks up the module name
        if name not in self.__dict__: # So we don't overwrite what's already set
            # Make our instance of TagWrap exist so we can return it properly
            setattr(self, name, TagWrap(name))
        return self.__dict__[name]

    def __call__(self, *args, **kwargs):
        # This turns the 'a' in "from htmltag import a" into a callable:
        return TagWrap(self.tagname, *args, **kwargs)

if __name__ == "__main__":
    """
    Execute `python htmltag.py -v` to run the doctests.
    """
    import doctest
    doctest.testmod()
else:
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrap(self)
