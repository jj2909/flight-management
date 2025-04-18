from app.initiate_db import initiate
from app.models import Aircrafts, Airports, Pilots, Flights
from app.tui.tui import FlightMangement


def main():
    tables = [Aircrafts, Airports, Pilots, Flights]
    # initiate()
    FlightMangement(tables).run()


if __name__ == "__main__":
    main()
