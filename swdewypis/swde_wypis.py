# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SWDEWypis
                                 A QGIS plugin
 przezentuje dane o działce geodezyjnej z bazy danych SWDE (Postgres) w formie zbliżonej do wypisu z rejestru gruntów 
                              -------------------
        begin                : 2015-11-13
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QPrintDialog, QFileDialog, QDialog, QMessageBox
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from swde_wypis_dialog import SWDEWypisDialog
import os.path
import time
from types import *

from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable


class SWDEWypis:
    """QGIS Plugin Implementation."""

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
            'SWDEWypis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = SWDEWypisDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&SWDE Wypis')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'SWDEWypis')
        self.toolbar.setObjectName(u'SWDEWypis')
        
        #dane dotyczace serwera odczytane z QSettings
        self.pguser =''
        self.pgbase = ''
        self.pguserpswd = ''
        self.pgserver = ''
        self.pgadmin = ''
        self.pgadminpswd = ''
        
        #zmienne do operacji wyboru kolejnej dzialki z zazanczonych
        self.actualSelect = 0

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
        return QCoreApplication.translate('SWDEWypis', message)


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

        icon_path = ':/plugins/SWDEWypis/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'SWDE Wypis'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        #------obsluga przyciskow ------------------
        QObject.connect(self.dlg.pbtnRefresh,SIGNAL("clicked()"),self.pbtnRefreshClicked)
        QObject.connect(self.dlg.pbtnPrint,SIGNAL("clicked()"),self.pbtnPrintClicked)
        QObject.connect(self.dlg.pbtnPrev,SIGNAL("clicked()"),self.pbtnPrevClicked)
        QObject.connect(self.dlg.pbtnNext,SIGNAL("clicked()"),self.pbtnNextClicked)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginDatabaseMenu(
                self.tr(u'&SWDE Wypis'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        
        layer = self.iface.activeLayer()  
        fields = layer.pendingFields()   
        field_names = [field.name() for field in fields]
        self.dlg.txtFeedback.clear()
         
        uid_dze = ""
        
        for f in layer.selectedFeatures():
            uid_dze =  f['tab_uid']
            break 
        
        if uid_dze == "":
            komunikat = u"<BR><BR><HR><H3>Nie wybrano żadnej warstwy, nie zaznaczono żadnego obiektu lub warstwa nie jest prawidłową warstwą działek ewidencyjnych</HR><H3>"
            self.dlg.txtFeedback.setText(komunikat)
        else:
            #dane dotyczace serwera odczytane z QSettings
            sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
            self.pguser = sett.value('pguser', '', type=str)
            self.pgbase = sett.value('pgbase', '', type=str)
            self.pguserpswd = sett.value('pguserpswd', '', type=str)
            self.pgserver = sett.value('pgserver', '', type=str)

            self.dlg.txtFeedback.setText( self.dzeInfo(uid_dze))

       
        
        
        self.dlg.show()
        
        
#===============================================================================
#         layer = self.iface.activeLayer()
#         provider = layer.dataProvider()
#         lname =  layer.name()
#         provname =  provider.name()
#         if layer and lname == 'g5dze' and provname == 'postgres' :
#             nF = layer.selectedFeatureCount()
#             fields = layer.pendingFields()
#             features = QgsFeature(fields)
#             #features = layer.selectedFeatures()
#             for f in features:
#                 map = f.attributeMap()
#             if nF == 1:
#                 provider = layer.dataProvider()
#                 uid_dze = map[provider.fieldNameIndex('tab_uid')].toString()
#                 #uid_dze  =  '040601_256126'
#                 #dane dotyczace serwera odczytane z QSettings
#                 sett = QSettings('erdeproj', 'SWDE_qgis_plugin')
#                 self.pguser = sett.value('pguser', '', type=str)
#                 self.pgbase = sett.value('pgbase', '', type=str)
#                 self.pguserpswd = sett.value('pguserpswd', '', type=str)
#                 self.pgserver = sett.value('pgserver', '', type=str)
# 
#                 self.dlg.setTextBrowser( self.dzeInfo(uid_dze))
#                 # show the dialog
#                 self.dlg.show()
#             else:
#                 QMessageBox.critical(self.iface.mainWindow(),"Error", u"Musisz wybrać dokładnie jedną działkę, użyj narzędzia: <<Wybierz jeden obiekt>>")
#         else:
#             QMessageBox.critical(self.iface.mainWindow(),"Error",u"Nie wybrano żadnej warstwy lub warstwa nie jest prawidłową warstwą g5dze")
#===============================================================================

        
    #=====================================================================================
    #===================obsluga zdarzen===================================================
    
    def pbtnPrintClicked(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.dlg.txtFeedback.document().print_(dialog.printer())
            
    #------------------------------------------------------------------------------------
    def pbtnRefreshClicked(self):
        
        layer = self.iface.activeLayer()  
        fields = layer.pendingFields()   
        field_names = [field.name() for field in fields] 
        uid_dze = ""
        for f in layer.selectedFeatures():
            uid_dze =  f['tab_uid']
            break

        if uid_dze == "":
            komunikat = u"<BR><BR><HR><H3>Nie wybrano żadnej warstwy, nie zaznaczono żadnego obiektu lub warstwa nie jest prawidłową warstwą działek ewidencyjnych</HR><H3>"
            self.dlg.txtFeedback.setText(komunikat)
        else:
            self.actualSelect=0
            self.dlg.txtFeedback.setText( self.dzeInfo(uid_dze))
    
    #-----------------------------------------------------------------------------------
    def pbtnPrevClicked(self):
        
        layer = self.iface.activeLayer()  
        fields = layer.pendingFields()   
        field_names = [field.name() for field in fields] 
        uid_dze = ""
        
        if self.actualSelect > 0:
            self.actualSelect-=1
        selFeatNr = 0
        for f in layer.selectedFeatures():
            if selFeatNr == self.actualSelect:
                uid_dze =  f['tab_uid']
                break   
            selFeatNr+=1
        
        
            

        self.dlg.txtFeedback.setText( self.dzeInfo(uid_dze))
        
    
    #-------------------------------------------------------------------------------------
    def pbtnNextClicked(self):
        
        layer = self.iface.activeLayer()  
        fields = layer.pendingFields()   
        field_names = [field.name() for field in fields] 
        uid_dze = ""
        
        selCount = layer.selectedFeatureCount()
        if self.actualSelect < (selCount - 1):
            self.actualSelect+=1
        selFeatNr = 0
        for f in layer.selectedFeatures():
            if selFeatNr == self.actualSelect:
                uid_dze =  f['tab_uid']
                break   
            selFeatNr+=1
        
        
            

        self.dlg.txtFeedback.setText( self.dzeInfo(uid_dze))
        
    #------------------------------------------------------------------------------------
    def dzeInfo(self, uid_dze):
        self.rdbase = RobDBBase(str(self.pgserver), str(self.pgbase), str(self.pguser), str(self.pguserpswd), 1)
        txt = ""

        #uni = lambda s: s if type(s) == unicode else unicode(s,'utf-8','replace')
        #powyzsza 
        ntype = lambda s: '' if type(s)==NoneType else s
        uni = lambda s: s if type(s) == unicode else unicode(ntype(s),'utf-8','replace')
        cols = ['g5idd', 'nr', 'id_zd', 'g5idr', 'g5nos', 'g5wrt', 'g5dwr', 'g5pew', 'g5rzn', 'g5dww', 'g5radr', 'g5rpwl', 'g5rpwd', 'g5rjdr', 'g5dtw', 'g5dtu', 'g5rkrg', 'g5id2', 'g5id1', 'nrobr', 'tab_uid']
        g5dzeT = RobDBTable(self.rdbase, 'g5dze', cols, 1, 1)
        g5dzeT.where(['tab_uid'], [str(uid_dze)] )

        txt = "<HR><H3>PODSTAWOWE INFORMACJE</H3><HR>"
        txt += "<b>IDD: </b>" + g5dzeT.get_col_value('g5idd') + "<br>"
        txt += u"<b>nr działki: </b>" + g5dzeT.get_col_value('nr') + "<br>"
        txt += "<b>Pow. ew: </b>" + str(g5dzeT.get_col_value('g5pew')) + " m2 <br>" 
        nr_obr = g5dzeT.get_col_value('nrobr')
        nr_jew = g5dzeT.get_col_value('id_zd')
        id_jdr = g5dzeT.get_col_value('g5rjdr')
	if id_jdr == None:
		id_jdr = '0'
        dze_id1 = g5dzeT.get_col_value('g5id1')
        id_zd = g5dzeT.get_col_value('id_zd')
        dze_uid = g5dzeT.get_col_value('tab_uid')
        dze_radr = g5dzeT.get_col_value('g5radr')
        dze_rpwl = g5dzeT.get_col_value('g5rpwl')
        dze_rpwd = g5dzeT.get_col_value('g5rpwd')

        cols = ['g5nro', 'g5naz']
        g5obrT = RobDBTable(self.rdbase, 'g5obr', cols, 1, 1)
        g5obrT.where(['g5nro'], [nr_jew + "." + nr_obr])
        txt += u"<b>Obręb:</b> " + uni(g5obrT.get_col_value('g5naz')) + "(" + g5obrT.get_col_value('g5nro')+ ")<br>"
        cols = ['g5idj', 'g5naz', 'plik_data']
        g5jewT = RobDBTable(self.rdbase, 'g5jew', cols, 1,1)
        g5jewT.where(['g5idj'], [nr_jew])
        txt += "<b>Jednostka ewidencyjna: </b>" + uni(g5jewT.get_col_value('g5naz')) + " (" + g5jewT.get_col_value('g5idj') + ")<br>"
        plik_data = uni(g5jewT.get_col_value('plik_data'))
        cols = ['g5id1', 'g5tjr', 'g5ijr', 'g5rgn']
        g5jdrT = RobDBTable(self.rdbase, 'g5jdr', cols, 1, 1)
        g5jdrT.where(['id_zd', 'g5id1'], [nr_jew, id_jdr])
        txt += "<b>Jednostka rejestrowa:</b>" + g5jdrT.get_col_value('g5ijr') + "<br><br>" 

        cols = ['g5ofu', 'g5ozu', 'g5ozk', 'g5pew']
        g5kluT = RobDBTable(self.rdbase, 'g5klu', cols, 1,1)
        g5kluT.where(['id_zd', 'g5rdze'], [nr_jew, dze_id1])
        txt  += u"<HR></HR><H3>UŻYTKI GRUNTOWE</H3><HR></HR>"
        txt += u'<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>OFU - sposób zagospodarowania</td><td>OZU - oznaczenie użytku </td><td>OZK - klasa bonitacyjna</td><td>Powierzchnia.</td></tr>'
        for row in g5kluT.rows:
            txt += '<tr bgcolor="#E6E6FA"><td>' + uni(row[0]) + "</td><td>" + uni(row[1]) + "</td><td>" + uni(row[2])+ "</td><td>" + str(row[3]) + "</td></tr>"
        txt += "</table>"



        cols = ['g5ud', 'g5rwls', 'g5rpod', 'rpod_rodzaj']
        g5udzT = RobDBTable(self.rdbase, 'g5udz', cols, 1, 1)
        g5udzT.where(['id_zd', 'g5rwls'], [nr_jew, id_jdr])

        txt  += u"<HR></HR><H3>WłAŚCICIEL</H3><HR></HR>"
        txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>Udzial</td><td>Rodz podmiotu</td><td>Podmiot</td><td>Adres</td></tr>'
        for row in g5udzT.rows:
            pod_id = row[2]
            pod_rodz = row[3]
            udz = row[0]
            
            cols = ['g5nzw', 'g5pim', 'g5dim', 'g5radr']
            g5osfT = RobDBTable(self.rdbase, 'g5osf', cols, 1, 1)

            
            if pod_rodz == "G5INS":
                cols = ['g5sti', 'g5npe', 'g5nsk', 'g5rgn', 'g5nip', 'g5radr']
                g5insT = RobDBTable(self.rdbase, 'g5ins', cols, 1, 1)
                g5insT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                npe = uni(g5insT.get_col_value('g5npe'))
                radr = g5insT.get_col_value('g5radr')
                if  not radr: # jesli radr jest typu None konieczne jest wstawienie jakiejkolwiek wartosci. W innym przypadku nie da się stworzyć pytania sql z uwagi na błąd łączenia string i None 
                    radr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, radr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = g5adrT.get_col_value('g5pcz')
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                adr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz 
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>INS</td><td>" + npe +  "</td><td>" + adr + "</td></tr>"

            elif pod_rodz == "G5OSF":
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                radr = g5osfT.get_col_value('g5radr')
                if  not radr:
                    radr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, radr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                adr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz 
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>OSF</td><td>" + uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim')) +  "</td><td>" + adr + "</td></tr>"

            elif pod_rodz == "G5MLZ":
                cols = ['g5rmaz', 'g5rzona']
                g5mlzT = RobDBTable(self.rdbase, 'g5mlz', cols, 1, 1)
                g5mlzT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rmaz')])
                
                mradr = g5osfT.get_col_value('g5radr')
                if  not mradr:
                    mradr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, mradr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                madr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz
                maz =  uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rzona')])
                zona = uni(g5osfT.get_col_value('g5nzw'))+ " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                zradr = g5osfT.get_col_value('g5radr')
                if  not zradr:
                    zradr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, zradr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                zadr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz

                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>MLZ</td><td>" + maz + ", " + zona + "</td><td>" + u"[mąż: " + madr + u"];[żona: " + zadr + "]</td></tr>"

        txt += "</table>"

        cols = ['g5ud', 'g5rwld', 'g5rpod', 'rpod_rodzaj', 'g5rwd']
        g5udwT = RobDBTable(self.rdbase, 'g5udw', cols, 1, 1)
        g5udwT.where(['id_zd', 'g5rwld'], [nr_jew, id_jdr])

        txt  += u"<HR></HR><H3>WŁADAJĄCY</H3><HR></HR>"
        txt += u'<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>Udzial</td><td>Rodz podmiotu</td><td>Podmiot</td><td>Adres</td><td>Rodzaj władania</td></tr>'
        rodz_wdtxt = ""
        for row in g5udwT.rows:
            #txt += row[0] + ' ' + row[1] + ' ' + row[2] + ' '  + row[3] + ' '  + row[4]
            pod_id = row[2]
            pod_rodz = row[3]
            udz = row[0]
            rodz_wd = row[4]
            
            if rodz_wd == '1':
                rodz_wdtxt = u'użytkowanie wieczyste'     
            if rodz_wd == '2':
                rodz_wdtxt = u'trwały zarząd lub zarząd'
            if rodz_wd == '3':
                rodz_wdtxt = u'wykonywanie prawa własności Skarbu Państwa i innych praw rzeczowych'
            if rodz_wd == '4':
                rodz_wdtxt = u'gospodarowanie zasobem nieruchomości Skarbu Państwa oraz gminnymi, powiatowymi i wojewódzkimi zasobami nieruchomości'
            if rodz_wd == '5':
                rodz_wdtxt = u'użytkowanie'
            if rodz_wd == '6':
                rodz_wdtxt = u'ułamkowa część własności nieobciążona prawami wymienionymi w pkt 1,2,5'
            
            cols = ['g5nzw', 'g5pim', 'g5dim']
            g5osfT = RobDBTable(self.rdbase, 'g5osf', cols, 1, 1)

            
            if pod_rodz == "G5INS":
                cols = ['g5sti', 'g5npe', 'g5nsk', 'g5rgn', 'g5nip', 'g5radr']
                g5insT = RobDBTable(self.rdbase, 'g5ins', cols, 1, 1)
                g5insT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                npe = uni(g5insT.get_col_value('g5npe'))
                radr = g5insT.get_col_value('g5radr')
                if  not radr: # jesli radr jest typu None konieczne jest wstawienie jakiejkolwiek wartosci. W innym przypadku nie da się stworzyć pytania sql z uwagi na błąd łączenia string i None 
                    radr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, radr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                adr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz 
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>INS</td><td>" + npe +  "</td><td>" + adr + "</td><td>" + rodz_wdtxt +  "</td></tr>"

            elif pod_rodz == "G5OSF":
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                radr = g5osfT.get_col_value('g5radr')
                if  not radr:
                    radr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, radr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                adr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz 
                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>OSF</td><td>" + uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim'))+ " "  + uni(g5osfT.get_col_value('g5dim')) +  "</td><td>" + adr + "</td><td>" + rodz_wdtxt +  "</td></tr>"

            elif pod_rodz == "G5MLZ":
                cols = ['g5rmaz', 'g5rzona']
                g5mlzT = RobDBTable(self.rdbase, 'g5mlz', cols, 1, 1)
                g5mlzT.where(['id_zd', 'g5id1'], [nr_jew, pod_id])
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rmaz')])
                mradr = g5osfT.get_col_value('g5radr')
                if  not mradr:
                    mradr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, mradr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                madr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz
                maz =  uni(g5osfT.get_col_value('g5nzw')) + " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                
                g5osfT.where(['id_zd', 'g5id1'], [nr_jew, g5mlzT.get_col_value('g5rzona')])
                zona = uni(g5osfT.get_col_value('g5nzw'))+ " " + uni(g5osfT.get_col_value('g5pim')) + " "  + uni(g5osfT.get_col_value('g5dim'))
                zradr = g5osfT.get_col_value('g5radr')
                if  not zradr:
                    zradr = '0'
                cols = ['g5ulc', 'g5nra', 'g5nrl', 'g5msc', 'g5kod', 'g5pcz']
                g5adrT = RobDBTable(self.rdbase, 'g5adr', cols, 1, 1)
                g5adrT.where(['id_zd', 'g5id1'], [nr_jew, zradr])
                ulc = uni(g5adrT.get_col_value('g5ulc'))
                nra = uni(g5adrT.get_col_value('g5nra'))
                nrl = uni(g5adrT.get_col_value('g5nrl'))
                if len(nrl) > 0:
                    nrl = '/'+ nrl
                msc = uni(g5adrT.get_col_value('g5msc'))
                kod = uni(g5adrT.get_col_value('g5kod'))
                pcz = uni(g5adrT.get_col_value('g5pcz'))
                zadr = ulc + ' ' + nra + nrl + ' ' + msc + ', ' + kod + ' ' + pcz

                txt += '<tr bgcolor="#E6E6FA"><td>' + udz + "</td><td>MLZ</td><td>" + maz + ", " + zona + "</td><td>" + maz + "," + zona + "</td><td>" + u"[mąż: " + madr + u"];[żona: " + zadr + "]</td><td>" + rodz_wdtxt +  "</td></tr>"

        txt += "</table>"

        #dokumenty rpwl
        SQLstr = "SELECT g5kdk, g5dtd, g5dtp, g5syg, g5nsr, g5opd FROM g5dok where tab_uid = any(array["
        res = None
        if dze_rpwl:
            for dok_id in dze_rpwl:
                SQLstr += "'" + nr_jew + dok_id + "',"
            SQLstr = SQLstr.rstrip(',')
            SQLstr += "]);"
            res = self.rdbase.executeSQL(SQLstr)

        if res:
            txt  += u"<HR></HR><H3>DOKUMENTY POWIĄZANE</H3><HR></HR>"
            txt += '<table><tr bgcolor="#BFBFBF" style="font-style: oblique;"><td>KDK</td><td>DTD</td><td>DTP</td><td>SYG</td><td>NSR</td><td>OPD</td></tr>'
            for row in res:
                txt += '<tr bgcolor="#E6E6FA"><td>' + uni(row[0]) + "</td><td>" + uni(row[1]) +"</td><td>" + uni(row[2]) + "</td><td>" + uni(row[3]) + "</td><td>" + uni(row[4])  + "</td></tr>"

            txt += "</table>"



        txt+= "<HR></HR><BR><RIGHT>" + time.strftime("%Y-%m-%d %H:%M:%S") + " (plik SWDE z dnia: " +  plik_data + ")</RIGHT>"
        return txt
    
