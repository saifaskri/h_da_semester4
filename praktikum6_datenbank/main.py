from sqlalchemy import *


# Create an engine object with connection information to the database
# This uses python f-strings, see https://peps.python.org/pep-0498/
DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    host="141.100.232.166",
    port=5432,
    database="stsaaskri",
    username="saif_zineddine",
    password="Saif2019@"
)
engine = create_engine(DATABASE_URL, echo=True)


def get_all_airports():
    """Returns a list of all Airport IATA Codes and Names

    You have to implement this function.
    The expected return type is a list of tuples where a tuple represents
    a single airport. Inside the tuple, the iata code is expected to be the first
    element.
    The order of the airports is not important.
    """
    with engine.connect() as con:
        stmt = text(f"select iata, name  from flughaefen")
        return con.execute(stmt)  # binding parameters on execution


def addNewUser(vorname: str, nachname: str) -> int:
    print(f"Adding new User {vorname} {nachname}")
    newKnr = lastKnr() + 1
    with engine.connect() as con:
        stmt = text(f"INSERT INTO Passagiere (knr,nachname,vorname,bonusmeilen) VALUES (:newKnr ,:nachname , :vorname, 0)")
        result = con.execute(stmt, {"newKnr": newKnr, "vorname": vorname,"nachname": nachname})  # binding parameters on execution

        """ # Check the result for success
        if result.rowcount > 0:
            print("Insert successful!")
        else:
            print("Insert failed!") 
        """
        con.commit()
        return newKnr


def lastKnr():
    with engine.connect() as con:
        stmt = text("select MAX(knr) from Passagiere p ")
        return con.execute(stmt).scalar()  # binding parameters on execution


def fetchUser(vorname: str, nachname: str):
    with engine.connect() as con:
        stmt = text("select * from Passagiere p where p.vorname = :vorname and p.nachname = :nachname")
        return con.execute(stmt, {"vorname": vorname, "nachname": nachname})  # binding parameters on execution


def login(vorname: str, nachname: str) -> int:
    result = fetchUser(vorname, nachname)
    fetched_user = result.fetchone()
    if ( fetched_user is not None):
        return fetched_user[0]
    else:
        return addNewUser(vorname, nachname)


def book_flight(current_user: int, home: str):
    """Book a flight for the currently logged in user, starting from the home airport

    You have to implement this function.
    Obviously, this function will only work is current_user and home are filled with
    correct data. This is already implemented in the menu, so you can assume that the
    values are corrent.
    First, present the user with a list of all flights starting at the home airport.
    The list shall contain (at least) the following information:
    - Flight number
    - Departure Date
    - **Name** of the destination airport

    The user then chooses which flight they would like to book and the booking is completed
    by inserting the correct values to the table. Assume that all flights are 99 Euros/Dollar.
    Don't forget to commit the connection after the insert!
    """
    with engine.connect() as con:
        stmt = text(f"SELECT a.flugnr , a.datum , flug_ziel.name from Abfluege as a JOIN Fluege as f ON a.flugnr = f.flugnr JOIN Flughaefen as flug_ziel ON flug_ziel.iata = f.ziel ")
        result = con.execute(stmt)
        # print(result.fetchall())
        stmt = text(f"INSERT INTO Buchung b (b.knr,b.flugnr,b.datum,b.preis) VALUES (7,'LH-100','2000.12.03',99)")
        con.execute(stmt)
        print("Insert successful!")
        # Commit the transaction
        con.commit()

if __name__ == "__main__":
    current_user = None
    home = None
    while True:
        print()
        if current_user is None:
            print("Buchungssystem für Flüge - Hauptmenü")
            print("------------------------------------")
        else:
            print(
                f"Buchungssystem für Flüge - Hauptmenü (Eingeloggt: {current_user})")
            print("----------------------------------------------------")

        print("1 Benutzer einloggen")
        if current_user is not None:
            print("2 Heimatflughafen wählen")
            print("3 Flüge anzeigen und buchen")
        print("0 Programm beenden")
        inp = input("Eingabe? ")

        if inp == "0":
            break

        if inp == "1":
            vorname = input("Vorname? ")
            nachname = input("Nachname? ")
            current_user = login(vorname, nachname)
            print(f"{current_user} Passagier eingeloggt")
        if current_user is not None and inp == "2":
            print()
            airports = get_all_airports().fetchall()
            for airport in enumerate(airports):
                print(f"{airport[0]} {airport[1][0]} {airport[1][1]}")
            inp = int(input("Welche Flughafennummer? "))
            if inp < 0 or inp >= len(airports):
                print("Ungültige Nummer ausgewählt!")
            else:
                home = airports[inp][0]

        if current_user is not None and inp == "3":
            if home is None:
                print("Bitte zuerst einen Heimatflughafen wählen")
            else:
                book_flight(current_user, home)
