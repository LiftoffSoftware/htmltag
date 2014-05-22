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
    '<a href="http://liftoffsoftware.com/"><strong>I am already HTML. Don\'t escape me!</strong></a>'

Since Python doesn't allow modules to have dashes (-) in their names, if you
need to create a tag like that just use an underscore and change its 'tagname'
attribute::

    >>> from htmltag import foo_bar
    >>> print(foo_bar('baz')) # Before
    '<foo_bar>baz</foo_bar>'
    >>> foo_bar.tagname = 'foo-bar'
    >>> print(foo_bar('baz')) # Before
    '<foo-bar>baz</foo-bar>'

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
    '<a href="http://hacker/"><img src="javascript:alert(\'pwned!\')"></a>'
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
    '<a href="http://hacker/">&lt;img src="javascript:alert(\'pwned!\')"&gt;</a>'

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
