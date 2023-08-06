# -*- coding: utf-8 -*-


class QTemplateTag:
    """ Base QTemplateWidget Tags used to modify the parent QWidget in but does
        not represent a QWidget itself. This allows a plugin developer to extend
        the capacilities of the qtemplate parser.
    """

    def __init__(self, qtmpl, elem, parent, context, *args):
        self.qtmpl = qtmpl          # Ref to parent QTemplateWidget object
        self.elem = elem            # Current etree item to render children
        self.parent = parent        # Parent qobj to add children to
        self.context = context      # Context for building the children
