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
    '<a href="http://liftoffsoftware.com/"><strong>I am already escaped. Don\'t escape me!</strong></a>'
