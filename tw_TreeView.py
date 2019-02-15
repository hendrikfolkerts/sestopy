# -*- coding: utf-8 -*-

__author__ = 'Hendrik Folkerts'


#Example for importing modules optionally
def foo():
    try:
        import external_module
    except ImportError:
        pass

    if external_module:
        external_module.some_whizzy_feature()
    else:
        print("You could be using a whizzy feature right now, if you had external_module.")