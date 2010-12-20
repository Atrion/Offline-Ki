# -*- coding: utf-8 -*-
# Describe classes, methods and functions in a Plasma module.

import inspect
import os, sys

INDENT=0
out = open('doc', 'w')

def wi(*args):
    """ Function to print lines indented according to level """

    if INDENT: print >>out, '*'*INDENT,
    for arg in args: print >>out, arg,
    print >>out

def cp(*args):
    """ Function to print captions indented according to level """
    print >>out, '='*(INDENT+2),
    for arg in args: print >>out, arg,
    print >>out, '='*(INDENT+2),
    print >>out

def indent():
    """ Increase indentation """

    global INDENT
    INDENT += 1

def dedent():
    """ Decrease indentation """

    global INDENT
    INDENT -= 1

def describe_routine(obj):
    """ Describe the function object passed as argument. """

    # parse the parameters. The format of __doc__ is like this:
    # Params: list,of,parameters
    # description (may contain newlines)
    doc = obj.__doc__
    if not doc: doc = ''
    lines = doc.split('\n')
    params = lines[0]
    if params.startswith("Params: "):
        params = params[len("Params: "):]
        doc = ';'.join(lines[1:])
    else:
        params = ''
        doc = doc.replace('\n', ';')

    if inspect.ismethod(obj):
        str = "'''Method''': "
    else:
        str = "'''Function''': "
    str += obj.__name__ + '(' + params + ')'
    if len(doc): str += ' - '+doc
    wi(str)

def describe(sth):
    """ Describe whatever was passed as argument """
    if inspect.isroutine(sth):
        describe_routine(sth)
    elif inspect.isclass(sth) or inspect.ismodule(sth):
        type = 'Module'
        if inspect.isclass(sth): type = 'Class'
        try:
            cp("'''%s''': %s" % (type, sth.__name__))
        except: # an instance of a class does not seem to have __name__
            cp("'''%s'''" % type)

        indent()
        for name in dir(sth):
            if name.startswith('__') and name.endswith('__'): continue # prevent an endless loop
            obj = getattr(sth, name)
            if isinstance(obj, property):
                doc = obj.__doc__
                if not doc: doc = ''
                str = "'''Property''': "+name
                if len(doc): str += ' - '+doc.replace('\n', ';')
                wi(str)
            else:
                describe(obj)
        dedent()
    else:
        wi("Unknown something %s: %s" % (`sth`, `dir(sth)`))
