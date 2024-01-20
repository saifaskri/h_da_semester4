from sqlalchemy import *


user = "saif_zineddine"
password = "Saif2019@"
dbname = "stsaaskri"
server = "141.100.70.93"

# Create an engine object with connection information to the database
# This uses python f-strings, see https://peps.python.org/pep-0498/
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{server}/{dbname}", echo=True)


def get_all_airports():
    """Returns a list of all Airport IATA Codes and Names

    You have to implement this function.
    The expected return type is a list of tuples where a tuple represents
    a single airport. Inside the tuple, the iata code is expected to be the first
    element.
    The order of the airports is not important.
    """
    pass


def login(vorname: str, nachname: str) -> int:
    """Logs in a user, creating them if necessary

    You have to implement this function.
    This function shall first query the database, if a user with the given parameters
    vorname, nachname exists. If it does, then return the Kundennummer of the user.

    If the user does not exists, determine the next unused Kundennummer, create the user
    in the database and return the new Kundennummer.
    Don't forget to commit the connection after the insert!
    """
    pass


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
    pass


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
            print("Passagier eingeloggt")

        if current_user is not None and inp == "2":
            print()
            airports = get_all_airports()
            for airport in enumerate(airports):
                print(airport[0], airport[1][0], airport[1][1])
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
