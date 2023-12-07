#!/bin/zsh

# Function to count occurrences in a file
count_occurrences() {
    local file="$1"
    local dir="$(dirname "$file")"
    local count=$(grep -c "test_" "$file" || echo 0)
    echo "$dir $count"
}

# Temporary file to store counts
tempfile=$(mktemp)

# Find all 'test_*.py' files and process them
for file in $(find . -type f -name "test_*.py")
do
    count_occurrences "$file" >> "$tempfile"
done

# Aggregate counts by directory
sort -k1,1 "$tempfile" | awk '{count[$1]+=$2} END {for (dir in count) print dir, count[dir]}'

# Clean up
rm "$tempfile"

