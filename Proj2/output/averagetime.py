import sys
import glob

def process_files(file_pattern):
    files = glob.glob(file_pattern)
    results = []

    for file in files:
        with open(file, 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) == 4:
                    try:
                        first_int = int(parts[0])
                        float_value = float(parts[3])
                        results.append((first_int, float_value))
                    except ValueError:
                        continue

    return results

def calculate_averages(results):
    averages = {}
    for first_int, float_value in results:
        if first_int not in averages:
            averages[first_int] = []
        averages[first_int].append(float_value)

    for key in averages:
        averages[key] = sum(averages[key]) / len(averages[key])

    return averages

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python averagetime.py <file_pattern>")
        sys.exit(1)

    file_pattern = sys.argv[1]
    results = process_files(file_pattern)
    averages = calculate_averages(results)

    for key, avg in averages.items():
        print(f"{key}: {avg:.2f}")