import csv
from collections import defaultdict

def calculate_probabilities(csv_file):
    # Initialize counters
    number_frequencies = defaultdict(int)
    total_appearances = 0

    # Read the CSV file
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Assuming the column name is 'Numero'
        column_name = 'Numero'
        
        if column_name not in reader.fieldnames:
            raise KeyError(f"Column '{column_name}' not found in the CSV file.")
        
        for row in reader:
            number = int(row[column_name])
            number_frequencies[number] += 1
            total_appearances += 1

    # Calculate probabilities
    number_probabilities = {}
    for number in range(1, 1001):
        frequency = number_frequencies[number]
        probability = frequency / total_appearances if total_appearances > 0 else 0
        number_probabilities[number] = probability

    return number_probabilities

def display_probabilities(probabilities):
    print(f"{'Number':>6} |  {'Probability':>12}")
    print("-" * 22)
    for number, probability in probabilities.items():
        print(f"{number:03d} | %{probability:>12.10f}")

def display_top_5(probabilities):
    # Sort the probabilities from highest to lowest
    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    # Select the top 5
    top_5 = sorted_probabilities[:5]

    print("\nTop 5 most likely numbers:")
    print(f"{'Number':>6} | {'Probability':>12}")
    print("-" * 22)
    for number, probability in top_5:
        print(f"{number:03d} | %{probability:>12.10f}")


csv_file = 'results.csv'
probabilities = calculate_probabilities(csv_file)
display_probabilities(probabilities)
display_top_5(probabilities)
