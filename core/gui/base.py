# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.notify import Listener

class GUIObject(Listener):
    def __init__(self, view, app):
        Listener.__init__(self, app)
        self.view = view
        self.app = app
    
    def elements_changed(self):
        # The list of loaded elements have changed.
        pass
    
    def file_opened(self):
        pass
    
