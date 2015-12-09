# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SWDESzukaj
                                 A QGIS plugin
 wyszukiwarka działek geodezyjnych w bazie Postgis (dane zaimportowane z pliku SWDE)
                              -------------------
        begin                : 2015-12-08
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Robert Dorna
        email                : robert.dorna@wp.eu
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4.QtSql import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from swdeszukaj_dialog import SWDESzukajDialog
import os.path
import subprocess, os, sys
import glob

class SWDESzukaj:
    """QGIS Plugin Implementation."""

    pguser =''
    pgbase = ''
    pguserpswd = ''
    pgserver = ''
    pgadmin = ''
    pgadminpswd = ''
    pgport = ''
    postgisQueryTmpPath = ''
    ogr2ogrfile = ''
    id_vLayer = ''

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SWDESzukaj_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SWDESzukajDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SWDE Szukaj')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SWDESzukaj')
        self.toolbar.setObjectName(u'SWDESzukaj')


        self.postgisQueryTmpPath = self.plugin_dir + "/tmp"
        self.dzemodel = QSqlQueryModel(self.dlg)
        self.cmbjew_model = QSqlQueryModel(self.dlg)
        self.cmbobr_model = QSqlQueryModel(self.dlg)


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SWDESzukaj', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToDatabaseMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SWDESzukaj/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'wyszukiwarka dzialek SWDE'),
            callback=self.run,
            parent=self.iface.mainWindow())

        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.pguser = sett.value('pguser', '', type=str)
        self.pgbase = sett.value('pgbase', '', type=str)
        self.pguserpswd = sett.value('pguserpswd', '', type=str)
        self.pgserver = sett.value('pgserver', '', type=str)
        self.pgport = sett.value('pgport', '5432', type=str)


        self.dlg.peditOut.appendPlainText("tmp : " +  self.postgisQueryTmpPath)
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setHostName(self.pgserver)
        db.setDatabaseName(self.pgbase)
        db.setUserName(self.pguser)
        db.setPassword(self.pguserpswd)
        ok = db.open()
        #self.model.setQuery("select * from g5jew")
        self.cmbjew_model.setQuery("select id_zd, g5naz from g5jew order by g5naz")
        self.dlg.cmbxJEW.setModel(self.cmbjew_model)
        self.dlg.cmbxJEW.setModelColumn(1)
        self.cmbobr_model.setQuery("select g5nro, g5naz from g5obr order by g5naz")
        self.dlg.cmbxOBR.setModel(self.cmbobr_model)
        self.dlg.cmbxOBR.setModelColumn(1)
        self.dlg.tabvDZE.setModel(self.dzemodel)
        #ostatecznie ponizsze sa ustawiane z poziomu qtdesignera
        #self.dlg.tabvDZE.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.dlg.tabvDZE.setSelectionMode(QAbstractItemView.SingleSelection)
        self.dlg.tabvDZE.setColumnHidden(0,True)


        QObject.connect(self.dlg.pbtnLokalizuj,SIGNAL("clicked()"),self.pbtnLokalizujClicked)
        QObject.connect(self.dlg.pbtnClose,SIGNAL("clicked()"),self.pbtnCloseClicked)
        QObject.connect(self.dlg.chckJEWfiltr,SIGNAL("clicked()"),self.chckJEWfiltrClicked)
        QObject.connect(self.dlg.tbtnObrRefresh,SIGNAL("clicked()"),self.tbtnObrRefreshClicked)
        QObject.connect(self.dlg.pbtnDzeSearch,SIGNAL("clicked()"),self.pbtnDzeSearchClicked)
        #QObject.connect(self.dlg.cmbxJEW,SIGNAL("currentIndexChanged(int)"),self.cmbxJEWIndexChanged(int))
        self.dlg.cmbxJEW.currentIndexChanged.connect(self.cmbxJEWIndexChanged)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&SWDE Szukaj'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
        
        #self.postgisQueryTmpPath = sett.value('tmppath', self.tmpPath, type=str)

        self.dlg.tabvDZE.show()
        # show the dialog
        self.dlg.show()

    def pbtnCloseClicked(self):
        self.dlg.close()

    def tbtnObrRefreshClicked(self):

        id_jew = self.cmbjew_model.data(self.cmbjew_model.index(self.dlg.cmbxJEW.currentIndex(),0))
        sqlstr = "select g5nro, g5naz from g5obr where id_zd = '" + id_jew + "' order by g5naz"
        self.cmbobr_model.setQuery(sqlstr)



    def chckJEWfiltrClicked(self):
        pass

    def pbtnDzeSearchClicked(self):
        nr_dze = self.dlg.leditDZE.text()
        sqlstr = u"SELECT tab_uid, g5dze.nr, (select g5naz from g5obr where g5nro = g5dze.id_zd || '.' ||g5dze.nrobr) as obręb, g5dze.g5pew, g5dze.g5idd, g5dze.id_zd, g5dze.nrobr FROM g5dze "
        if self.dlg.chckDzeDokladnie.isChecked():
            sqlstr += " where nr = '" + nr_dze + "' "
        else:
            sqlstr += " where nr like '" + nr_dze + "%' "
        sqlwhere = ""
        if self.dlg.chckJEWfiltr.isChecked():
            id_jew = self.cmbjew_model.data(self.cmbjew_model.index(self.dlg.cmbxJEW.currentIndex(),0))
            sqlwhere += " and id_zd = '" + id_jew + "' "
        if self.dlg.chckOBRfiltr.isChecked():
            id_obr = stringBetweenChar(self.cmbobr_model.data(self.cmbobr_model.index(self.dlg.cmbxOBR.currentIndex(),0)),".",1)
            if len(sqlwhere)>0:
                sqlwhere += " and "
            else:
                sqlwhere += " where "
            sqlwhere += "nrobr = '" + id_obr + "'"

        sqlstr+=sqlwhere
        self.dzemodel.setQuery(sqlstr)
        self.dlg.tabvDZE.setModel(self.dzemodel)
        self.dlg.tabvDZE.setColumnHidden(0,True)
        self.dlg.tabvDZE.show()

        self.dlg.peditOut.appendPlainText(sqlstr)


    def cmbxJEWIndexChanged(self):
        id_jew = self.cmbjew_model.data(self.cmbjew_model.index(self.dlg.cmbxJEW.currentIndex(),0))
        sqlstr = "select g5nro, g5naz from g5obr where id_zd = '" + id_jew + "' order by g5naz"
        self.cmbobr_model.setQuery(sqlstr)


    def pbtnLokalizujClicked(self):
        select = self.dlg.tabvDZE.selectionModel()
        sqlstr = "select g5idd, nr, tab_uid,  geom from g5dze where "
        wherestr = ""
        for sel in select.selectedRows():
            uid = sel.data(Qt.DisplayRole)
            if len(wherestr)== 0:
                wherestr = "tab_uid = '" + uid + "' "
            else:
                wherestr += " or tab_uid = '" + uid + "' "

        sqlstr += wherestr
        self.showVLayer(sqlstr)


#@brief executing the Query via pgsql2shp and adding the resulting shape to map canvas
#@param string query
#@return  none
#@author Dr. Horst Duester
#@date 10. March 2009
#@version 1.0
#@todo
    def showVLayer(self, query):
        sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
        self.id_vLayer = sett.value('id_vLayer', '', type=str)
        if len(self.id_vLayer) > 0:
            QgsMapLayerRegistry.instance().removeMapLayer(self.id_vLayer)
        tmpLayerDef = self.createShapeFileName(self.postgisQueryTmpPath)

        #tmpLayerDef = self.createShapeFileName("/home/robert/.qgis2/python/plugins/swdeszukaj/tmp/")
        file = tmpLayerDef[0]

        layerName = tmpLayerDef[1]

#  PG serverdefinintion holen
        dbName = self.pgbase
        dbUser = self.pguser
        dbHost = self.pgserver
        dbPort = self.pgport
        dbPasswd = self.pguserpswd
        query = query.replace('"','\\"')

        cmdHost = ""
        cmdUser = ""
        cmdPasswd = ""

        if len(dbHost) != 0:
            cmdHost = "-h "+dbHost
        if len(dbUser) != 0:
            cmdUser = "-u "+dbUser
        if len(dbPasswd) != 0:
            cmdPasswd = "-P "+dbPasswd
     

        osCmd = "ogr2ogr" + ' -f "ESRI Shapefile" ' + '"' + str(file) + '"' + ' PG:"host=' + dbHost+ ' port=' + dbPort +  ' user=' + dbUser + ' dbname=' + dbName + ' password=' + dbPasswd + ' " -sql ' + '"' +query+'"'
#     qmessageBox.information(None,'',osCmd)
        self.dlg.peditOut.appendPlainText( osCmd )
        self.dlg.peditOut.clear()
        proc = subprocess.Popen(osCmd.encode('utf-8'),
                           shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE
                           )
        stdout_value, stderr_value = proc.communicate()
        #self.dlg.txtOutput.setText(stdout_value+stderr_value)
        #usunięcie starej mapy    
        uri = file
        if len(self.id_vLayer) > 0:
            QgsMapLayerRegistry.instance().removeMapLayer(self.id_vLayer)

        vLayer = QgsVectorLayer(uri,  layerName,  "ogr")
        self.id_vLayer = vLayer.id()
        sett.setValue('id_vLayer', self.id_vLayer)
        canvas = self.iface.mapCanvas()
        #symbol = QgsMarkerSymbolV2.createSimple( { 'color' : '255,0,0' } )
        #vLayer.setRendererV2( QgsSingleSymbolRendererV2( symbol ) )
        #symbols = vLayer.rendererV2().symbols() 
	#symbol = symbols[0]
	#symbol.setFillColor(QColor.fromRgb(250,0,0)) 
        #rect = canvas.extent()
        #rect = vLayer.extent()
        canvas.setExtent(vLayer.extent()) 
        try:
            QgsMapLayerRegistry.instance().addMapLayer(vLayer)         
        except:
            QgsMapLayerRegistry.instance().addMapLayers([vLayer])
         
        pass
    
#@brief define the temporary shape file name
#@param String path to the temporary folder
#@return  tmpShapeName
#@author Dr. Horst Duester
#@date 10. March 2009
#@version 1.0
#@todo
    def createShapeFileName(self, myPath):
        myTempShape = str(myPath) + "/SwdeDzeSearchQuery.shp"
        mask = str(myPath) + "/SwdeDzeSearchQuery*"
        myTempLayer = "SwdeDzeSearchQuery" 
        
        filelist = glob.glob(mask)
        for f in filelist:
            os.remove(f)
        #usunięcie plików 
        #while os.path.isfile(unicode(myTempShape,'latin1')):
        #    myTempShape = str(myPath) + "querytmp" + str(i) + ".shp"
        #    myTempLayer = "querytmp" + str(i)
        
        myLayer = []   
        myLayer.append(myTempShape)
        myLayer.append(myTempLayer)
        print myTempShape 
        self.dlg.peditOut.appendPlainText(myTempShape)
        return myLayer

#==================================================================

def stringBetweenChar(string, char, nr):
    #wyszukuje lancuch znakow pomiedzy okreslonymi w char znakami
    #nr - okresla pomiedzy ktorym (pierwszym) wystapieniem znaku
    #a kolejnym znajduje sie szukany ciag. Jesli nr okresla ostatnie
    #wystapienie znaku char w string-u zostanie wyszukany ciag do konca
    #stringa
    char_pos = -1 #pozycja znaku w ciagu
    char_wyst = 0 # kolejne wystapienie char w ciagu
    char_nextpos = -1 # pozycja kolejnego wystapienia znaku w ciagu

    if nr == 0: #czyli od poczatku stringa do pierwszego znaku
        char_pos = 0
        i = 0
        for ch in string:
            if ch  == char:
                char_nextpos = i
                break
            i = i + 1
    else:
        i = 0
        for ch in string:
            if ch == char:
                char_wyst = char_wyst + 1
                if char_wyst == nr:
                    char_pos = i + 1
                elif char_wyst == nr+1:
                    char_nextpos = i
                    break
            i = i + 1

    if char_pos != -1: #czyli znaleziono znak
        if char_nextpos == -1: #czyli trzeba czytac do konca linii
            char_nextpos = len(string)
        return  string[char_pos:char_nextpos]
    else:
        return -1

