# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Toggle Active Layer
Description          : Plugin for toggle visibility of active layer
Date                 : June, 2015
copyright            : (C) 2015 by Luiz Motta
email                : motta.luiz@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtGui import ( QAction, QIcon )
from PyQt4.QtCore import pyqtSlot

from toggleactivelayer import ToggleActiveLayerMapTool

import os

def classFactory(iface):
  return ToggleActiveLayerPlugin( iface )

class ToggleActiveLayerPlugin:

  def __init__(self, iface):
    self.iface = iface
    self.canvas = iface.mapCanvas() 

    self.action = None
    self.tool = ToggleActiveLayerMapTool( self.iface )

  def initGui(self):
    title = "Toggle visibility of active layer"
    icon = QIcon( os.path.join( os.path.dirname(__file__), 'toggleactivelayer.png' ) )
    self.action = QAction( icon, title, self.iface.mainWindow() )
    self.action.setObjectName( "ToggleActiveLayerPlugin" )
    self.action.setWhatsThis( title )
    self.action.setStatusTip( title )
    self.action.triggered.connect( self.run )

    # Maptool
    self.action.setCheckable( True )
    self.tool.setAction( self.action )

    self.iface.addToolBarIcon( self.action )

  def unload(self):
    self.iface.removeToolBarIcon( self.action )
    del self.action

  @pyqtSlot()
  def run(self):
    if self.canvas.mapTool() != self.tool:
      self.canvas.setMapTool( self.tool)
