#!/bin/bash

# Update imports from cfbd.utils to cbbd.utils in all Python files
echo "Updating utils imports in Python files..."

# Find all Python files and update imports
find . -name "*.py" -type f -exec sed -i '"' 's/from cfbd.utils/from cbbd.utils/g' {} \;
find . -name "*.py" -type f -exec sed -i '"' 's/import cfbd.utils/import cbbd.utils/g' {} \;

echo "Utils import updates completed."
