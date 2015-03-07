# -*- coding: utf-8 -*-
#
#       Copyright 2014 Liftoff Software Corporation
#
# For license information see LICENSE.txt
from __future__ import unicode_literals

# Meta
__version__ = '1.7'
__version_info__ = (1, 7)
__license__ = "Apache 2.0"
__author__ = 'Dan McDougall <daniel.mcdougall@liftoffsoftware.com>'

# NOTE: The doctests only pass in Python 3 due to the missing u'' syntax.

__doc__ = """\
The htmltag module
==================
.. note::

    The latest, complete documentation of htmltag can be found here:
    http://liftoff.github.io/htmltag/

    The latest version of this module can be obtained from Github:
    https://github.com/LiftoffSoftware/htmltag

htmltag.py - A Python (2 *and* 3) module for wrapping whatever strings you want
in HTML tags. Example::

    >>> from htmltag import strong
    >>> print(strong("SO STRONG!"))
    <strong>SO STRONG!</strong>

What tags are supported?  All of them!  An important facet of modern web
programming is the ability to use your own custom tags.  For example::

    >>> from htmltag import foobar
    >>> foobar('Custom tag example')
    '<foobar>Custom tag example</foobar>'

To add attributes inside your tag just pass them as keyword arguments::

    >>> from htmltag import a
    >>> print(a('awesome software', href='http://liftoffsoftware.com/'))
    <a href="http://liftoffsoftware.com/">awesome software</a>

To work around the problem of reserved words as keyword arguments (i.e. can't
have 'class="foo"') just prefix the keyword with an underscore like so::

    >>> from htmltag import div
    >>> print(div("example", _class="someclass"))
    <div class="someclass">example</div>

Another option--which is useful for things like 'data-\*' attributes--is to pass
keyword arguments as a dict using the `\*\* operator
<http://docs.python.org/2/tutorial/controlflow.html#unpacking-argument-lists>`_
like so::

    >>> from htmltag import li
    >>> print(li("CEO", **{"class": "user", "data-name": "Dan McDougall"}))
    <li class="user" data-name="Dan McDougall">CEO</li>

If you want to use upper-case tags just import them in caps:

    >>> from htmltag import STRONG
    >>> print(STRONG('whatever'))
    <STRONG>whatever</STRONG>

Combining Tags and Content
--------------------------
You can combine multiple tags to create a larger HTML string like so::

    >>> from htmltag import table, tr, td
    >>> print(table(
    ...     tr(td('100'), td('200'), id="row1"),
    ...     tr(td('150'), td('250'), id="row2"),
    ... ))
    <table><tr id="row1"><td>100</td><td>200</td></tr><tr id="row2"><td>150</td><td>250</td></tr></table>

**NOTE:** If you're going to do something like the above please use a *real*
template language/module instead of `htmltag`.  You're *probably* "doing it
wrong" if you end up with something like the above in your code.  For example,
try `Tornado's template engine
<http://www.tornadoweb.org/en/stable/template.html>`_.

Special Characters
------------------
Special characters that cause trouble like, '<', '>', and '&' will be
automatically converted into HTML entities.  If you don't want that to happen
just wrap your string in :class:`htmltag.HTML` like so::

    >>> from htmltag import HTML, a
    >>> txt = HTML("<strong>I am already HTML. Don't escape me!</strong>")
    >>> a(txt, href="http://liftoffsoftware.com/")
    '<a href="http://liftoffsoftware.com/"><strong>I am already HTML. Don\\'t escape me!</strong></a>'

Since Python doesn't allow modules to have dashes (-) in their names, if you
need to create a tag like that just use an underscore and change its 'tagname'
attribute::

    >>> from htmltag import foo_bar
    >>> print(foo_bar('baz')) # Before
    <foo_bar>baz</foo_bar>
    >>> foo_bar.tagname = 'foo-bar'
    >>> print(foo_bar('baz')) # After
    <foo-bar>baz</foo-bar>

By default self-closing HTML tags like '<img>' will not include an ending slash.
To change this behavior (i.e. for XHTML) just set 'ending_slash' to `True`::

    >>> from htmltag import img
    >>> img.ending_slash = True
    >>> img(src="http://somehost/images/image.png")
    '<img src="http://somehost/images/image.png" />'
    >>> img.ending_slash = False # Reset for later doctests

Protections Against Cross-Site Scripting (XSS)
----------------------------------------------
By default all unsafe (XSS) content in HTML tags will be removed::

    >>> from htmltag import a, img
    >>> a(img(src="javascript:alert('pwned!')"), href="http://hacker/")
    '<a href="http://hacker/">(removed)</a>'

If you want to change this behavior set the tag's 'safe_mode' attribute like
so::

    >>> from htmltag import a, img
    >>> a.safe_mode = False
    >>> img.safe_mode = False
    >>> a(img(src="javascript:alert('pwned!')"), href="http://hacker/")
    '<a href="http://hacker/"><img src="javascript:alert(\\'pwned!\\')"></a>'
    >>> a.safe_mode = True # Reset for later doctests
    >>> img.safe_mode = True # Ditto

You may also change the replacement text if you like::

    >>> from htmltag import a, img
    >>> img.replacement = "No no no!"
    >>> a(img(src="javascript:alert('pwned!')"), href="http://hacker/")
    '<a href="http://hacker/">No no no!</a>'

If you set 'replacement' to 'entities' the rejected HTML will be converted to
character entities like so::

    >>> from htmltag import a, img
    >>> a.replacement = "entities"
    >>> img.replacement = "entities"
    >>> a(img(src="javascript:alert('pwned!')"), href="http://hacker/")
    '<a href="http://hacker/">&lt;img src="javascript:alert(\\'pwned!\\')"&gt;</a>'

It is also possible to create a whitelist of allowed tags.  All other tags
contained therein will automatically be replaced::

    >>> from htmltag import span
    >>> whitelist = ['span', 'b', 'i', 'strong']
    >>> span.whitelist = whitelist
    >>> span(HTML('This is <b>bold</b> new lib is <script>awesome();</script>'))
    '<span>This is <b>bold</b> new lib is (removed)awesome();(removed)</span>'

Lastly, all strings returned by `htmltag` are actually a subclass of `str`:
`~htmltag.HTML`.  It has a useful `escaped` property:

    >>> from htmltag import address
    >>> address.safe_mode = False # Turn off so we have a dangerous example ;)
    >>> html = address('1 Hacker Ln., Nowhere, USA')
    >>> print(html)
    <address>1 Hacker Ln., Nowhere, USA</address>
    >>> print(html.escaped)
    &lt;address&gt;1 Hacker Ln., Nowhere, USA&lt;/address&gt;

This can be extremely useful if you want to be double-sure that no executable
stuff ends up in your program's output.


Functions and Classes
=====================
"""

import sys, re, cgi, logging
from types import ModuleType

if sys.version_info.major == 2:
    stringtype = unicode
else: # Python 3
    stringtype = str

self_closing_tags = set([
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
    'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr',
])
FILE = __file__

def strip_xss(html, whitelist=None, replacement="(removed)"):
    """
    This function returns a tuple containing:

        * *html* with all non-whitelisted HTML tags replaced with *replacement*.
        * A `set()` containing the tags that were removed.

    Any tags that contain JavaScript, VBScript, or other known XSS/executable
    functions will also be removed.

    If *whitelist* is not given the following will be used::

        whitelist = set([
            'a', 'abbr', 'aside', 'audio', 'bdi', 'bdo', 'blockquote', 'canvas',
            'caption', 'code', 'col', 'colgroup', 'data', 'dd', 'del',
            'details', 'div', 'dl', 'dt', 'em', 'figcaption', 'figure', 'h1',
            'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'li',
            'mark', 'ol', 'p', 'pre', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
            'small', 'source', 'span', 'strong', 'sub', 'summary', 'sup',
            'table', 'td', 'th', 'time', 'tr', 'track', 'u', 'ul', 'var',
            'video', 'wbr'
        ])

    .. note:: To disable the whitelisting simply set `whitelist="off"`.

    Example::

        >>> html = '<span>Hello, exploit: <img src="javascript:alert(\"pwned!\")"></span>'
        >>> html, rejects = strip_xss(html)
        >>> print("'%s', Rejected: '%s'" % (html, " ".join(rejects)))
        '<span>Hello, exploit: (removed)</span>', Rejected: '<img src="javascript:alert("pwned!")">'

    .. note:: The default *replacement* is "(removed)".

    If *replacement* is "entities" bad HTML tags will be encoded into HTML
    entities.  This allows things like <script>'whatever'</script> to be
    displayed without execution (which would be much less annoying to users that
    were merely trying to share a code example).  Here's an example::

        >>> html = '<span>Hello, exploit: <img src="javascript:alert(\"pwned!\")"></span>'
        >>> html, rejects = strip_xss(html, replacement="entities")
        >>> print(html)
        <span>Hello, exploit: &lt;img src="javascript:alert("pwned!")"&gt;</span>
        >>> print("Rejected: '%s'" % ", ".join(rejects))
        Rejected: '<img src="javascript:alert("pwned!")">'

    **NOTE:** This function should work to protect against *all* `the XSS
    examples at OWASP
    <https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet>`_.  Please
    `let us know <https://github.com/LiftoffSoftware/htmltag/issues>`_ if you
    find something we missed.
    """
    re_html_tag = re.compile( # This matches HTML tags (if used correctly)
      "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>")
    # This will match things like 'onmouseover=' ('on<whatever>=')
    on_events_re = re.compile('.*\s+(on[a-z]+\s*=).*')
    if not whitelist:
        # These are all pretty safe and covers most of what users would want in
        # terms of formatting and sharing media (images, audio, video, etc).
        whitelist = set([
            'a', 'abbr', 'aside', 'audio', 'bdi', 'bdo', 'blockquote', 'canvas',
            'caption', 'code', 'col', 'colgroup', 'data', 'dd', 'del',
            'details', 'div', 'dl', 'dt', 'em', 'figcaption', 'figure', 'h1',
            'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'li',
            'mark', 'ol', 'p', 'pre', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
            'small', 'source', 'span', 'strong', 'sub', 'summary', 'sup',
            'table', 'td', 'th', 'time', 'tr', 'track', 'u', 'ul', 'var',
            'video', 'wbr'
        ])
    elif whitelist == "off":
        whitelist = None # Disable it altogether
    bad_tags = set()
    for tag in re_html_tag.finditer(html):
        tag = tag.group()
        tag_lower = tag.lower()
        short_tag = tag_lower.split()[0].lstrip('</').rstrip('>')
        if whitelist and short_tag not in whitelist:
            bad_tags.add(tag)
            continue
        # Make sure the tag can't execute any JavaScript
        if "javascript:" in tag_lower:
            bad_tags.add(tag)
            continue
        # on<whatever> events are not allowed (just another XSS vuln)
        if on_events_re.search(tag_lower):
            bad_tags.add(tag)
            continue
        # Flash sucks
        if "fscommand" in tag_lower:
            bad_tags.add(tag)
            continue
        # I'd be impressed if an attacker tried this one (super obscure)
        if "seeksegmenttime" in tag_lower:
            bad_tags.add(tag)
            continue
        # Yes we'll protect IE users from themselves...
        if "vbscript:" in tag_lower:
            bad_tags.add(tag)
            continue
    if replacement == "entities":
        for bad_tag in bad_tags:
            escaped = cgi.escape(bad_tag).encode('ascii', 'xmlcharrefreplace')
            html = html.replace(bad_tag, escaped.decode('ascii'))
    else:
        for bad_tag in bad_tags:
            html = html.replace(bad_tag, replacement)
    return (html, bad_tags)

class HTML(stringtype):
    """
    .. versionadded:: 1.2.0

    A subclass of Python's built-in `str` to add a simple `__html__` method
    that lets us know this string is HTML and does not need to be escaped.  It
    also has an `escaped` property that will return `self` with all special
    characters converted into HTML entities.
    """
    tagname = None
    def __html__(self):
        """
        Returns `self` (we're already a string) in unmodified form.
        """
        return self

    @property
    def escaped(self):
        """
        A property that returns `self` with all characters that have special
        meaning (in HTML/XML) replaced with HTML entities.  Example::

            >>> print(HTML('<span>These span tags will be escaped</span>').escaped)
            &lt;span&gt;These span tags will be escaped&lt;/span&gt;
        """
        return cgi.escape(self).encode(
            'ascii', 'xmlcharrefreplace').decode('ascii')

    def append(self, *strings):
        """
        Adds any number of supplied *strings* to `self` (we're a subclass of
        `str` remember) just before the last closing tag and returns a new
        instance of `~htmltag.HTML` with the result.
        Example::

            >>> from htmltag import span, b
            >>> html = span('Test:')
            >>> print(html)
            <span>Test:</span>
            >>> html = html.append(' ', b('appended'))
            >>> print(html)
            <span>Test: <b>appended</b></span>

        In the case of self-closing tags like '<img>' the string will simply be
        appended after the tag::

            >>> from htmltag import img
            >>> image = img(src="http://company.com/image.png")
            >>> print(image.append("Appended string"))
            <img src="http://company.com/image.png">Appended string

        .. note:: Why not update ourselves in-place?  Because we're a subclass
            of `str`; in Python strings are immutable.
        """
        close_tag_start = self.rfind('</')
        if self.tagname: # More accurate
            close_tag_start = self.rfind('</'+self.tagname)
        if close_tag_start == -1: # Couldn't find closing tag
            return self + "".join(strings) # Just tack on to the end
        ending = self[close_tag_start:]
        beginning = self[:close_tag_start]
        if self.tagname: # Preserve it
            tagname = self.tagname
            new = HTML(beginning + "".join(strings) + ending)
            new.tagname = tagname
            return new
        else:
            return HTML(beginning + "".join(strings) + ending)

class TagWrap(object):
    """
    Lets you wrap whatever string you want in whatever HTML tag (*tagname*) you
    want.

    **Optional Keyword Arguments:**

    :keyword safe_mode: If `True` dangerous (XSS) content will be removed
        from all HTML.  Defaults to `True`
    :keyword whitelist: If given only tags that exist in the whitelist will be
        allowed.  All else will be escaped into HTML entities.
    :keyword replacement: A string to replace unsafe HTML with.  If set to
        "entities", will convert unsafe tags to HTML entities so they
        display as-is but won't be evaluated by renderers/browsers'.  The
        defaults is "(removed)".
    :keyword log_rejects: If `True` rejected unsafe (XSS) HTML will be
        logged using :meth:`logging.error`.  Defaults to `False`
    :keyword ending_slash: If `True` self-closing HTML tags like '<img>'
        will not have a '/' placed before the '>'.  Usually only necessary
        with XML and XHTML documents (as opposed to regular HTML).  Defaults
        to `False`.
    :type safe_mode: boolean
    :type whitelist: iterable
    :type replacement: string, "entities", or "off"
    :type log_rejects: boolean
    :type ending_slash: boolean

    The `TagWrap` class may be used in a direct fashion (as opposed to the
    metaprogramming magic way: ``from htmltag import sometag``)::

        >>> from htmltag import TagWrap
        >>> img = TagWrap('img', ending_slash=True)
        >>> print(img(src="http://company.com/someimage.png"))
        <img src="http://company.com/someimage.png" />

    The `TagWrap` class also has a :meth:`~TagWrap.copy` method which can be
    useful when you want a new tag to have the same attributes as another::

        >>> from htmltag import TagWrap
        >>> whitelist = ["b", "i", "strong", "a", "em"]
        >>> replacement = "(tag not allowed)"
        >>> b = TagWrap('b', whitelist=whitelist, replacement=replacement)
        >>> i = b.copy('i')
        >>> print(i.whitelist)
        ['b', 'i', 'strong', 'a', 'em']

    Here's how you can create a number of tags with your own custom settings all
    at once::

        >>> import sys
        >>> from htmltag import TagWrap
        >>> whitelist = ["b", "i", "strong", "a", "em"] # Whitelist ourselves
        >>> replacement = "(tag not allowed)"
        >>> for tag in whitelist:
        ...     setattr(sys.modules[__name__], tag,
        ...         TagWrap(tag, whitelist=whitelist, replacement=replacement))
        >>> strong.replacement # doctest: +SKIP
        '(tag not allowed)'    # doctest: +SKIP

    .. note:: ``sys.modules[__name__]`` is the current module; the global 'self'.
    """
    # NOTE: The above doctest is skipped because it only works in reality :)
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname
        self.safe_mode = kwargs.get('safe_mode', True)
        self.whitelist = kwargs.get('whitelist', "off")
        self.replacement = kwargs.get('replacement', '(removed)')
        self.log_rejects = kwargs.get('log_rejects', False)
        # This only applies to self-closing tags:
        self.ending_slash = kwargs.get('ending_slash', False)

    def escape(self, string):
        """
        Returns *string* with all instances of '<', '>', and '&' converted into
        HTML entities.
        """
        html_entities = {"&": "&amp;", '<': '&lt;', '>': '&gt;'}
        return HTML("".join(html_entities.get(c, c) for c in string))

    def wrap(self, tag, *args, **kwargs):
        """
        Returns all *args* (strings) wrapped in HTML tags like so::

            >>> b = TagWrap('b')
            >>> print(b('bold text'))
            <b>bold text</b>

        To add attributes to the tag you can pass them as keyword arguments::

            >>> a = TagWrap('a')
            >>> print(a('awesome software', href='http://liftoffsoftware.com/'))
            <a href="http://liftoffsoftware.com/">awesome software</a>

        .. note:: :meth:`~TagWrap.wrap` will automatically convert '<', '>', \
        and '&' into HTML entities unless the wrapped string has an `__html__` \
        method
        """
        template = "<{tagstart}>{content}</{tag}>"
        if tag in self_closing_tags:
            template = "<{tagstart}>" # self-closing tags don't have content
            if self.ending_slash:
                template = "<{tagstart} />"
        content = ""
        for string in args:
            if not hasattr(string, '__html__'): # Indicates already escaped
                string = self.escape(string)
            content += string.__html__()
        tagstart = tag
        if kwargs:
            tagstart += ' '
            for key, value in kwargs.items():
                key = key.lstrip('_')
                if value == True:
                    tagstart = tagstart + key + ' '
                elif value == False:
                    continue # skip it altogether
                else:
                    tagstart = tagstart + '{key}="{value}" '.format(
                        key=key, value=value)
            tagstart = tagstart.rstrip()
        html = template.format(tagstart=tagstart, content=content, tag=tag)
        if self.safe_mode:
            html, rejected = strip_xss(
                html, whitelist=self.whitelist, replacement=self.replacement)
            if self.log_rejects:
                logging.error(
                    "{name} rejected unsafe HTML: '{rejected}'".format(
                    name=self.__class__.__name__, rejected=rejected))
        html = HTML(html)
        html.tagname = tag # So we can easily append()
        return html

    def copy(self, tagname, **kwargs):
        """
        Returns a new instance of `TagWrap` using the given *tagname* that has
        all the same attributes as this instance.  If *kwargs* is given they
        will override the attributes of the created instance.
        """
        new_kwargs = {
            'replacement': self.replacement,
            'whitelist': self.whitelist,
            'safe_mode': self.safe_mode,
            'log_rejects': self.log_rejects,
            'ending_slash': self.ending_slash
        }
        new_kwargs.update(**kwargs)
        return TagWrap(tagname, **new_kwargs)

    def __call__(self, *args, **kwargs):
        return self.wrap(self.tagname, *args, **kwargs)

    def __getitem__(self, k):
        if k == "__all__":
            raise ImportError("Cannot 'import *' with htmltag.")
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
    This class is the magic that lets us do things like::

        >>> from htmltag import span
    """
    def __init__(self, tagname, *args, **kwargs):
        self.tagname = tagname
        # This is necessary for reload() to work and so we don't overwrite
        # these values with instances of TagWrap:
        no_override = [
            'HTML', 'SelfWrap', 'TagWrap', 'strip_xss', '__author__',
            '__builtins__', '__doc__', '__license__', '__name__',
            '__package__', '__version__', '__version_info__'
        ]
        for attr in no_override:
            setattr(self, attr, getattr(tagname, attr, None))
        self.__path__ = [] # Required for Python 3.3
        self.__file__ = FILE # Needed for Sphinx docs

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
    # NOTE: Execute `python htmltag.py -v` to run the doctests.
    # Doctests should work in both Python 2 and Python 3.
    import doctest
    doctest.testmod()
else:
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrap(self)
