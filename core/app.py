# Created By: Virgil Dupras
# Created On: 2011-06-12
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

from pdfminer.pdfparser import PDFSyntaxError

from hscommon.reg import RegistrableApplication
from hscommon.notify import Broadcaster
from hscommon.trans import tr

from .const import ElementState
from .pdf import extract_text_elements_from_pdf
from . import __appname__
from .gui.element_table import ElementTable
from .gui.opened_file_label import OpenedFileLabel
from .gui.page_controller import PageController
from .gui.build_pane import BuildPane
from .gui.edit_pane import EditPane

class JobType:
    LoadPDF = 'job_load_pdf'


JOBID2TITLE = {
    JobType.LoadPDF: tr("Reading PDF"),
}

class App(Broadcaster, RegistrableApplication):
    #--- model -> view calls:
    # open_path(path)
    # reveal_path(path)
    # setup_as_registered()
    # start_job(j, *args)
    
    PROMPT_NAME = __appname__
    
    def __init__(self, view):
        Broadcaster.__init__(self)
        RegistrableApplication.__init__(self, view, appid=6)
        self.current_path = None
        self._hide_ignored = False
        self.selected_elements = set()
        self.pages = []
        self.elements = []
        self.last_file_was_invalid = False
        
        self.element_table = ElementTable(self)
        self.opened_file_label = OpenedFileLabel(self)
        self.page_controller = PageController(self)
        self.build_pane = BuildPane(self)
        self.edit_pane = EditPane(self)
    
    #--- Overrides
    def _setup_as_registered(self):
        self.view.setup_as_registered()
    
    #--- Protected
    def _job_completed(self, jobid):
        # Must be called by subclasses when they detect that an async job is completed.
        if jobid == JobType.LoadPDF:
            if not self.last_file_was_invalid:
                self.notify('file_opened')
                self.notify('elements_changed')
            else:
                self.view.show_message("This file is not a PDF.")
    
    #--- Public (Internal)
    def select_elements(self, elements):
        if elements == self.select_elements:
            return
        self.selected_elements = elements
        self.notify('elements_selected')
    
    #--- Public (API)
    def open_path(self, path):
        self.view.open_path(path)
    
    def reveal_path(self, path):
        self.view.reveal_path(path)
    
    def change_state_of_selected(self, newstate):
        for element in self.selected_elements:
            if newstate == ElementState.Title:
                if element.state == ElementState.Title:
                    element.title_level += 1
                    if element.title_level > 6:
                        element.title_level = 1
                else:
                    element.title_level = 1
            element.state = newstate
        self.notify('elements_changed')
    
    def load_pdf(self, path):
        def do(j):
            self.last_file_was_invalid = False
            try:
                self.pages, self.elements = extract_text_elements_from_pdf(path, j)
                self.current_path = path
            except PDFSyntaxError:
                self.last_file_was_invalid = True
        
        self.view.start_job(JobType.LoadPDF, do)
    
    #--- Properties
    @property
    def hide_ignored(self):
        return self._hide_ignored
    
    @hide_ignored.setter
    def hide_ignored(self, value):
        self._hide_ignored = value
        self.notify('elements_changed')
    
