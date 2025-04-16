from app.models.load import initiate, Aircrafts, Airports, Pilots, Flights
from app.tui.tui import FlightMangement

tables = [Aircrafts, Airports, Pilots, Flights]

if __name__ == "__main__":
    initiate()
    FlightMangement(tables).run()