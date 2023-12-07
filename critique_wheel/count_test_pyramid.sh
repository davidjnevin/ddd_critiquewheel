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

# Find all 'test_*.py' files in the tests directory and process them
for file in $(find ./tests -type f -name "test_*.py")
do
    count_occurrences "$file" >> "$tempfile"
done

# Aggregate counts by directory and sort by test count
sort -k1,1 "$tempfile" | \
    awk '{count[$1]+=$2} END {for (dir in count) print dir, count[dir]}' | \
    sort -k2,2nr | \
    awk '{printf "%-20s (%3d) ", $1, $2; for (i=0; i<$2; i++) printf "x"; print ""}'

# Clean up
rm "$tempfile"

