#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2

class RobDBBase():
    host = ""
    db = ""
    user = ""
    password = ""
    #cur = 0 #None - wyrzuca na windowsach błędy np self.conn = psycopg2.connect(...)
            # object type None nie posiada atrybutu connect , czy jakoś tak:
    #conn = 0 # j/w
    #ostatecznie trzeba było obie linie zakomentować z uwagi na błąd opisany dwie linie temu - pojawiał się w trakcie pracy wtyczki swdeDzeInfo
    rows = []
    row_count = 0


    def __init__(self, host, db, user, password, connect = 0):
        #print "connect w db = " + str(connect)
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        if connect == 1:
            self.connectdb()

    def connectdb(self):
        #print "uruchomiona connectdb"
        connstring = "host='" + self.host + "' dbname='" + self.db + "' user='" + self.user + "' password='" + self.password + "'"
        #print connstring
        self.conn = psycopg2.connect(connstring)
        self.cur = self.conn.cursor()
        return self.cur

    def commit(self):
        #TODO obsluga bledow
        self.conn.commit()

    def rollback(self):
        #TODO obsluga bledow
        self.conn.rollback()

    def executeSQL(self, SQLstr):# TODO sprawdzic co bedzie jak sql bedzie inne niz select - sprawdzone - ProgrammingError: no results to fetch
        print SQLstr
        self.cur.execute(SQLstr)
        #zeby uniknac 'ProgrammingError: no results to fetch' przy pytaniach innych niz select nalezy sprawdzic jaki jest typ zapytania
        if SQLstr.strip()[0:6].upper() == 'SELECT':
            rows = self.cur.fetchall()
            self.rows = []
            #normalnie odwołanie do row[nr] w instrukcji typu "for row in rows:" wywali błąd w przypadku row[nr] = None
            #poniższe zamiast None wstawi pusty ciąg znaków TODO - przetestować na liczbach
            for row in rows:
                nrow = []
                for i in range(len(row)):
                    if row[i] == None:
                        nrow.append('')
                    else:
                        nrow.append(row[i])
                self.rows.append(nrow)
            self.row_count = self.cur.rowcount
        else:
            self.rows = []
            self.row_count = 0

        return self.rows

class RobDBTable():

    table = ""          #nazwa tabeli z bazy
    col_list = ['*']    #lista kolumn, które będą wykorzystane w pytaniu SQL, muszą być podane przed połączeniem
                        #z bazą podobnie jak pozostałe parametry - domyslnie jest '*'
    id_nr = 0           #nr kolumny z col_list stanowiacej klucz glowny
    SQL = ""            #jesli zostanie puste - potraktowane to zostanie jak select * from tabela 
    cur = None          #cursor bazy pozyskiwany z RobDBBase.connectdb
    base = None         #obiekt RobDBBase
    colcount = 0
    rowcount = 0
    rows = ['']
    autocommit = 0
    autoexec = 0           #jeśli 1 - polecenie sql zostanie wywolane od razu po wywołaniu, jesli nie wymaga exec()

    def __init__(self, rbdbbase, table="", col_list=['*'], id_nr=0, connect = 0, autocommit = 0, autoexec = 0 ):
        #print "connect = " + str(connect)
        #print table
        #print col_list
        
        self.base = rbdbbase
        self.col_list = col_list
        self.id_nr = id_nr
        self.table = table
        if connect == 1:
            self.connectdb()
        self.autocommit = autocommit
        self.autoexec = autoexec

    def connectdb(self):
        #========================
        # łączy z bazą oraz ustawia i wypełnia tabelę na podstawie  parametrów self.rdbconn. Wyma uprzedniego ustawienia tych parametrów
        #=======================
        #+++++++++++++++++++++++
        #TODO !!!!! Obsługa błędów, na dzień dobry: puste parametry połączenia
        #++++++++++++++++++++++
        #TODO inicjalizacja rdbconn w wywołaniu funkcji albo w konstruktorze ??? czy w pythonie można przeciążać konstruktor i funkcje w ogóle ???
        #++++++++++++++++++++++
        self.cur = self.base.cur
        #ustawienie wielkości i wypełnienie tabeli - najpierw konieczne jest podanie nazwy tabeli do zmennej table
        #print "connect w table"
        if len(self.col_list) == 1 and self.col_list[0] == '*':
            #czyli wszystkie kolumny
            #print "wszystkie kolumny"
            SQLstr = "select column_name from information_schema.columns where table_name ='" + self.table + "';"
            self.cur.execute(SQLstr)
            colnames = self.cur.fetchall()
            self.col_count = self.cur.rowcount
            self.col_list = []
            for colname in colnames:
                self.col_list.append(colname[0])
        else:
            self.col_count = len(self.col_list)
            #print str(self.col_count)

        #utworzenie pytania SQL
        SQLstr = "select"
        for colname in self.col_list:
            #print colname
            if colname == self.col_list[0]:
                SQLstr = SQLstr + ' "' + colname + '"'
            else:
                SQLstr = SQLstr + ', "' + colname + '"'

        SQLstr = SQLstr + " from " + self.table
        #print "SQLstr = " + SQLstr
        self.SQL = SQLstr
        if self.autoexec == 1: #w przeciwnym przypadku czeka na wywolanie exec()
            self.cur.execute(SQLstr)
            self.rows = self.cur.fetchall()
            self.row_count = self.cur.rowcount

    def execute(self):
        self.cur.execute(self.SQL)
        self.rows = self.cur.fetchall()
        self.row_count = self.cur.rowcount

    def executeSQL(self, SQLstr):# TODO zastanowic sie nad przeniesieniem do RobDBBase , zeby uniezaleznic od table
        #dowolne pytanie - nie ma wplywu na self.SQL
        self.cur.execute(SQLstr)
        self.rows = self.cur.fetchall()
        self.row_count = self.cur.rowcount

    def first(self):
        self.cur.scroll(0, 'absolute')

    def next(self):
        try:
            self.cur.scroll(1, 'relative')
        except psycopg2.ProgrammingError:
            print "Proba dostepu do zmiennej spoza zakresu (+1)"

    def prev(self):
        try:
            self.cur.scroll(-1, 'relative')
        except psycopg2.ProgrammingError:
            print "Proba dostepu do zmiennej spoza zakresu (-1)"

    def last(self):
        self.cur.scroll(self.row_count - 1, 'absolute')

    def get_row(self, scroll=0):
        if scroll == 0:                 #domyslnie fetchone pobiera record i przesuwa kursor do nastepnego rekordu
            row = self.cur.fetchone()   #jesli chcemy dobrac sie do biezacego rekordu bez przesuwania trzeba ustawic
            try:
                self.cur.scroll(-1)         #parametr scroll= 0, nastapi wtedy cofniecie kursora po pobraniu wartosci
            except psycopg2.ProgrammingError:
                print "Proba dostepu do zmiennej spoza zakresu (-1)"
            return row
        else:
            return self.cur.fetchone()

    def get_row_nr(self, nr):
        self.cur.scroll(nr, 'absolute')
        row = self.cur.fetchone()
        try:
            self.cur.scroll(-1)         #parametr scroll= 0, nastapi wtedy cofniecie kursora po pobraniu wartosci
        except psycopg2.ProgrammingError:
            print "Proba dostepu do zmiennej spoza zakresu (-1)"
        return row

    def get_rownumber(self):
        return self.cur.rownumber


    def update(self, uid, update_cols_list, update_values_list):
        #TODO osluga wyjatkow
        sqlStr=  "update " +  self.table + " set "

        ilosc = len(update_cols_list)
        for i in range(0, ilosc):
            if i == 0:
                sqlStr = sqlStr + update_cols_list[i] + "='" + update_values_list[i]
            else:
                sqlStr = sqlStr + "', " +  update_cols_list[i] + "='" + update_values_list[i]
        sqlStr= sqlStr+ "' where "  + rdtable.get_id_name() + "='" +  str(uid) + "'"
        self.cur.execute(sqlStr)
        if self.autocommit == 1:
            self.base.commit()

    def update_where(self, update_cols_list, update_values_list, where_cols_list, where_values_list):
        #TODO osluga wyjatkow
        sqlStr=  "update " +  self.table + " set "

        ilosc = len(update_cols_list)
        znak = "='"
        znak2 = "' "
        for i in range(0, ilosc):
            if znak == "=":
                znak2 = ","
            elif znak == "='":
                znak2 = "', "
            if update_values_list[i][0:5] == "ARRAY":
                znak = "="
            else:
                znak = "='"

            if i == 0:
                sqlStr = sqlStr + update_cols_list[i] + znak + update_values_list[i]
            else:
                sqlStr = sqlStr + znak2 +  update_cols_list[i] + znak + update_values_list[i]


        if len(where_cols_list) == len(where_values_list):
            where_str = ""
            for i in range(0,len(where_cols_list)):
                if where_str == "":
                    where_str = where_str + '  "' + where_cols_list[i] + '" = ' + "'" + where_values_list[i] + "'" 
                else:
                    where_str = where_str + ' and  "' + where_cols_list[i] + '" = ' + "'" + where_values_list[i] + "'" 

        znak3 = ""
        if znak == "=":
            znak3 = ""
        else:
            znak3 = "'"
        sqlStr= sqlStr + znak3 + " where "  + where_str
        print sqlStr
        self.cur.execute(sqlStr)
        if self.autocommit == 1:
            self.base.commit()

    def get_id_name(self):
        return self.col_list[self.id_nr]

    def delete(self, did):
        sqlStr =  "delete from " + self.rdtable + " where " + rdtable.get_id_name + " ='" + str(did) + "'"
        self.cur.execute(sqlStr)

        if self.autocommit == 1:
            self.base.commit()

    def insert(self, uid, insert_cols_list, insert_values_list):
        sqlStr = "insert into " + self.table  + " ("
        ilosc = len(insert_cols_list)
        for i in range(0, ilosc):
            if i == 0:
                sqlStr = sqlStr + insert_cols_list[i]
            else:
                sqlStr = sqlStr + ", " + insert_cols_list[i]

        sqlStr = sqlStr + ") values ("
        for i in range (0, ilosc):
            if i in range(0, ilosc):
                #sprawdzenie czy wartość nie jest tablicą
                array = 0
                if insert_values_list[i][0:5] == "ARRAY":
                    array = 1
                #print "array = "+ str(array) + " " + insert_values_list[i][0:4]
                if i == 0:
                    if array == 1:
                        sqlStr = sqlStr  + insert_values_list[i]
                    else:
                        if insert_values_list[i][0:1] == "@":
                            sqlStr = sqlStr + str.lstrip(str(insert_values_list[i]),'@')
                            #jedna z dziwniejszych spraw - bez tego "str" w str(insert....)
                            #wywala sie - ale tylko w przypadku importu testowego dla g5jew i g5obr  (dla g5dze nie)
                            #mimo, ze pozostale rodzaje importu przechodza bez zastrzezen. błąd: lstrip 
                        else:
                            sqlStr = sqlStr + "'" + insert_values_list[i] + "'"
                else:
                    if array == 1:
                        sqlStr = sqlStr + ", " + insert_values_list[i] 
                    else:
                        if insert_values_list[i][0:1] == "@":
                            sqlStr = sqlStr + ", " + str.lstrip(str(insert_values_list[i]),'@')
                        else:
                            sqlStr = sqlStr + ", '" + insert_values_list[i] + "'"

        sqlStr = sqlStr + ")"
        #print "sqlStr = ", sqlStr
        self.cur.execute(sqlStr)
        if self.autocommit == 1:
            self.base.commit()

    def where(self, col_list, value_list): #najprostszy ale najczesciej wystepujacy where na swiecie typu "where col = value and ....." 
       #zapytanie zostanie wykonane natychmiast, bez względu na wartość self.autoexec 
        if len(col_list) == len(value_list):
            where_str = ""
            for i in range(0,len(col_list)):
                if where_str == "":
                    where_str = where_str + '  "' + col_list[i] + '" = ' + "'" + value_list[i] + "'" 
                else:
                    where_str = where_str + ' and  "' + col_list[i] + '" = ' + "'" + value_list[i] + "'" 


                
            SQLstr = self.SQL + " where " + where_str
            #print "SQLstr = " + SQLstr
            self.cur.execute(SQLstr)
            self.rows = self.cur.fetchall()
            self.row_count = self.cur.rowcount

    def get_col_value(self, colname):
        #TODO zabezpieczenie przed pustym row
        if len(self.rows) > 0:
            row = self.rows[0]
            col_nr = self.col_list.index(colname)
            return row[col_nr]
        else:
            return ""
