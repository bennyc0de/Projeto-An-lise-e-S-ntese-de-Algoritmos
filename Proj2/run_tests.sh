#!/bin/bash

# Compile the proj.cpp file
g++ -o proj proj.cpp

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

# Output file to store all results
combined_output_file="combined_output.txt"
> "$combined_output_file"  # Clear the file if it exists

# Run the compiled program with each file that starts with "teste"
for test_file in $(ls teste* | sort -V); 
do
    if [ -f "$test_file" ]; then
        echo "Running with $test_file"
        echo "Output for $test_file:" >> "$combined_output_file"
        ./proj < "$test_file" >> "$combined_output_file"
        echo -e "\n" >> "$combined_output_file"
    fi
done

echo "All outputs saved to $combined_output_file"