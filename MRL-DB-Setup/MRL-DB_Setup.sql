DROP TABLE IF EXISTS
  Format,
  Attribut,
  Arbeitsbereich,
  Kategorie,
  KL_DIN276,
  KL_IFC,
  KL_Omniclass,
  KL_Uniformat,
  MWZ_Archicad,
  MWZ_Revit,
  Typ,
  Pset,
  Einheit,
  Verantwortlichkeit,
  Matching   CASCADE;


SET client_encoding = UTF8;
SHOW client_encoding;


CREATE TABLE Format (
  bezeichnung TEXT PRIMARY KEY
);

CREATE TABLE Attribut (
  id SERIAL PRIMARY KEY,
  bezeichnung TEXT,
  format TEXT,
  FOREIGN KEY(format) REFERENCES Format(bezeichnung)
  /*
  ,
  standardArchicad BOOLEAN,
  standardRevit BOOLEAN
  */
);

CREATE TABLE Arbeitsbereich (
  bezeichnung TEXT PRIMARY KEY
);

CREATE TABLE Kategorie (
  id SERIAL PRIMARY KEY,
  bezeichnung TEXT NOT NULL,
  arbeitsbereich TEXT,
  FOREIGN KEY(arbeitsbereich) REFERENCES Arbeitsbereich(bezeichnung),
  log100 TEXT,
  log200 TEXT,
  log300 TEXT,
  log400 TEXT,
  log500 TEXT
);

CREATE TABLE KL_DIN276 (
  kostengruppe INT PRIMARY KEY,
  bezeichnung TEXT NOT NULL
);

CREATE TABLE KL_IFC (
  bezeichnung TEXT PRIMARY KEY
);
/*
CREATE TABLE KL_Omniclass (
  bezeichnung VARCHAR PRIMARY KEY
);

CREATE TABLE KL_Uniformat (
  bezeichnung VARCHAR PRIMARY KEY
);

CREATE TABLE MWZ_Archicad (
  id SERIAL PRIMARY KEY,
  bezeichnung VARCHAR NOT NULL
);

CREATE TABLE MWZ_Revit (
  id SERIAL PRIMARY KEY,
  bezeichnung VARCHAR NOT NULL
);
*/
CREATE TABLE Typ (
  id SERIAL PRIMARY KEY,
  bezeichnung TEXT NOT NULL,
  kategorieId SERIAL,
  FOREIGN KEY(kategorieId) REFERENCES Kategorie(id)  ON DELETE CASCADE,
  klDin276 INT,
  FOREIGN KEY(klDin276) REFERENCES KL_DIN276(kostengruppe),
  klIfc TEXT,
  FOREIGN KEY(klIfc) REFERENCES KL_IFC(bezeichnung)
  /*
  ,
  klOmniclass VARCHAR  FOREIGN KEY REFERENCES KL_Omniclass(bezeichnung),
  klUniformat VARCHAR  FOREIGN KEY REFERENCES KL_Uniformat(bezeichnung),
  mwzArchicadId SERIAL  FOREIGN KEY REFERENCES MWZ_Archicad(id),
  mwzRevitId SERIAL  FOREIGN KEY REFERENCES MWZ_Revit(id)
  */
);

CREATE TABLE Pset (
  bezeichnung TEXT PRIMARY KEY
);

CREATE TABLE Einheit (
  bezeichnung TEXT PRIMARY KEY
);

CREATE TABLE Verantwortlichkeit (
  bezeichnung TEXT PRIMARY KEY,
  erklaerung TEXT
);

CREATE TABLE Matching (
  typId SERIAL,
  FOREIGN KEY(typId) REFERENCES Typ(id),
  attributId SERIAL,
  FOREIGN KEY(attributId) REFERENCES Attribut(id),
  PRIMARY KEY(typId, attributId),
  pset TEXT,
  FOREIGN KEY(pset) REFERENCES Pset(bezeichnung),
  loi_min INT,
  einheit TEXT,
  FOREIGN KEY(einheit) REFERENCES Einheit(bezeichnung),
  infoLieferung TEXT,
  FOREIGN KEY(infoLieferung) REFERENCES Verantwortlichkeit(bezeichnung),
  infoAufnahme TEXT,
  FOREIGN KEY(infoAufnahme) REFERENCES Verantwortlichkeit(bezeichnung)
);
