import sys

def print_usage():
    print("Usage: python main.py [squares|virus]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    simulation_type = sys.argv[1].lower()
    if simulation_type == "squares":
        from src import calculate_squares
        calculate_squares.main()
    elif simulation_type == "virus":
        from src import virus_simulation
        virus_simulation.main()
    else:
        print("Invalid simulation type. Choose 'squares' or 'virus'.")
        print_usage()
