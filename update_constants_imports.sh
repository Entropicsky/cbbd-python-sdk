#!/bin/bash

# Update imports from cfbd.constants to cbbd.constants in all Python files
echo "Updating constants imports in Python files..."

# Find all Python files in the cbbd directory and update imports
find cbbd -name "*.py" -type f -exec sed -i '' 's/from cfbd.constants/from cbbd.constants/g' {} \;
find cbbd -name "*.py" -type f -exec sed -i '' 's/import cfbd.constants/import cbbd.constants/g' {} \;

echo "Constants import updates completed." 