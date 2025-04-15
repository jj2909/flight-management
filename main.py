from load import initiate, Aircrafts, Airports, Pilots, Flights
from tui.menus import show_intro, main_menu

tables = [Aircrafts, Airports, Pilots, Flights]

if __name__ == "__main__":
    initiate()
    show_intro()
    main_menu(tables)
