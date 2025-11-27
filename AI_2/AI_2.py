# map_coloring.py
class MapColoring:
    def __init__(self, regions=None, adjacency=None, colors=None):
        # Default: Australia map
        self.regions = regions or ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
        self.adjacency = adjacency or {
            "WA": ["NT", "SA"],
            "NT": ["WA", "SA", "Q"],
            "SA": ["WA", "NT", "Q", "NSW", "V"],
            "Q": ["NT", "SA", "NSW"],
            "NSW": ["Q", "SA", "V"],
            "V": ["SA", "NSW"],
            "T": []  # Tasmania has no land neighbors
        }
        self.colors = colors or ["Red", "Green", "Blue"]
        # assignment: region -> color or None
        self.assignment = {r: None for r in self.regions}
        self.steps = 0

    def display_state(self):
        print("Current assignments:")
        for r in self.regions:
            print(f"  {r}: {self.assignment[r] or '-'}")
        print()

    def is_valid(self, region, color):
        """Check if coloring 'region' with 'color' conflicts with neighbors."""
        for neigh in self.adjacency.get(region, []):
            neigh_color = self.assignment.get(neigh)
            if neigh_color == color:
                return False
        return True

    def select_unassigned_region(self):
        """Simple selection: first unassigned region (could be improved with MRV)."""
        for r in self.regions:
            if self.assignment[r] is None:
                return r
        return None

    def backtrack(self):
        """Recursive backtracking search. Returns True if a complete valid assignment is found."""
        self.steps += 1
        region = self.select_unassigned_region()
        if region is None:
            return True  # all regions assigned

        for color in self.colors:
            if self.is_valid(region, color):
                self.assignment[region] = color
                # Uncomment next two lines to see the assignment steps live
                # print(f"Assign {region} = {color}")
                # self.display_state()
                if self.backtrack():
                    return True
                # backtrack
                self.assignment[region] = None

        return False

    def solve(self, show_steps=False):
        self.steps = 0
        if show_steps:
            print("Starting map coloring...\n")
            self.display_state()
        success = self.backtrack()
        if success:
            print("Solution found!\n")
            self.display_state()
            print(f"Steps (recursive calls): {self.steps}")
            return True
        else:
            print("No solution found.")
            return False


def main():
    # You can customize regions, adjacency and colors here if you want another map.
    solver = MapColoring()

    # Interactive choice: solve automatically or let user assign manually before solving
    choice = input("Solve automatically? (y/n) [y]: ").strip().lower() or "y"
    if choice == "y":
        solver.solve(show_steps=False)
    else:
        # Manual interactive assignment
        while True:
            solver.display_state()
            if all(solver.assignment[r] is not None for r in solver.regions):
                print("All regions assigned.")
                break
            region = input(f"Enter region to color {solver.regions}: ").strip()
            if region not in solver.regions:
                print("Unknown region. Try again.")
                continue
            color = input(f"Enter color {solver.colors}: ").strip().title()
            if color not in solver.colors:
                print("Invalid color. Try again.")
                continue
            if not solver.is_valid(region, color):
                print("Invalid assignment: neighbors have same color. Try again.")
                continue
            solver.assignment[region] = color

        # Optionally check/complete with solver
        cont = input("Do you want the solver to complete remaining regions / check consistency? (y/n) [n]: ").strip().lower() or "n"
        if cont == "y":
            solver.solve(show_steps=True)

if __name__ == "__main__":
    main()
