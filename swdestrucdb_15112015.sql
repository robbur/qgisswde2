-- Table: g5adr

-- DROP TABLE g5adr;

CREATE TABLE g5adr
(
  tab_uid character varying(50) NOT NULL, -- Adres obiektu
  g5tar character(1), -- typ adresu 1 - adres, 2 - nazwa własna
  g5naz character varying(150),
  g5krj character varying(100), -- kraj
  g5wjd character varying(100), -- województwo
  g5pwj character varying(100), -- powiat, miasto
  g5gmn character varying(100), -- gmina
  g5ulc character varying(255), -- ulica
  g5nra character varying(50), -- numer porzadkowy domu - niestety muszę zarezerwować 50 znakow poniewaz zdazylo sie ze to pole było wykorzystywanie jako komentaż
  g5nrl character varying(50), -- nr lokalu - uwagi jak do g5nra
  g5msc character varying(100), -- Miejscowośc
  g5kod character varying(50), -- kod pocztowy - początkowo miałem 7 znaków, ale trafiłem na jakieś długasy - zagraniczne kody
  g5pcz character varying(100), -- poczta
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(50) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5adr_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5adr
  OWNER TO biuro;
COMMENT ON TABLE g5adr
  IS 'Adres obiektu';
COMMENT ON COLUMN g5adr.tab_uid IS 'Adres obiektu';
COMMENT ON COLUMN g5adr.g5tar IS 'typ adresu 1 - adres, 2 - nazwa własna';
COMMENT ON COLUMN g5adr.g5krj IS 'kraj';
COMMENT ON COLUMN g5adr.g5wjd IS 'województwo';
COMMENT ON COLUMN g5adr.g5pwj IS 'powiat, miasto';
COMMENT ON COLUMN g5adr.g5gmn IS 'gmina';
COMMENT ON COLUMN g5adr.g5ulc IS 'ulica';
COMMENT ON COLUMN g5adr.g5nra IS 'numer porzadkowy domu - niestety muszę zarezerwować 50 znakow poniewaz zdazylo sie ze to pole było wykorzystywanie jako komentaż';
COMMENT ON COLUMN g5adr.g5nrl IS 'nr lokalu - uwagi jak do g5nra';
COMMENT ON COLUMN g5adr.g5msc IS 'Miejscowośc ';
COMMENT ON COLUMN g5adr.g5kod IS 'kod pocztowy - początkowo miałem 7 znaków, ale trafiłem na jakieś długasy - zagraniczne kody
';
COMMENT ON COLUMN g5adr.g5pcz IS 'poczta';
COMMENT ON COLUMN g5adr.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5adr.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5adr.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5adr.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5adr.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';

-- Table: g5bud

-- DROP TABLE g5bud;

CREATE TABLE g5bud
(
  tab_uid character varying(50) NOT NULL,
  g5idb character varying(50), -- identyfikator budynku
  g5fuz character varying(2), -- kod funkcji użytkowej.1 -mieszkalne,2 -przemysłowe,3 -transportu i łączności,4 -handlowo-usługowe,5 -zbiorniki, silosy i budynki magazynowe,6 -biurowe,7 -szpitale i zakłady opieki medycznej, 8 -oświaty, nauki i kultury oraz budynki sportowe, 9 - produkcyjne, usługowe i gospodarcze dla rolnictwa,10 -inne niemieszkalne
  g5wrt numeric, -- wartość w zł
  g5dwr character varying(20), -- data wyceny
  g5rbb integer, -- rok zakończenia budowy
  g5pew integer, -- pole powierzchni zabudowy w m2 do 1m2
  g5peu integer, -- łączne pole powierzchni  powierzchni użytkowej lokali w budynku wraz z pomieszczeniami przynależnymi do lokali w m2
  g5rzn character varying(50), -- numer rejestru zabytków
  g5scn character(1), -- materiał ścian zewnętrznych - 1 mur, 2 drewno, 3 inne
  g5radr character varying(50)[], -- adres(y) - budynek może mieć wiele adresów i nazw - relacja 0+
  g5rpwl character varying(50)[], -- podstawa własności - dokument - Dotyczy budynków stanowiących odrębny od gruntu przedmiot własności (JR typu 2)- relacja 0+
  g5rpwd character varying(50)[], -- Podstawa innych praw do budynku. Dokument. relacja 0+
  g5rkrg character varying(50)[], -- Źródło danych o położeniu, dokument - operat geodezyjny - relacja 1+
  g5rjdr character varying(50), -- Niepuste. Jednostka rejestrowa może być typu 1 lub 2. Budynek jest odrębną nieruchomością, gdy wskazywana jednostka rejestrowa jest typu 2.
  g5rdze character varying(50)[], -- jest położony na gruntach - działka ewidencyjna. relacja 1+.
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(50) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5bud_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5bud
  OWNER TO biuro;
COMMENT ON TABLE g5bud
  IS 'Budynek - Zgodnie z § 2 ust. 1 pkt 4 rozporządzenia';
COMMENT ON COLUMN g5bud.g5idb IS 'identyfikator budynku';
COMMENT ON COLUMN g5bud.g5fuz IS 'kod funkcji użytkowej.1 -mieszkalne,2 -przemysłowe,3 -transportu i łączności,4 -handlowo-usługowe,5 -zbiorniki, silosy i budynki magazynowe,6 -biurowe,7 -szpitale i zakłady opieki medycznej, 8 -oświaty, nauki i kultury oraz budynki sportowe, 9 - produkcyjne, usługowe i gospodarcze dla rolnictwa,10 -inne niemieszkalne';
COMMENT ON COLUMN g5bud.g5wrt IS 'wartość w zł';
COMMENT ON COLUMN g5bud.g5dwr IS 'data wyceny';
COMMENT ON COLUMN g5bud.g5rbb IS 'rok zakończenia budowy';
COMMENT ON COLUMN g5bud.g5pew IS 'pole powierzchni zabudowy w m2 do 1m2';
COMMENT ON COLUMN g5bud.g5peu IS 'łączne pole powierzchni  powierzchni użytkowej lokali w budynku wraz z pomieszczeniami przynależnymi do lokali w m2';
COMMENT ON COLUMN g5bud.g5rzn IS 'numer rejestru zabytków';
COMMENT ON COLUMN g5bud.g5scn IS 'materiał ścian zewnętrznych - 1 mur, 2 drewno, 3 inne';
COMMENT ON COLUMN g5bud.g5radr IS 'adres(y) - budynek może mieć wiele adresów i nazw - relacja 0+';
COMMENT ON COLUMN g5bud.g5rpwl IS 'podstawa własności - dokument - Dotyczy budynków stanowiących odrębny od gruntu przedmiot własności (JR typu 2)- relacja 0+';
COMMENT ON COLUMN g5bud.g5rpwd IS 'Podstawa innych praw do budynku. Dokument. relacja 0+';
COMMENT ON COLUMN g5bud.g5rkrg IS 'Źródło danych o położeniu, dokument - operat geodezyjny - relacja 1+';
COMMENT ON COLUMN g5bud.g5rjdr IS 'Niepuste. Jednostka rejestrowa może być typu 1 lub 2. Budynek jest odrębną nieruchomością, gdy wskazywana jednostka rejestrowa jest typu 2.';
COMMENT ON COLUMN g5bud.g5rdze IS 'jest położony na gruntach - działka ewidencyjna. relacja 1+.';
COMMENT ON COLUMN g5bud.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5bud.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5bud.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5bud.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5bud.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';

-- Table: g5dok

-- DROP TABLE g5dok;

CREATE TABLE g5dok
(
  tab_uid character varying(50) NOT NULL,
  g5kdk character varying(10), -- Rodzaj dokumentu Dopuszczalne wartości atrybutu KDK - kod dokumentu określa tablica nr 26. Teoretycznie powinien być tylko jeden znak od 1 - 8. Ale praktycznie zdarzyło się inaczej.
  g5dtd character varying(25),
  g5dtp character varying(25),
  g5syg character varying(255), -- sygnatura akt  -niestety znajdują się czasami tam całkiem długie łańcuchy opisowe
  g5nsr character varying(255),
  g5opd character varying(255),
  g5rdok character varying(50)[],
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5dok_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5dok
  OWNER TO biuro;
COMMENT ON TABLE g5dok
  IS 'Dokument opisujący prawa';
COMMENT ON COLUMN g5dok.g5kdk IS 'Rodzaj dokumentu Dopuszczalne wartości atrybutu KDK - kod dokumentu określa tablica nr 26. Teoretycznie powinien być tylko jeden znak od 1 - 8. Ale praktycznie zdarzyło się inaczej.';
COMMENT ON COLUMN g5dok.g5syg IS 'sygnatura akt  -niestety znajdują się czasami tam całkiem długie łańcuchy opisowe';
COMMENT ON COLUMN g5dok.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5dok.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5dok.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5dok.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5dok.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';


-- Table: g5dze

-- DROP TABLE g5dze;

CREATE TABLE g5dze
(
  g5idd character varying(40) NOT NULL,
  nr character varying(20),
  id_zd character varying(50) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5idr character varying(100),
  g5nos character varying(100),
  g5wrt character varying(20),
  g5dwr character varying(25),
  g5pew integer,
  g5rzn character varying(100),
  g5dww character varying(25),
  g5radr character varying(50)[],
  g5rpwl character varying(50)[],
  g5rpwd character varying(50)[],
  g5rjdr character varying(50),
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  g5rkrg character varying(50)[],
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  nrobr character varying(10), -- numer obrębu wyłuskany z teryta
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5dze_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5dze_g5idd_key UNIQUE (g5idd )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5dze
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5dze', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5dze.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5dze.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5dze.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5dze.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5dze.nrobr IS 'numer obrębu wyłuskany z teryta';
COMMENT ON COLUMN g5dze.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5dze_geom

-- DROP INDEX sidx_g5dze_geom;

CREATE INDEX sidx_g5dze_geom
  ON g5dze
  USING gist
  (geom );

-- Table: g5dze_test

-- DROP TABLE g5dze_test;

CREATE TABLE g5dze_test
(
  g5idd character varying(40) NOT NULL,
  nr character varying(20),
  id_zd character varying(50) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5idr character varying(100),
  g5nos character varying(100),
  g5wrt character varying(20),
  g5dwr character varying(25),
  g5pew integer,
  g5rzn character varying(100),
  g5dww character varying(25),
  g5radr character varying(50)[],
  g5rpwl character varying(50)[],
  g5rpwd character varying(50)[],
  g5rjdr character varying(50),
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  g5rkrg character varying(50)[],
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  nrobr character varying(10), -- numer obrębu wyłuskany z teryta
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5dze_test_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5dze_test_g5idd_key UNIQUE (g5idd )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5dze_test
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5dze_test', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5dze_test.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5dze_test.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5dze_test.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5dze_test.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5dze_test.nrobr IS 'numer obrębu wyłuskany z teryta';
COMMENT ON COLUMN g5dze_test.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5dze_test_geom

-- DROP INDEX sidx_g5dze_test_geom;

CREATE INDEX sidx_g5dze_test_geom
  ON g5dze_test
  USING gist
  (geom );

-- Table: g5ins

-- DROP TABLE g5ins;

CREATE TABLE g5ins
(
  g5sti character(2), -- Status ...
  g5npe character varying(255),
  g5nsk character varying(255), -- Nazwa skrócona - niestety nie zawsze jest ona skrócona w stosunku do npe - stąd długość 255 znaków
  g5rgn character varying(20),
  g5nip character varying(20),
  g5nzr character varying(100),
  g5nrr character varying(50),
  g5nsr character varying(255),
  g5radr character varying(50),
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5ins_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5ins
  OWNER TO biuro;
COMMENT ON COLUMN g5ins.g5sti IS 'Status 
Atrybut STI wykorzystuje się do określenia grupy i podgrupy rejestrowej Dopuszczalny zakres wartości: 3—31. Wartosci te znajda sie w tabeli osfsti.
';
COMMENT ON COLUMN g5ins.g5nsk IS 'Nazwa skrócona - niestety nie zawsze jest ona skrócona w stosunku do npe - stąd długość 255 znaków';
COMMENT ON COLUMN g5ins.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5ins.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5ins.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5ins.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5ins.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5jdr

-- DROP TABLE g5jdr;

CREATE TABLE g5jdr
(
  g5tjr character(1), -- rodzaj jednostki rejestrowej - 1 - gruntowa, 2 -budynkowa, 3 - lokalowa
  g5ijr character varying(50), -- Identyfikator jednostki rejestrowej
  g5rgn character varying(20), -- Oznaczenie gospodarstwa rolnego lub leśnego – numer REGON.  Nieruchomości wchodzące w skład gospodarstw rolnych, jak i nieruchomości pozarolnicze będące w posiadaniu tych samych osób są opisane w ramach niezależnych jednostek rejestrowych
  g5rwl character(1), -- Rodzaj uprawnienia podmiotu ewidencyjnego do nieruchomości (rodzaj „własności”), 1- własność, 2 - władanie (na zasadach posiadania samoistnego)
  g5rwls character varying(50)[], -- Udział własności lub władania, o którym mowa w § 10 ust. 2 rozporządzenia (UWŁS). Suma udziałów zawsze równa 1. W przypadku współwładania wszystkie udziały są równe. Relacja 1+
  g5rwld character varying(50)[], -- Udział w prawach przysługujących osobom, o których mowa w § 11 ust. 1 pkt 1 rozporządzenia (UWŁD). Suma udziałów zawsze równa 1 lub 0. Relacja 0+
  g5robr character varying(50), -- Leży w obszarze - odnośnik do obrębu. Dokładnie 1 obiekt.
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5jdr_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5jdr
  OWNER TO biuro;
COMMENT ON TABLE g5jdr
  IS 'Jednostka rejestrowa - zgodnie z par 16 rozporządzenia';
COMMENT ON COLUMN g5jdr.g5tjr IS 'rodzaj jednostki rejestrowej - 1 - gruntowa, 2 -budynkowa, 3 - lokalowa';
COMMENT ON COLUMN g5jdr.g5ijr IS 'Identyfikator jednostki rejestrowej';
COMMENT ON COLUMN g5jdr.g5rgn IS 'Oznaczenie gospodarstwa rolnego lub leśnego – numer REGON.  Nieruchomości wchodzące w skład gospodarstw rolnych, jak i nieruchomości pozarolnicze będące w posiadaniu tych samych osób są opisane w ramach niezależnych jednostek rejestrowych';
COMMENT ON COLUMN g5jdr.g5rwl IS 'Rodzaj uprawnienia podmiotu ewidencyjnego do nieruchomości (rodzaj „własności”), 1- własność, 2 - władanie (na zasadach posiadania samoistnego)';
COMMENT ON COLUMN g5jdr.g5rwls IS 'Udział własności lub władania, o którym mowa w § 10 ust. 2 rozporządzenia (UWŁS). Suma udziałów zawsze równa 1. W przypadku współwładania wszystkie udziały są równe. Relacja 1+';
COMMENT ON COLUMN g5jdr.g5rwld IS 'Udział w prawach przysługujących osobom, o których mowa w § 11 ust. 1 pkt 1 rozporządzenia (UWŁD). Suma udziałów zawsze równa 1 lub 0. Relacja 0+';
COMMENT ON COLUMN g5jdr.g5robr IS 'Leży w obszarze - odnośnik do obrębu. Dokładnie 1 obiekt.';
COMMENT ON COLUMN g5jdr.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5jdr.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5jdr.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5jdr.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5jdr.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5jew

-- DROP TABLE g5jew;

CREATE TABLE g5jew
(
  g5idj character varying(20) NOT NULL, -- Identyfikator jedn. ewid....
  g5pew integer, -- Pole powierzchni ewidencyjnej, w m2
  g5naz character varying(50), -- Nazwa własna
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  g5rkrg character varying(20)[], -- Źródło danych o przebiegu granic
  id_zd character varying(50) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5jew_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5jew_g5idj_key UNIQUE (g5idj )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5jew
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5jew', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5jew.g5idj IS 'Identyfikator jedn. ewid.
Teoretycznie 10 znaków powinno wystarczyć, ale na wszelki wypadek zostanie 20';
COMMENT ON COLUMN g5jew.g5pew IS 'Pole powierzchni ewidencyjnej, w m2';
COMMENT ON COLUMN g5jew.g5naz IS 'Nazwa własna';
COMMENT ON COLUMN g5jew.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5jew.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5jew.g5rkrg IS 'Źródło danych o przebiegu granic';
COMMENT ON COLUMN g5jew.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5jew.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5jew.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5jew_geom

-- DROP INDEX sidx_g5jew_geom;

CREATE INDEX sidx_g5jew_geom
  ON g5jew
  USING gist
  (geom );

-- Table: g5jew_test

-- DROP TABLE g5jew_test;

CREATE TABLE g5jew_test
(
  g5idj character varying(20) NOT NULL, -- Identyfikator jedn. ewid....
  g5pew integer, -- Pole powierzchni ewidencyjnej, w m2
  g5naz character varying(50), -- Nazwa własna
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  g5rkrg character varying(20)[], -- Źródło danych o przebiegu granic
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5jew_test_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5jew_test_g5idj_key UNIQUE (g5idj )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5jew_test
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5jew_test', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5jew_test.g5idj IS 'Identyfikator jedn. ewid.
Teoretycznie 10 znaków powinno wystarczyć, ale na wszelki wypadek zostanie 20';
COMMENT ON COLUMN g5jew_test.g5pew IS 'Pole powierzchni ewidencyjnej, w m2';
COMMENT ON COLUMN g5jew_test.g5naz IS 'Nazwa własna';
COMMENT ON COLUMN g5jew_test.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5jew_test.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5jew_test.g5rkrg IS 'Źródło danych o przebiegu granic';
COMMENT ON COLUMN g5jew_test.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5jew_test.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5jew_test.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5jew_test_geom

-- DROP INDEX sidx_g5jew_test_geom;

CREATE INDEX sidx_g5jew_test_geom
  ON g5jew_test
  USING gist
  (geom );

-- Table: g5kkl

-- DROP TABLE g5kkl;

CREATE TABLE g5kkl
(
  tab_uid character varying(50) NOT NULL,
  g5idk character varying(50), -- identyfikator konturu.
  g5ozu character varying(10), -- Oznaczenie użytku - Tabela: „Dopuszczalne wartości atrybutu OZU, OFU"
  g5ozk character varying(10), -- Oznaczenie klasy bonitacyjnej - I, II, III, IIIa, IIIb, IV, IVa, IVb, V,VI, VIz , pusty
  g5pew integer, -- powierzchnia ewidencyjna - W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha
  g5rkrg character varying(50)[], -- Źródło danych o położeniu - Dokument - Operat geodezyjny. relacja 1+
  g5robr character varying(50), -- Leży na obszarze - obręb - dokładnie 1 obiekt
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5kkl_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5kkl
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5kkl', 'geom', 2180, 'POLYGON', 2);
COMMENT ON TABLE g5kkl
  IS 'Kontur klasyfikacyjny - Ciągły obszar gruntu wyodrębniony w wyniku klasyfikacji gleboznawczej.';
COMMENT ON COLUMN g5kkl.g5idk IS 'identyfikator konturu.';
COMMENT ON COLUMN g5kkl.g5ozu IS 'Oznaczenie użytku - Tabela: „Dopuszczalne wartości atrybutu OZU, OFU"';
COMMENT ON COLUMN g5kkl.g5ozk IS 'Oznaczenie klasy bonitacyjnej - I, II, III, IIIa, IIIb, IV, IVa, IVb, V,VI, VIz , pusty';
COMMENT ON COLUMN g5kkl.g5pew IS 'powierzchnia ewidencyjna - W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha';
COMMENT ON COLUMN g5kkl.g5rkrg IS 'Źródło danych o położeniu - Dokument - Operat geodezyjny. relacja 1+';
COMMENT ON COLUMN g5kkl.g5robr IS 'Leży na obszarze - obręb - dokładnie 1 obiekt';
COMMENT ON COLUMN g5kkl.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5kkl.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5kkl.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5kkl.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5kkl.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';


-- Index: sidx_g5kkl

-- DROP INDEX sidx_g5kkl;

CREATE INDEX sidx_g5kkl
  ON g5kkl
  USING gist
  (geom );


-- Table: g5klu

-- DROP TABLE g5klu;

CREATE TABLE g5klu
(
  g5ofu character varying(10), -- Sposób zagospodarowania lub ustalenia prawne dotyczące użytków ekologicznych. Patrz tabela „Dopuszczalne wartości atrybutu OZU i OFU" w pkt 22. Może być pusty, jeżeli oznaczenie wynikające ze sposobu zagospodarowania jest takie samo, jak oznaczenie użytku według operatu gleboznawczego
  g5ozu character varying(10), -- Rodzaj użytku. Jak wyżej. Oznaczenie użytku według operatu gleboznawczego.
  g5ozk character varying(5), -- Oznaczenie klasy bonitacyjnej, I, II, III, IIla, IIIb, IV, IVa, IVb, V,VI, VIz, pusty. Oznaczenie wg operatu gleboznawczego; może być pusty
  g5pew integer, -- Powierzchnia ewidencyjna.  W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha.
  g5rdze character varying(50), -- Wskazanie na działkę ewidencyjną
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5klu_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5klu
  OWNER TO biuro;
COMMENT ON TABLE g5klu
  IS 'Użytki gruntowe i klasy gleboznawcze w granicach działki. 	
Zgodnie z § 67 i 68 rozporządzenia';
COMMENT ON COLUMN g5klu.g5ofu IS 'Sposób zagospodarowania lub ustalenia prawne dotyczące użytków ekologicznych. Patrz tabela „Dopuszczalne wartości atrybutu OZU i OFU" w pkt 22. Może być pusty, jeżeli oznaczenie wynikające ze sposobu zagospodarowania jest takie samo, jak oznaczenie użytku według operatu gleboznawczego';
COMMENT ON COLUMN g5klu.g5ozu IS 'Rodzaj użytku. Jak wyżej. Oznaczenie użytku według operatu gleboznawczego.';
COMMENT ON COLUMN g5klu.g5ozk IS 'Oznaczenie klasy bonitacyjnej, I, II, III, IIla, IIIb, IV, IVa, IVb, V,VI, VIz, pusty. Oznaczenie wg operatu gleboznawczego; może być pusty';
COMMENT ON COLUMN g5klu.g5pew IS 'Powierzchnia ewidencyjna.  W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha.';
COMMENT ON COLUMN g5klu.g5rdze IS 'Wskazanie na działkę ewidencyjną';
COMMENT ON COLUMN g5klu.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5klu.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5klu.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5klu.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5klu.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5klu.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5lkl

-- DROP TABLE g5lkl;

CREATE TABLE g5lkl
(
  tab_uid character varying(50) NOT NULL,
  g5idl character varying(50), -- Identyfikator lokalu
  g5tlok character(1), -- typ lokalu - 1 mieszkalny, 2 niemieszkalny
  g5pew integer, -- pole powierzchni użytkowej lokalu
  g5ppp integer, -- Pole powierzchni pomieszczeń przynależnych do lokalu - w m2
  g5liz integer, -- liczba izb
  g5wrt numeric, -- wartość w zł
  g5dwr character varying(25), -- data wyceny
  g5rjdr character varying(50)[], -- jest częścią - jednostka rejestrowa - Niepuste, gdy lokal jest przedmiotem oddzielnej własności, w przeciwnym wypadku informacja o lokalu samodzielnym. Relacja 0+
  g5radr character varying(50), -- adres - dokładnie 1
  g5rdok character varying(50)[], -- dokumenty - podstawa - 1+
  g5rbud character varying(50), -- budynek - niepuste - dokładnie 1 obiekt
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5lkl_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5lkl
  OWNER TO biuro;
COMMENT ON TABLE g5lkl
  IS 'Lokal samodzielny - Samodzielny lokal mieszkalny lub inny lokal zgodnie z ustawą o własności lokali.';
COMMENT ON COLUMN g5lkl.g5idl IS 'Identyfikator lokalu';
COMMENT ON COLUMN g5lkl.g5tlok IS 'typ lokalu - 1 mieszkalny, 2 niemieszkalny';
COMMENT ON COLUMN g5lkl.g5pew IS 'pole powierzchni użytkowej lokalu';
COMMENT ON COLUMN g5lkl.g5ppp IS 'Pole powierzchni pomieszczeń przynależnych do lokalu - w m2';
COMMENT ON COLUMN g5lkl.g5liz IS 'liczba izb';
COMMENT ON COLUMN g5lkl.g5wrt IS 'wartość w zł';
COMMENT ON COLUMN g5lkl.g5dwr IS 'data wyceny';
COMMENT ON COLUMN g5lkl.g5rjdr IS 'jest częścią - jednostka rejestrowa - Niepuste, gdy lokal jest przedmiotem oddzielnej własności, w przeciwnym wypadku informacja o lokalu samodzielnym. Relacja 0+';
COMMENT ON COLUMN g5lkl.g5radr IS 'adres - dokładnie 1';
COMMENT ON COLUMN g5lkl.g5rdok IS 'dokumenty - podstawa - 1+';
COMMENT ON COLUMN g5lkl.g5rbud IS 'budynek - niepuste - dokładnie 1 obiekt';
COMMENT ON COLUMN g5lkl.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5lkl.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5lkl.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5lkl.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5lkl.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';

-- Table: g5mlz

-- DROP TABLE g5mlz;

CREATE TABLE g5mlz
(
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5rmaz character varying(50),
  g5rzona character varying(50),
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5mlz_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5mlz
  OWNER TO biuro;
COMMENT ON TABLE g5mlz
  IS 'Dwie osoby różnej płci pozostające we współwłasności łącznej przedmiotu ewidencji';
COMMENT ON COLUMN g5mlz.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5mlz.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5mlz.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5mlz.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5mlz.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5obr

-- DROP TABLE g5obr;

CREATE TABLE g5obr
(
  g5nro character varying(40) NOT NULL, -- Nr obrębu w jedn. ewid.
  g5pew integer, -- Pole powierzchni ewidencyjnej
  g5naz character varying(50), -- Nazwa własna
  g5dtw character varying(25),
  g5dtu character varying(25),
  g5rkrg character varying(20)[],
  g5rjew character(20),
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  idjew character varying(50),
  CONSTRAINT g5obr_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5obr_g5nro_key UNIQUE (g5nro )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5obr
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5obr', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5obr.g5nro IS 'Nr obrębu w jedn. ewid.';
COMMENT ON COLUMN g5obr.g5pew IS 'Pole powierzchni ewidencyjnej';
COMMENT ON COLUMN g5obr.g5naz IS 'Nazwa własna';
COMMENT ON COLUMN g5obr.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5obr.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5obr.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5obr_geom

-- DROP INDEX sidx_g5obr_geom;

CREATE INDEX sidx_g5obr_geom
  ON g5obr
  USING gist
  (geom );

-- Table: g5obr_test

-- DROP TABLE g5obr_test;

CREATE TABLE g5obr_test
(
  g5nro character varying(40) NOT NULL, -- Nr obrębu w jedn. ewid.
  g5pew integer, -- Pole powierzchni ewidencyjnej
  g5naz character varying(50), -- Nazwa własna
  g5dtw character varying(25),
  g5dtu character varying(25),
  g5rkrg character varying(20)[],
  g5rjew character(20),
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  idjew character varying(50),
  CONSTRAINT g5obr_test_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5obr_test_g5nro_key UNIQUE (g5nro )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5obr_test
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5obr_test', 'geom', 2180, 'POLYGON', 2);
COMMENT ON COLUMN g5obr_test.g5nro IS 'Nr obrębu w jedn. ewid.';
COMMENT ON COLUMN g5obr_test.g5pew IS 'Pole powierzchni ewidencyjnej';
COMMENT ON COLUMN g5obr_test.g5naz IS 'Nazwa własna';
COMMENT ON COLUMN g5obr_test.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5obr_test.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5obr_test.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5obr_test_geom

-- DROP INDEX sidx_g5obr_test_geom;

CREATE INDEX sidx_g5obr_test_geom
  ON g5obr_test
  USING gist
  (geom );

-- Table: g5osf

-- DROP TABLE g5osf;

CREATE TABLE g5osf
(
  g5plc character(1), -- Płeć - 1 - męska, 2 - żeńska
  g5psl character varying(15),
  g5nip character varying(20), -- NIP
  g5nzw character varying(100), -- Nazwisko
  g5pim character varying(50), -- pierwsze imie
  g5dim character varying(50), -- drugie imie
  g5oim character varying(50), -- Imię ojca
  g5mim character varying(50), -- imię matki
  g5obl character varying(50), -- Obywatelstwo - Pusty oznacza – polskie
  g5dos character varying(50), -- Oznaczenie dokumentu stwierdzającego tożsamość - Seria i nr paszportu lub dowodu osobistego; może być pusty, jeżeli wpisano PESEL lub NIP
  g5radr character varying(50), -- Adres miejsca pobytu stałego (1 lub wcale) - Osoba może nie ujawnić adresu
  g5sti character(1),
  g5dtw character varying(25),
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50) NOT NULL,
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5osf_pkey PRIMARY KEY (tab_uid ),
  CONSTRAINT g5osf_id_zd_g5id1_key UNIQUE (id_zd , g5id1 )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5osf
  OWNER TO biuro;
COMMENT ON TABLE g5osf
  IS 'Osoba fizyczna';
COMMENT ON COLUMN g5osf.g5plc IS 'Płeć - 1 - męska, 2 - żeńska';
COMMENT ON COLUMN g5osf.g5nip IS 'NIP';
COMMENT ON COLUMN g5osf.g5nzw IS 'Nazwisko';
COMMENT ON COLUMN g5osf.g5pim IS 'pierwsze imie';
COMMENT ON COLUMN g5osf.g5dim IS 'drugie imie';
COMMENT ON COLUMN g5osf.g5oim IS 'Imię ojca';
COMMENT ON COLUMN g5osf.g5mim IS 'imię matki';
COMMENT ON COLUMN g5osf.g5obl IS 'Obywatelstwo - Pusty oznacza – polskie';
COMMENT ON COLUMN g5osf.g5dos IS 'Oznaczenie dokumentu stwierdzającego tożsamość - Seria i nr paszportu lub dowodu osobistego; może być pusty, jeżeli wpisano PESEL lub NIP';
COMMENT ON COLUMN g5osf.g5radr IS 'Adres miejsca pobytu stałego (1 lub wcale) - Osoba może nie ujawnić adresu';
COMMENT ON COLUMN g5osf.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5osf.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5osf.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5osf.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5osz

-- DROP TABLE g5osz;

CREATE TABLE g5osz
(
  g5sti character(2), -- Status - 32 -podmioty pozostające we współwłasności łącznej do nieruchomości...
  g5npe character varying(255), -- Nazwa pełna- Może być pusta. Dotyczy spółek cywilnych
  g5nsk character varying(255), -- Nazwa skrócona - niestety praktyka pokazala ze nazwa ta potrafi byc tak samo długa jak g5npe - stąd 255 znaków
  g5rgn character varying(20),
  g5nip character varying(20),
  g5radr character varying(50),
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  g5rskd character varying(50)[],
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5osz_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5osz
  OWNER TO biuro;
COMMENT ON TABLE g5osz
  IS 'Inny podmiot grupowy - Grupa osób, z wyłączeniem małżeństwa, posiadająca prawa do nieruchomości na zasadach współwłasności łącznej, a także: spółki cywilne i wspólnoty gruntowe';
COMMENT ON COLUMN g5osz.g5sti IS 'Status - 32 -podmioty pozostające we współwłasności łącznej do nieruchomości
33 - spółka cywilna
34 - wspólnota gruntowa
35 - inne podmioty grupowe';
COMMENT ON COLUMN g5osz.g5npe IS 'Nazwa pełna- Może być pusta. Dotyczy spółek cywilnych';
COMMENT ON COLUMN g5osz.g5nsk IS 'Nazwa skrócona - niestety praktyka pokazala ze nazwa ta potrafi byc tak samo długa jak g5npe - stąd 255 znaków';
COMMENT ON COLUMN g5osz.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5osz.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5osz.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5osz.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po wartości liczbowej i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5osz.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5udw

-- DROP TABLE g5udw;

CREATE TABLE g5udw
(
  g5rwd character(1), -- Rodzaj innych niż własność praw uwidacznianych w ewidencji (rodzaj władania). Atrybut RWD wykorzystuje się do określenia grupy i podgrupy rejestrowej. ...
  g5ud character varying(50), -- Udział, Ułamek właściwy
  g5rwld character varying(50), -- jest częścia jednostki rejestrowej. Jednostka rejestrowa 1 lub 0.
  g5rpod character varying(50), -- Osoba, która dysponuje udziałem. 1. Osoba fizyczna. 2 - instytucja 3 -małżeństwo 4  - inny podmiot grupow. Dokładnie jedna wartość
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  rpod_rodzaj character varying(20),
  id_podmiot character varying(50), -- złączenie danych, czyli podmiot oraz nazwa tabeli
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5udw_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5udw
  OWNER TO biuro;
COMMENT ON TABLE g5udw
  IS 'Udział władania - Udział w prawach przysługujących osobom, o których mowa w § 11 ust. 1 pkt 1 rozporz. (UWŁD)';
COMMENT ON COLUMN g5udw.g5rwd IS 'Rodzaj innych niż własność praw uwidacznianych w ewidencji (rodzaj władania). Atrybut RWD wykorzystuje się do określenia grupy i podgrupy rejestrowej. 
1 - użytkowanie wieczyste. 2 - trwały zarząd lub zarząd, 3 -wykonywanie prawa własności Skarbu Państwa i innych praw rzeczowych (np. przez AWRSP, WAM, AMW), 4 -gospodarowanie zasobem nieruchomości Skarbu Państwa oraz gminnymi, powiatowymi i wojewódzkimi zasobami nieruchomości, 5 -użytkowanie, 6 -ułamkowa część własności,nieobciążona prawami wymienionymi w pkt 1, 2, 5';
COMMENT ON COLUMN g5udw.g5ud IS 'Udział, Ułamek właściwy';
COMMENT ON COLUMN g5udw.g5rwld IS 'jest częścia jednostki rejestrowej. Jednostka rejestrowa 1 lub 0.';
COMMENT ON COLUMN g5udw.g5rpod IS 'Osoba, która dysponuje udziałem. 1. Osoba fizyczna. 2 - instytucja 3 -małżeństwo 4  - inny podmiot grupow. Dokładnie jedna wartość';
COMMENT ON COLUMN g5udw.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5udw.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5udw.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5udw.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5udw.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5udw.id_podmiot IS 'złączenie danych, czyli podmiot oraz nazwa tabeli ';
COMMENT ON COLUMN g5udw.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5udz

-- DROP TABLE g5udz;

CREATE TABLE g5udz
(
  g5ud character varying(50), -- udział - ułamek właściwy
  g5rwls character varying(50), -- Jest częścią jednostki rejestrowej.  Jednostka rejestrowa - dokładnie jeden element.
  g5rpod character varying(50), -- Osoba, która dysponuje udziałem. 1 - osoba fizyczna, 2 - instytucja, 3 - małżeństwo, 4 -inny podmiot grupowy. Podmiot ewidencyjny lub inny władający, dokładnie 1 element
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  g5id1 character varying(50),
  rpod_rodzaj character varying(20),
  id_podmiot character varying(50), -- złączenie danych, czyli podmiot oraz nazwa tabeli
  g5udz_urpod character varying(50), -- Wszkazanie na pomiot, ale będące złączeniem id_zd + g5rpod + rppod_rodzaj. Jest to wartość unikalna w całej bazie. Służy do złączenia z podmiotem. Nie wiem czy 50 znaków starczy - się okaże.
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5udz_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5udz
  OWNER TO biuro;
COMMENT ON TABLE g5udz
  IS 'Udział osoby we własności lub władaniu, o którym mowa w § 10 ust. 2 rozporządzenia (UWŁS)';
COMMENT ON COLUMN g5udz.g5ud IS 'udział - ułamek właściwy';
COMMENT ON COLUMN g5udz.g5rwls IS 'Jest częścią jednostki rejestrowej.  Jednostka rejestrowa - dokładnie jeden element.';
COMMENT ON COLUMN g5udz.g5rpod IS 'Osoba, która dysponuje udziałem. 1 - osoba fizyczna, 2 - instytucja, 3 - małżeństwo, 4 -inny podmiot grupowy. Podmiot ewidencyjny lub inny władający, dokładnie 1 element';
COMMENT ON COLUMN g5udz.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5udz.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5udz.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5udz.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5udz.id_podmiot IS 'złączenie danych, czyli podmiot oraz nazwa tabeli ';
COMMENT ON COLUMN g5udz.g5udz_urpod IS 'Wszkazanie na pomiot, ale będące złączeniem id_zd + g5rpod + rppod_rodzaj. Jest to wartość unikalna w całej bazie. Służy do złączenia z podmiotem. Nie wiem czy 50 znaków starczy - się okaże.';
COMMENT ON COLUMN g5udz.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';

-- Table: g5uzg

-- DROP TABLE g5uzg;

CREATE TABLE g5uzg
(
  g5idt character varying(50), -- Identyfikator użytku
  g5ozu character varying(10), -- Oznaczenie użytku - wg tabeli „Dopuszczalne wartości atrybutu OZU, OFU"
  g5pew integer, -- Pole powierzchni - W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha
  g5rkrg character varying(50)[], -- Źródło danych o położeniu. Dokument - operat geodezyjny. Relacja 1+
  g5robr character varying(50), -- Leży na obszarze - czyli obręb. Dokładnie jedno wskazanie
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  g5ofu character varying(10),
  tab_uid character varying(50) NOT NULL, -- Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania
  CONSTRAINT g5uzg_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5uzg
  OWNER TO biuro;
SELECT AddGeometryColumn('public', 'g5uzg', 'geom', 2180, 'POLYGON', 2);
COMMENT ON TABLE g5uzg
  IS 'Kontur użytku gruntowego. Ciągły obszar gruntu w granicach obrębu, wyodrębniony ze względu na faktyczny sposób zagospodarowania';
COMMENT ON COLUMN g5uzg.g5idt IS 'Identyfikator użytku';
COMMENT ON COLUMN g5uzg.g5ozu IS 'Oznaczenie użytku - wg tabeli „Dopuszczalne wartości atrybutu OZU, OFU"';
COMMENT ON COLUMN g5uzg.g5pew IS 'Pole powierzchni - W m2, do 1 m2, co odpowiada reprezentacji pola powierzchni z dokładnością do 0,0001 ha';
COMMENT ON COLUMN g5uzg.g5rkrg IS 'Źródło danych o położeniu. Dokument - operat geodezyjny. Relacja 1+';
COMMENT ON COLUMN g5uzg.g5robr IS 'Leży na obszarze - czyli obręb. Dokładnie jedno wskazanie';
COMMENT ON COLUMN g5uzg.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5uzg.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5uzg.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5uzg.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5uzg.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5uzg.tab_uid IS 'Unikalny identyfikator, będący kluczem głównym. Stanowi połączenie id_zd i g5id1 - nie ma więc możliwości zdublowania';


-- Index: sidx_g5uzg_geom

-- DROP INDEX sidx_g5uzg_geom;

CREATE INDEX sidx_g5uzg_geom
  ON g5uzg
  USING gist
  (geom );

-- Table: g5zmn

-- DROP TABLE g5zmn;

CREATE TABLE g5zmn
(
  tab_uid character varying(50) NOT NULL,
  g5nrz character varying(50), -- nr zmiany
  g5stz character varying(255), -- Opis zmiany
  g5dzz character varying(25), -- data zgłoszenia zmiany
  g5dta character varying(25), -- data akceptacji zmiany
  g5dtz character varying(25), -- Data druku zawiadomienia o zmianie
  g5naz character varying(255), -- jednostka prowadząca
  g5robj character varying(50)[], -- dotyczy - relacja 1+
  g5rdok character varying(50)[], -- dokument 1+
  g5dtw character varying(25), -- Data weryfikacji danych
  g5dtu character varying(25), -- Data utworzenia obiektu
  id_zd character varying(40) NOT NULL, -- Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.
  g5id2 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków.
  g5id1 character varying(50), -- Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków.
  CONSTRAINT g5zmn_pkey PRIMARY KEY (tab_uid )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE g5zmn
  OWNER TO biuro;
COMMENT ON TABLE g5zmn
  IS 'Zmiana – „Dziennik zgłoszeń zmian”';
COMMENT ON COLUMN g5zmn.g5nrz IS 'nr zmiany';
COMMENT ON COLUMN g5zmn.g5stz IS 'Opis zmiany';
COMMENT ON COLUMN g5zmn.g5dzz IS 'data zgłoszenia zmiany';
COMMENT ON COLUMN g5zmn.g5dta IS 'data akceptacji zmiany';
COMMENT ON COLUMN g5zmn.g5dtz IS 'Data druku zawiadomienia o zmianie';
COMMENT ON COLUMN g5zmn.g5naz IS 'jednostka prowadząca';
COMMENT ON COLUMN g5zmn.g5robj IS 'dotyczy - relacja 1+';
COMMENT ON COLUMN g5zmn.g5rdok IS 'dokument 1+';
COMMENT ON COLUMN g5zmn.g5dtw IS 'Data weryfikacji danych';
COMMENT ON COLUMN g5zmn.g5dtu IS 'Data utworzenia obiektu';
COMMENT ON COLUMN g5zmn.id_zd IS 'Identyfikator zbioru danych - zazwyczaj najlepiej sprawdza się teryt jednostki rejestrowej. Niezbędny przy aktualizacji danych. Pole wymagane maksymalnie 40 znaków.';
COMMENT ON COLUMN g5zmn.g5id2 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, tuż po id1 i jest ciągiem różnistych znaków. ';
COMMENT ON COLUMN g5zmn.g5id1 IS 'Identyfikator tekstowy rekordu w plikach swde - występuje zaraz po definicji rekordu - czyli w liniach RD i RO, i jest ciągiem różnistych znaków. ';

-- Function: g5sp_delfromtables(character varying)

-- DROP FUNCTION g5sp_delfromtables(character varying);

CREATE OR REPLACE FUNCTION g5sp_delfromtables(in_id_zd character varying)
  RETURNS void AS
$BODY$
BEGIN
	DELETE FROM g5jew where g5jew.id_zd = $1;
	DELETE FROM g5obr where g5obr.id_zd = $1;
	DELETE FROM g5dze where g5dze.id_zd = $1;
	DELETE FROM g5osf where g5osf.id_zd = $1;
	DELETE FROM g5ins where g5ins.id_zd = $1;
	DELETE FROM g5mlz where g5mlz.id_zd = $1;
	DELETE FROM g5osz where g5osz.id_zd = $1;
	DELETE FROM g5jdr where g5jdr.id_zd = $1;
	DELETE FROM g5udz where g5udz.id_zd = $1;
	DELETE FROM g5udw where g5udw.id_zd = $1;
	DELETE FROM g5klu where g5klu.id_zd = $1;
	DELETE FROM g5uzg where g5uzg.id_zd = $1;
	DELETE FROM g5dok where g5dok.id_zd = $1;
	DELETE FROM g5adr where g5adr.id_zd = $1;   
	DELETE FROM g5kkl where g5kkl.id_zd = $1;
	DELETE FROM g5bud where g5bud.id_zd = $1;
	DELETE FROM g5lkl where g5lkl.id_zd = $1;
	DELETE FROM g5zmn where g5zmn.id_zd = $1; 
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION g5sp_delfromtables(character varying)
  OWNER TO postgres;
