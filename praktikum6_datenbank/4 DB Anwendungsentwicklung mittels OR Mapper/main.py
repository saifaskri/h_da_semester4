from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from datetime import datetime
from typing import List
from sqlalchemy.orm.exc import NoResultFound


# Basisklasse für die ORM-Klassen
Base = declarative_base()

movie_genre = Table(
    "movie_genre_table",
    Base.metadata,
    Column("genre", ForeignKey("genre_table.genre"), primary_key=True),
    Column("movie", ForeignKey("movie_table.imdbID"), primary_key=True),
)

class Genre(Base):
    __tablename__ = 'genre_table'
    genre : Mapped[str] = mapped_column(String, primary_key=True)
    movies = relationship("Movie",secondary=movie_genre, back_populates="genres")
    
    def __init__(self, genre):
        self.genre = genre
    def __repr__(self):
        return f"{self.genre}"

class Movie(Base):
    __tablename__ = 'movie_table'
    imdbID : Mapped[str] = mapped_column(String, primary_key=True)
    titel : Mapped[str] = mapped_column(String)
    year : Mapped[Date] = mapped_column(Date)
    studio_name_fk : Mapped[str] = mapped_column(ForeignKey("studio_table.name"), nullable=False)

    genres: Mapped[List[Genre]] = relationship(secondary=movie_genre, back_populates="movies")
    studio = relationship('Studio', back_populates='movies')

    def __init__(self, imdbID, titel, year,studio,genres:list):
        self.imdbID = imdbID
        self.titel = titel
        self.year = year
        self.studio = studio
        for gen in genres:
            self.genres.append(gen)

    def __repr__(self):
        return f"{self.imdbID} {self.titel} {self.year}"

        

class Studio(Base):
    __tablename__ = 'studio_table'
    name : Mapped[str] = mapped_column(String, primary_key=True)
    country : Mapped[str] = mapped_column(String)
    movies : Mapped[List[Movie]] = relationship(back_populates="studio")

    def __init__(self, name, country):
        self.name = name
        self.country = country

    def get_name(self):
        return self.name
    
    def get_country(self):
        return self.country

    def __repr__(self):
        return f"{self.name} {self.country}"

def db_fill():
    # Erstellen einer Session
    Session = sessionmaker(bind=engine)
    session = Session()
    s1 = Studio("Saif","Germany")
    s2 = Studio("Ahmed","Tunesia")
    # Genres erstellen
    g1 = Genre("Commedy")
    g2 = Genre("Action")
    g3 = Genre("Fiction")
    g4 = Genre("Horror")
    g5 = Genre("Drama")
    m1 = Movie("1", "Inception", datetime(2010, 7, 16),s1,[g1])
    m2 = Movie("2", "The Dark Knight", datetime(2008, 7, 18),s2,[g1,g3,g4])
    m3 = Movie("3", "Interstellar", datetime(2014, 11, 7),s2,[g5,g3,g2])
    m4 = Movie("4", "The Prestige", datetime(2006, 10, 20),s1,[g5,g3,g4])
    session.add_all([s1, s2])
    session.add_all([g1, g2, g3, g4, g5])
    session.add_all([m1, m2,m3,m4])
    # Transaktion abschließen (commit)
    session.commit()
    # Session schließen
    session.close()

def Ausgabe_aller_Studios():
    with Session(engine) as session:
        all_studio = select(Studio)
        studios = session.scalars(all_studio).fetchall()
        print("All Studios:")
        for studio in studios:
            print(studio)

def Ausgabe_aller_Filme_eines_Studios():
    with Session(engine) as session:
        studioname = input("Enter the name of the studio: ")
        
        try:
            stmt = select(Studio).where(Studio.name == studioname)
            studio = session.scalars(stmt).one()
            if studio:
                print(f"All movies of Studio {studio.name}:")
                for movie in studio.movies:
                    print(movie)
            else:
                print("Studio not found.")
        except NoResultFound:
            print("No studio with the provided name was found.")

def Ausgabe_aller_Genres():
    with Session(engine) as session:
        stmt = select(Genre)
        geners = session.scalars(stmt).fetchall()
        print("All Genres:")
        for gener in geners:
            print(gener)

def Ausgabe_aller_Filme_eines_Genres():
    with Session(engine) as session:
        genre_type = input("Enter the name of the genres: ")
        try:
            stmt = select(Genre).where(Genre.genre == genre_type)
            genres = session.scalars(stmt).one()
            if genres:
                print(f"All movies of Genres {genre_type}:")
                for movie in genres.movies:
                    print(movie)
            else:
                print("Genres not found.")
        except NoResultFound:
            print("No Genre with the provided input was found.")





DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    host="141.100.232.166",
    port=5432,
    database="stsaaskri",
    username="saif_zineddine",
    password="Saif2019@"
)

engine = create_engine(DATABASE_URL, echo=False)

#Base.metadata.create_all(engine)
#db_fill()
print("################################################################################################################################################")
Ausgabe_aller_Studios()
print("################################################################################################################################################")
Ausgabe_aller_Filme_eines_Studios()
print("################################################################################################################################################")
Ausgabe_aller_Genres()
print("################################################################################################################################################")
Ausgabe_aller_Filme_eines_Genres()
print("################################################################################################################################################")



















