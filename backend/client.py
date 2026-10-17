import requests

API = "http://127.0.0.1:8000"


def read_matrix():
    while True:
        try:
            m = int(input("Number of rows/sources: "))
            n = int(input("Number of columns/destinations: "))
            if not (1 <= m <= 100 and 1 <= n <= 100):
                raise ValueError("Dimensions must be from 1 to 100.")
            break
        except ValueError as exc:
            print("Invalid dimensions:", exc)

    matrix = []
    print(f"Enter {m} rows with {n} values each.")
    for i in range(m):
        while True:
            try:
                row = [
                    float(v) for v in
                    input(f"Row {i + 1}: ").replace(",", " ").split()
                ]
                if len(row) != n:
                    raise ValueError(f"Enter exactly {n} values.")
                matrix.append(row)
                break
            except ValueError as exc:
                print("Invalid row:", exc)
    return matrix


def show_result(data):
    if "results" in data:
        print("\n========== METHOD COMPARISON ==========")
        for _, result in sorted(
            data["results"].items(),
            key=lambda item: item[1]["total_cost"]
        ):
            print(f"{result['method']:<32} Cost: {result['total_cost']:.2f}")
            print("Allocation:", result["allocation"])
        if "optimal" in data["results"]:
            print(
                "\nGLOBAL MINIMUM COST:",
                f"{data['results']['optimal']['total_cost']:.2f}"
            )
        return

    print("\n========== FINAL SOLUTION ==========")
    print("Problem:", data["problem"])
    print("Method:", data["method"])

    if data["problem"] == "assignment":
        print("\nAssignments:")
        for item in data["assignments"]:
            print(
                f"Row {item['row']} -> Column {item['column']}"
                f" | Cost = {item['cost']:g}"
            )
        print("\nAssignment matrix:")
        for row in data["allocation"]:
            print("  ".join(map(str, row)))
    else:
        print("\nAllocation matrix:")
        for i, row in enumerate(data["allocation"], start=1):
            print(f"Source {i}: " + "  ".join(f"{v:g}" for v in row))
        print("Supply totals:", data["row_totals"])
        print("Demand totals:", data["column_totals"])
        print("Supply verified:", data["supply_verified"])
        print("Demand verified:", data["demand_verified"])
        if "all_initial_results" in data:
            print("\nInitial-method comparison:")
            for item in data["all_initial_results"].values():
                print(f"{item['method']}: {item['total_cost']:.2f}")

    print("\nTotal cost:", f"{data['total_cost']:.2f}")
    print("Optimality guaranteed:", data["optimality_guaranteed"])


def main():
    while True:
        print("\n" + "=" * 46)
        print("    OPERATIONS RESEARCH SOLVER")
        print("=" * 46)
        print("1. Transportation Problem")
        print("2. Assignment Problem - Hungarian Method")
        print("0. Exit")

        choice = input("Choose problem: ").strip()
        if choice == "0":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                costs = read_matrix()
                supply = [
                    float(v) for v in input(
                        "Supply values (space/comma-separated): "
                    ).replace(",", " ").split()
                ]
                demand = [
                    float(v) for v in input(
                        "Demand values (space/comma-separated): "
                    ).replace(",", " ").split()
                ]

                print("\n1. North-West Corner")
                print("2. Least Cost")
                print("3. Vogel's Approximation Method")
                print("4. Best Minimum Cost (Optimal LP)")
                print("5. Compare All Methods")
                print("6. Best Initial Solution")
                methods = {
                    "1": "north_west",
                    "2": "least_cost",
                    "3": "vam",
                    "4": "optimal",
                    "5": "compare",
                    "6": "best_initial",
                }
                selected = input("Choose method: ").strip()
                if selected not in methods:
                    print("Invalid method.")
                    continue

                endpoint = "/transportation"
                payload = {
                    "costs": costs,
                    "supply": supply,
                    "demand": demand,
                    "method": methods[selected],
                }

            elif choice == "2":
                print("\nEnter assignment cost matrix:")
                costs = read_matrix()
                endpoint = "/assignment"
                payload = {"costs": costs}
            else:
                print("Invalid choice.")
                continue

            response = requests.post(
                API + endpoint, json=payload, timeout=60
            )
            if response.ok:
                show_result(response.json())
            else:
                try:
                    print("API error:", response.json().get("detail", response.text))
                except ValueError:
                    print("API error:", response.text)

        except (ValueError, requests.RequestException) as exc:
            print("Input or connection error:", exc)


if __name__ == "__main__":
    main()
