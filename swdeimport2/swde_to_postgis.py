#!/usr/bin/python
# -*- coding: utf-8 -*-


import pyproj
from rob_db_connection import RobDBBase
from rob_db_connection import RobDBTable
import sys
import datetime
import os
from dateutil import parser
from time import sleep, strftime
from asyncore import read

id_jed_rej = ""
ilosc_linii = 0
pzgdic = {}

def main():
    swde_file = str(sys.argv[1])
    #srid = str(sys.argv[2])
    print swde_file
    pzg_struct(swde_file)
    tablistString = sys.argv[2]
    srid = sys.argv[3]
    pyproj4strFrom = sys.argv[4]
    pyproj4strTo = sys.argv[5]
    rodz_importu = sys.argv[6]
    pgserver = sys.argv[7]
    pgbase = sys.argv[8]
    pguser = sys.argv[9]
    pguserpswd = sys.argv[10]
    txtcodec = sys.argv[11]
    id_zd = sys.argv[12]

    importuj(swde_file, tablistString, srid, pyproj4strFrom, pyproj4strTo, rodz_importu, pgserver, pgbase, pguser, pguserpswd, txtcodec, id_zd)
    
    #ponizsze tylkpo po to, zeby zatrzymac zewnetrzna konsole otwarta
    a = raw_input("wcisnij se entera")
    
    
    
#------------------------------------------------------------------------------------------------------#    
def pzg_struct(swde_file):
    
    ##wypelnienie struktury słownikowej z rozwinięciami punktów granicznych
    
    dic_idx = ""
    rp = 0
    global id_jed_rej
    global ilosc_linii #calkowita ilosc linii w pliku
    global pzgdic
    ile_lini_step = 0 #liczba linii w poszczególnym kroku - pomocne przy wyrzucaniu informacji o aktualnym
    #procesie postępu zadania
    step = 10000
    
    print "rozpoczynam prace: ", strftime("%Y-%m-%d %H:%M:%S")
    if swde_file != '':
        print "jeden"
        
        pgv = 0
    
        ilosc_pzg = 0
        
        #znaczniki dla zobrazowania pracy w konsoli
        znacznik = ["/","-","\\","|"]
        zn_nr = 0
        try:
            #self.f = open(str(self.swde_file.toUtf8()).decode('utf-8'), "r")
            f = open(swde_file, "r")
            print "plik otworzylem"
        
            try:
                for line in f.readlines():
                    ilosc_linii+=1
                    ile_lini_step+=1
                    if StringBetweenChar(line, ',', 0) == "NS" and StringBetweenChar(line, ',', 1) == "ZD":
                        id_jed_rej = StringBetweenChar(line, ',', 2)
                    pocz = StringBetweenChar(line, ',',0)
                    if pocz == "RP":
                        tab = StringBetweenChar(line, ',',2)
                        if tab == "G5PZG":
                            nr = StringBetweenChar(line, ',', 3)
                            rp = 1
                            dic_idx = nr
                    elif rp == 1:
                        y =StringBetweenChar(line, ',', 2)
                        x =StringBetweenChar(line, ',', 3)
                        dic_value = y +"," + x
                        pzgdic[nr] = dic_value
                        rp = 0
                        ilosc_pzg += 1
                    if ile_lini_step == step:  
                        #print znacznik[zn_nr], "trwa analiza PZG"
                        sys.stdout.write("\r analiza PZG: %s" % znacznik[zn_nr])
                        sys.stdout.flush()
                        sleep(0.01)
                        
                        if zn_nr == 3:
                            zn_nr = 0
                        else:    
                            zn_nr = zn_nr+1
                        ile_lini_step = 0


            finally:
                print "zakonczono"
                f.close()
                print "plik zamkniety"
                print "ilosc linii pliku:", str(ilosc_linii)
    
                print "ilosc puntkow zalamania granicy", str(ilosc_pzg)
                id_jed_rej = id_jed_rej.strip()
                if id_jed_rej !="":
                    print "Znaleziony identyfikator jednostki rejestrowej: ",  id_jed_rej,  u" zostanie wykorzystany  w bazie do stworzenia kluczy obiektów. Jeśli chcesz użyć innego możesz go zastąpić wpisanym przez siebie tekstem"
                else:
                    print u"Nie znaleziono identyfikatora jednostki rejestrowej - musisz samodzielnie określić identyfikator zbioru danych, wpisując samodzielnie - litery i cyfry - najlepiej do 10 znaków. Nie używaj polskich liter"

        except IOError:
            print u"IOError: błąd wczytania pliku swde"
            
           
    print u"ilość linii pliku:", str(ilosc_linii)
    
    print u"ilość puntków załamania granicy", str(ilosc_pzg)
    id_jed_rej = id_jed_rej.strip()
    if id_jed_rej !="":
        print "Znaleziony identyfikator jednostki rejestrowej: ",  id_jed_rej,  u" zostanie wykorzystany  w bazie do stworzenia kluczy obiektów. Jeśli chcesz użyć innego możesz go zastąpić wpisanym przez siebie tekstem"
    else:
        print u"Nie znaleziono identyfikatora jednostki rejestrowej - musisz samodzielnie określić identyfikator zbioru danych, wpisując samodzielnie - litery i cyfry - najlepiej do 10 znaków. Nie używaj polskich liter"

#-------------------------------------------------------------------------------------------------------#
def importuj(swde_file, tableListString, srid, pyproj4strFrom, pyproj4strTo, rodz_importu, pgserver, pgbase, pguser, pguserpswd,  txtcodec, id_zd):
    
    global id_jed_rej
    global ilosc_linii
    global pzgdic
    
    tableList = [] #tabela nazw tabel w bazie
    tableList = tableListString.split(',')
    
    import_testowy = False
    if rodz_importu == 'testowyJEW' or rodz_importu == 'testowyOBR' or rodz_importu == 'testowyDZE':
        import_testowy = True
    
    for tabName in tableList:
        if tabName <> 'NONE':
            print tabName
    print srid
    print pyproj4strFrom
    print pyproj4strTo
    print "identyfikator jednostki rejestrowej:", id_jed_rej
    print "ilość linii", ilosc_linii
    print "rodzaj importu", rodz_importu
    print pgserver, pgbase, pguser, pguserpswd
    
    
    uni = lambda s: s if type(s) == unicode else unicode(s,'utf-8','replace')
    
    try:
        f = open(swde_file, "r")
        if f == 0 or f.closed:
            print u"Przed rozpoczęciem importu musisz wczytać plik"
        else:
            if id_zd == 'NONE': #parametr wybierany przez uzytkownika, jesli jest inny niz NONE
                id_jed_rej  = str(id_jed_rej).rstrip() #zostanie uzyty jako wymuszenie nazwy zbioru danych
            else:                       #w innym przypadku uzyta zostanie nazwa jednostki rej wyłuskana przez program
                id_jed_rej = id_zd
            
                
                
     
            
            #lista column tablicowych - do innej obróbki niż pozostałe
            arrayCols = ['G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RSKD', 'G5RDOK', 'G5RDZE', 'G5ROBJ']
            #słownik kolumn do zmiany nazwy - zmieniamy polskie znaki w nazwie kolumn bo trochę to broi przy pytaniach SQL
            plcharCols =  {u'G5RŻONA':'G5RZONA', u'G5RMĄŻ':'G5RMAZ', u'G5RPWŁ':'G5RPWL', u'G5RWŁ':'G5RWL', u'G5RWŁS':'G5RWLS', u'G5RWŁD':'G5RWLD'}
            g5Cols = {} #słownik zbudowany: {'nazwa_tabeli':Tablica_Column[]} - posluzy do inicjacji tabel - obiektow robdbtable 
            #inicjalizacja  bazy danych
            rdbase = RobDBBase(pgserver, pgbase, pguser, pguserpswd,1)
            rdg5Table = {}  #słownik zawiera następującą strukturę: {'nazwa_tabeli': Obiekt_rdbtable}
            
            #okreslenie rodzaju importu
            
            if rodz_importu == 'zwykly' or rodz_importu == 'aktualizacja':
                Cols = ['G5IDJ', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU','G5RKRG']#g5jew
                g5Cols['G5JEW'] = Cols
                Cols = [ 'G5IDD',  'GEOM',    'NR', 'G5IDR', 'G5NOS', 'G5WRT', 'G5DWR', 'G5PEW', 'G5RZN', 'G5DWW', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR', 'G5DTW', 'G5DTU'] #g5dze
                g5Cols['G5DZE'] = Cols
                Cols = [ 'G5NRO', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU', 'G5RKRG', 'G5RJEW', 'IDJEW'] #g5obr
                g5Cols['G5OBR'] = Cols
                Cols = ['G5PLC', 'G5PSL', 'G5NIP', 'G5NZW', 'G5PIM', 'G5DIM', 'G5OIM', 'G5MIM', 'G5OBL', 'G5DOS', 'G5RADR', 'G5STI', 'G5DTW', 'G5DTU'] #g5osf
                g5Cols['G5OSF'] = Cols
                Cols = [ 'G5STI', 'G5NPE', 'G5NSK', 'G5RGN', 'G5NIP', 'G5NZR', 'G5NRR', 'G5NSR', 'G5RADR', 'G5DTW', 'G5DTU'] #g5ins
                g5Cols['G5INS'] = Cols
                Cols = ['G5RZONA',  'G5RMAZ', 'G5DTW', 'G5DTU'] #g5mlz
                g5Cols['G5MLZ'] = Cols
                Cols = [ 'G5STI', 'G5NPE', 'G5NSK', 'G5RGN', 'G5NIP', 'G5RSKD', 'G5RADR', 'G5DTW', 'G5DTU'] #g5osz
                g5Cols['G5OSZ'] = Cols
                Cols = ['G5TJR', 'G5IJR', 'G5RGN', 'G5RWL', 'G5RWLS', 'G5RWLD', 'G5ROBR', 'G5DTW', 'G5DTU' ] #g5jdr
                g5Cols['G5JDR'] = Cols
                Cols = [ 'G5UD', 'G5RWLS', 'G5RPOD', 'G5DTW', 'G5DTU'] #g5udz
                g5Cols['G5UDZ'] = Cols
                Cols = [ 'G5RWD', 'G5UD', 'G5RWLD', 'G5RPOD', 'G5DTW', 'G5DTU'] #g5udw
                g5Cols['G5UDW'] = Cols
                Cols = [ 'G5OFU', 'G5OZU', 'G5OZK', 'G5PEW', 'G5RDZE', 'G5DTW', 'G5DTU'] #g5klu
                g5Cols['G5KLU'] = Cols
                Cols = [ 'G5IDT', 'G5OZU','G5OFU', 'G5PEW', 'G5RKRG', 'G5ROBR', 'G5DTW', 'G5DTU'] #g5uzg
                g5Cols['G5UZG'] = Cols
                Cols = ['G5KDK', 'G5DTD', 'G5DTP', 'G5SYG', 'G5NSR', 'G5OPD', 'G5RDOK', 'G5DTW', 'G5DTU'] #g5dok
                g5Cols['G5DOK'] = Cols
                Cols = ['G5TAR', 'G5NAZ', 'G5KRJ', 'G5WJD', 'G5PWJ', 'G5GMN', 'G5ULC', 'G5NRA', 'G5NRL', 'G5MSC', 'G5KOD', 'G5PCZ', 'G5DTW', 'G5DTU']#g5adr
                g5Cols['G5ADR'] = Cols
                Cols = ['G5IDB', 'G5FUZ', 'G5WRT', 'G5DWR', 'G5RBB', 'G5PEW', 'G5PEU', 'G5RZN', 'G5SCN', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR','G5RDZE', 'G5DTU', 'G5DTW']#g5bud
                g5Cols['G5BUD'] = Cols
                Cols = ['G5IDK', 'G5OZU', 'G5OZK', 'G5PEW', 'G5RKRG', 'G5ROBR', 'G5DTW', 'G5DTU']
                g5Cols['G5KKL'] = Cols
                Cols = ['G5IDL', 'G5TLOK', 'G5PEW', 'G5PPP', 'G5LIZ', 'G5WRT', 'G5DWR', 'G5RJDR', 'G5RADR', 'G5RDOK', 'G5RBUD', 'G5DTW', 'G5DTU']
                g5Cols['G5LKL'] = Cols
                Cols = ['G5NRZ', 'G5STZ', 'G5DZZ', 'G5DTA', 'G5DTZ', 'G5NAZ', 'G5ROBJ', 'G5RDOK', 'G5DTW', 'G5DTU']
                g5Cols['G5ZMN'] = Cols
     
     
     
            elif rodz_importu == 'testowyJEW' or rodz_importu == 'testowyOBR' or rodz_importu == 'testowyDZE':
                #teoretycznie powinno wystarczyć zwykle elif bez parametrow, ale na wszelki dorzuce te ory
                #w przypadku importu testowego importować będziemy tylko jedną z trzech tabel (dze, obr, lub jew)
                # przy okazji opróżnimy zawartość dotychczasowych tabel testowych
                delSQLstr = "delete from "
                if rodz_importu == 'testowyJEW':
                    tableList.append('G5JEW')
                    g5Cols['G5JEW'] = ['G5IDJ', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU','G5RKRG']#g5jew
                    delSQLstr += "g5jew_test;"
                elif rodz_importu == 'testowyOBR':
                    tableList.append('G5OBR')
                    g5Cols['G5OBR'] = [ 'G5NRO', 'G5PEW', 'G5NAZ', 'G5DTW', 'G5DTU', 'G5RKRG', 'G5RJEW', 'IDJEW']
                    delSQLstr += "g5obr_test;"
                elif rodz_importu == 'testowyDZE':
                    tableList.append('G5DZE')
                    g5Cols['G5DZE'] = [ 'G5IDD',  'GEOM',    'NR', 'G5IDR', 'G5NOS', 'G5WRT', 'G5DWR', 'G5PEW', 'G5RZN', 'G5DWW', 'G5RADR', 'G5RPWL', 'G5RPWD', 'G5RKRG', 'G5RJDR', 'G5DTW', 'G5DTU']
                    delSQLstr += "g5dze_test;"
     
                rdbase.executeSQL(delSQLstr)
     
     
            #nazwy kolumn muszą zostać podane dokładnie jak w bazie - czyli małymi literami
            #na przyszłość można to rozwiązać w samej RobDBTable
            #za zamianę liter na małe w tablicy odpowiada ta fikuśna konstrukcja: [x.lower() ....]
            for tableName in tableList:
                if import_testowy:
                    appendix = '_TEST'
                else:
                    appendix = ''
                rdg5Table[tableName] = RobDBTable(rdbase, tableName + appendix, [x.lower() for x in g5Cols[tableName]], 1, 1)
     
            G5Table = ""
     
            collist = []
            valuelist = []
            insertdic = {} # forma [nazwa_tabeli:ilosc_insertow] 
            arraylist = [] #wykorzystywana do przechowywania kolumn typu tablicaowego w formie [[col2, wart..], [col1, wart..], [col2, wart..]]
            arrayvalue = [] # wykorzystywane do przechowywania danych 1+ takich jak g5rkrg
            arrayname = '' # nazwa tablicy tożsama z nazwą kolumny w bazie
            pointslist = []
            point = []
            Kznak = ""  #znacznik + albo -, oznaczajacy czy okreslane sa punkty tworzace polygon czy
                        #wycinajace w nim dziure
            oldKznak = "0" #posluzy do sprawdzenia czy nastapila zmiana Kznak
            newPoly = 0
            polycount = 0
     
        
            linianr = 0     #przyda sie w momencie gdy sie program wywali - okresli ktora linia pliku swde nabroiła
            obieg = 0       #bedzie wykorzystywane przy commit do bazy, ktore bedzie realizowane co np 100 pytań SQL
            
            transform = False
            if import_testowy == False: #tylko jesli nie jest to import testowy
                if pyproj4strFrom != pyproj4strTo:
                    transform = True
            print "transform:", transform
       
     
            print "Krok 2. Start programu: ", strftime("%Y-%m-%d %H:%M:%S")
     
     
            if rodz_importu == 'aktualizacja':
                #usuniecie wszystkich rekordow o id_zd
                print u"Usuwanie rekordów ze zbioru danych o id =  ", id_jed_rej
                #naprawde dziwna sprawa, ale bez tego dwukrotnie powtorzonego slepp-applicationevent 
                
                print u"Rozpoczęcie usuwania aktualizowanych rekordów: ",  strftime("%Y-%m-%d %H:%M:%S")
                rdbase.executeSQL("SELECT g5sp_delfromtables('" + id_jed_rej + "');")
                print u"Zakończono usuwanie aktualizowanych rekordów: ",  strftime("%Y-%m-%d %H:%M:%S")
            #import_file = str(self.swde_file.toUtf8()).decode('utf-8')
     
            try:
                #self.f = open(self.swde_file "r")
                f.seek(0.0)
                tekstline = ""
                try:
                    print u"Krok 3. Rozpoczynam import pliku: ",  f.name, " ",strftime("%Y-%m-%d %H:%M:%S")
                    i = 0;
                    procent_wykonania = 0; #do monitorowania postepu
                    linianr = 0
                    step = ilosc_linii/100
                    
                    print u'ilość linii:',ilosc_linii, "step", step
                    
                    for line in f.readlines():
                        tekstline = line #zmienna tekstline bedzie wykorzystywana poza petla w celu lokalizacji bledu - w exception
                        if i == step:
                            i = 0
                            procent_wykonania += 1
                            sys.stdout.write("\r wykonano: %d%s" % (procent_wykonania, "%"))
                            sys.stdout.flush()
                            sleep(0.01)
                            #print u"postęp:", procent_wykonania, u"%"
                        
                        line = unicode(line, txtcodec)
                        #print "unikod zadzialal"
                        i= i + 1
                        linianr+=1 #przyda sie jak sie program wypierniczy
     
                        pocz = StringBetweenChar(line, ',',0)
     
                        if pocz == "RO" or pocz == "RD" or pocz == "RC":
                            #line = unicode(line, txtcodec)
                            G5Table =  StringBetweenChar(line, ',',2)
                            g5id1_value = StringBetweenChar(line,',',3)
                            g5id2_value = StringBetweenChar(line,',',4)
                        if line[0:3] == "P,P":
                            #self.dlg.peditOutput.appendPlainText(u"znaleziono ciąg line 0:3 = P,P")
                            str1 =  StringBetweenChar(line, ',', 2)
                            #self.dlg.peditOutput.appendPlainText(u"str1 = " + str1 + u" o długości " + str(len(str1)) )
                            if str1 == u"G5PZG":
                                #self.dlg.peditOutput.appendPlainText(u"wlazło")
                                nr =  StringBetweenChar(line, ',', 3)
                                #self.dlg.peditOutput.appendPlainText(u"nr = " + nr)
                                #strnr = nr.rstrip(';\r')# trzeba usuwac pojedynczo czyli tak jak poniżej
                                strnr = nr.rstrip()# czyli jakiekolwiek białe znaki niezaleznie czy \n \r itp
                                strnr = strnr.rstrip(';')
                                #self.dlg.peditOutput.appendPlainText(u"strnr = " + strnr)
                                #oldline = line
                                #self.dlg.peditOutput.appendPlainText(u"oldline = " + oldline)
                                line = "P,G," + pzgdic[strnr] + ",;\n"
                                #self.dlg.peditOutput.appendPlainText(u"line = " + line)
                                #self.dlg.peditOutput.appendPlainText(u"Zastąpiono ciąg P,P >>" + oldline + "<< na >>" + line + "<< " + strftime("%Y-%m-%d %H:%M:%S"))
     

                        if G5Table in tableList:
                            colname = ""
                            colvalue = ""
                            znacznik = StringBetweenChar(line, ',',0)
                            if znacznik == "D" or znacznik == "WG":
                                line = line.rstrip()
                                line = line.rstrip(';') # szczególnie linie ze znacznikami WG zakończone są średnikiem 
                                line = line.strip("'")
                                line = line.strip('"')
                                line = line.replace("'", '')
                                line = line.replace('"', "")
                                colname = StringBetweenChar(line,',',1)
                                #zamiana nazw kolumn z polskimi znakami
                                if colname in plcharCols:
                                    colname = plcharCols[colname] 
                                colvalue = StringBetweenChar(line,',',3)
                                #dzialania wspolne dla wszystkich tablic
                                if colname in g5Cols[G5Table]:
                                    #G5RDZE w G5KLU nie jest typu tablicowego, natomiast w g5BUD
                                    #jest. Na szczescie w g5klu nie ma żadnego pola tablicowego
                                    #to samo dotyczy g5radr - w g5osf i g5ins - nie jest array w przeciwienstwie do g5bud
                                    if colname in arrayCols and G5Table != 'G5KLU' and G5Table != 'G5INS' and G5Table != 'G5OSF':
                                        arraylist.append([colname,colvalue])
     
                                    else:
                                        collist.append(colname)
                                        valuelist.append(colvalue)
     
                                    #dzialania nietypowe
                                    #TODO przewidziec dla g5obr wyluskanie numeru obrebu do osobnego pola
                                    if colname == 'G5IDD' and G5Table == "G5DZE": #trzeba wyluskac numer dzialki i zapisac do oddzielnej kolumny
                                        #nr_dzialki = StringBetweenChar(colvalue, '.', 2)
                                        collist.append(u'nr')
                                        valuelist.append(StringBetweenChar(colvalue, '.', 2))
                                        #nr obrębu też się przyda
                                        collist.append(u'nrobr')
                                        valuelist.append(StringBetweenChar(colvalue, '.', 1))
     
     
                                    if colname == 'G5RPOD': #dla tabel g5udz i g5udw - wyglada to nastepujaco: "WG,G5RPOD,G5OSF,5465;"
                                                            #a więc najpierw mamy określenie do jakiej tabeli jest dowiązanie (osf, ins, mlz czy osz)
                                                            #a potem wartość wiązania w danej tabeli. Należy więc jeszcze wyciągnąć wartość po drugim ','
                                        collist.append(u'rpod_rodzaj')
                                        pod_rodzaj = StringBetweenChar(line, ',', 2)
                                        valuelist.append(pod_rodzaj)
                                        #kolumna zawierajaca polaczone ze soba wartosci 
                                        collist.append(u'id_podmiot')
                                        valuelist.append(colvalue + pod_rodzaj)
                                 
     
                            elif znacznik == "K":
                                Kznak = StringBetweenChar(line, ',',1)#czyli albo '+;' albo '-;'
                                Kznak = Kznak[0]#pozostawienie tylko + albo -
                                newPoly = 1
                                polycount+=1
                                
                            elif znacznik == "P":
                                yvalue = StringBetweenChar(line, ',',2)
                                xvalue = StringBetweenChar(line, ',',3)
                                #print "xv:", xvalue, "yv:", yvalue
                                if transform:
                                    #print "transformacja"
                                    #p1 = pyproj.Proj(pyproj4strFrom)
                                    #p2 = pyproj.Proj(pyproj4strTo)
                                    p1 = pyproj.Proj(str(pyproj4strFrom))
                                    p2 = pyproj.Proj(str(pyproj4strTo))
                                    x92, y92 = pyproj.transform(p1,p2,xvalue,yvalue)
                                    value = str(x92) + " " + str(y92)
                                else:
                                    value = xvalue + " " + yvalue
                                point.append( polycount)
                                point.append(newPoly)
                                point.append(Kznak)
                                point.append(value) 
                                pointslist.append(point)
                                #print point
                                point = []
                                newPoly = 0
     
                            elif znacznik[0] == "X": #czyli koniec definicji recordu
                                #print "2 line", line
                                #print "2 znacznik = ", znacznik, collist, valuelist
                                p = ""
                                p1 = ""
                                if len(pointslist)>0:
                                    for points in pointslist:
                                        if points[1] == 1:#newPoly
                                            #p1 = points[3]
                                            if points[0] == 1:#czyli pierwszy i byc moze jedyny polygon
                                                if srid == -1: #niezdefiniowany układ
                                                    p = "POLYGON(("
                                                else:
                                                    p = "@ST_GeomFromText(\'POLYGON(("
                                            else: #czyli ewentualne kolejne polygony
                                                p = p + p1 + "),("
                                            p1 = points[3]
                                        p = p + points[3] + ','
                                    if srid == -1:
                                        p = p + p1 + "))"
                                    else:
                                        p = p + p1 + "))\'," + srid + ")"
                                    collist.append("geom")
                                    valuelist.append(p)
     
                                #dodanie kolumn tablicowych
                                if len(arraylist) > 0:
                                    old_col = ''
                                    arraystr = "ARRAY["
                                    arraylist.sort()
                                    for col, val in arraylist:
                                        if old_col == '': #startujemy
                                            old_col = col
                                        if  col == old_col:
                                            arraystr += "\'"+ val + "\',"
                                        else: #nastąpiła zmiana columny
                                            arraystr = arraystr.rstrip(",")
                                            arraystr += "]"
                                            collist.append(old_col)
                                            valuelist.append(arraystr)
                                            old_col = col
                                            arraystr = "ARRAY[\'" + val + "\',"
                                    collist.append(old_col)
                                    arraystr = arraystr.rstrip(",")
                                    arraystr += ']'
                                    valuelist.append(arraystr)
                                    arraylist = []
     
                                #dodatnie id_jed_rej do kazdej tabeli
                                collist.append("id_zd")
                                valuelist.append(id_jed_rej)
                                #dodanie id1 i id2 do kazdej z tabel
                                collist.append("g5id1")
                                valuelist.append(g5id1_value)
                                collist.append("g5id2")
                                valuelist.append(g5id2_value)
                                #dodanie unikatowej kolumny - będzie stanowiła klucz główny w całej bazie
                                collist.append('tab_uid')
                                valuelist.append(id_jed_rej+g5id1_value)
     
     
                                #sprawdzenie czy jest jeszcze jakas tablica, ktora nie zostala dodana do valuelist
                                if len(arrayvalue)>0:
                                    collist.append(arrayname)
                                    values = ""
                                    for value in arrayvalue:
                                        values += "\'" + value.strip('[]') + "\',"
                                    values = values.rstrip(",")#usuniecie ostatniego przecinka
                                    valuelist.append(u"ARRAY[" + values + "]")
                                    arrayname = ''
                                    arrayvalue = []
     
                                rdg5Table[G5Table].insert(0, collist, valuelist)
                                if G5Table in insertdic:
                                    insertdic[G5Table] += 1
                                else:
                                    insertdic[G5Table] = 1
     
                                #obieg+=1
                                #if obieg == 1000:
                                #    rdbase.commit()
                                #    obieg = 0
                                obieg+=1
                                collist = []
                                valuelist = []
                                pointslist = []
                                Kznak = ""
                                polycount = 0
                                G5Table = ""
     
                                if rodz_importu == 'testowyJEW':
                                    #w tym przypadku nie ma co dalej ciągnąć pętli
                                    break
                        #i = i+1
                except Exception, ex:
                    cols = "["
                    values = "["
                    for col in collist:
                        cols +=  col + ", "
                    for value in valuelist:
                        values += value + ", "
                    cols += "]"
                    values += "]"
                    print u"błąd: ", uni(G5Table),  uni(cols), uni(values), "rekord nr: ", uni(str(obieg)), "line = ",  uni(tekstline), "error: ",uni(str(ex))
                    #przerwanie = 1
     
                finally:
                    
                    rdbase.commit()
                    print "wykonano commita"
                    insstr = ""
                    for tab, ilosc in insertdic.items():
                        insstr += tab + ':' + str(ilosc) + '; '
                        print "tab:", tab
                    print "zapisano do bazy: ",str(obieg), u" rekordów: ", insstr
                         
                
                    f.close()
             
            except IOError:
                print "IOError: ",  strftime("%Y-%m-%d %H:%M:%S")
     
            print "przerobiono lini: ",  str(linianr)
            print "Koniec programu: ",  strftime("%Y-%m-%d %H:%M:%S")
    
    except IOError:
                print "IOError: ",  strftime("%Y-%m-%d %H:%M:%S")        

#--------------------------------------------------------------------------------------------------------#
def StringBetweenChar(string, char, nr):
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
    
#--------------------------------------------------------------------------------------------------------#    
    

main()

