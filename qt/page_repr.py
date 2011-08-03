# Created By: Virgil Dupras
# Created On: 2011-07-22
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QRect
from PyQt4.QtGui import QWidget, QPainter, QPen

from core.gui.page_repr import PageRepresentation as PageRepresentationModel, PageColor

COLORS = {
    PageColor.PageBg: Qt.white,
    PageColor.PageBorder: Qt.black,
    PageColor.ElemNormal: Qt.black,
    PageColor.ElemSelected: Qt.blue,
    PageColor.ElemIgnored: Qt.lightGray,
    PageColor.MouseSelection: Qt.blue,
}

class PageRepresentation(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)
        self.model = PageRepresentationModel(view=self, app=app.model)
    
    def _paintPage(self, painter):
        pagewidth = self.model.page.width
        pageheight = self.model.page.height
        ratio = pageheight / pagewidth
        # somehow, if we don't put the '-1's, the (bottom/right)most pixel line gets cropped.
        width = self.width() - 1
        height = self.height() - 1
        if width * ratio > height:
            # Our constraint is height, adjust according to it
            adjusted_width = height / ratio
            adjusted_height = height
            x = (width - adjusted_width) / 2
            y = 0
        else:
            # Our constraint is width, adjust according to it
            adjusted_width = width
            adjusted_height = width * ratio
            x = 0
            y = (height - adjusted_height) / 2
        r = QRect(x, y, adjusted_width, adjusted_height)
        painter.fillRect(r, Qt.white)
        painter.drawRect(r)
    
    #--- Qt Events
    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        self.current_painter = QPainter(self)
        self.model.draw(self.width(), self.height())
        del self.current_painter
    
    def mousePressEvent(self, event):
        self.model.mouse_down(event.x(), event.y())
    
    def mouseMoveEvent(self, event):
        self.model.mouse_move(event.x(), event.y())
    
    def mouseReleaseEvent(self, event):
        self.model.mouse_up()
    
    #--- model --> view
    def draw_rectangle(self, x, y, width, height, bgcolor, pencolor):
        painter = self.current_painter
        r = QRect(x, y, width, height)
        if bgcolor is not None:
            painter.fillRect(r, COLORS[bgcolor])
        if pencolor is not None:
            pen = QPen(painter.pen())
            pen.setColor(COLORS[pencolor])
            painter.setPen(pen)
            painter.drawRect(r)
    
    def refresh(self):
        self.update()
    
