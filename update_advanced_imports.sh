#!/bin/bash

# Update imports from cfbd.advanced to cbbd.advanced in all Python files
echo "Updating advanced imports in Python files..."

# Find all Python files and update imports
find . -name "*.py" -type f -exec sed -i '' 's/from cfbd.advanced/from cbbd.advanced/g' {} \;
find . -name "*.py" -type f -exec sed -i '' 's/import cfbd.advanced/import cbbd.advanced/g' {} \;

echo "Advanced import updates completed." 