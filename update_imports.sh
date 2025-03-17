#!/bin/bash

# Update imports and references from cfbd to cbbd in all test files
echo "Updating imports in test files..."

# Find all Python files in the tests directory and update imports
find tests -name "*.py" -type f -exec sed -i '' 's/from cfbd/from cbbd/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/import cfbd/import cbbd/g' {} \;

# Update CFBDClient to CBBDClient
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDClient/CBBDClient/g' {} \;

# Update error class names
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDError/CBBDError/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDAuthError/CBBDAuthError/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDRateLimitError/CBBDRateLimitError/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDNotFoundError/CBBDNotFoundError/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDAPIError/CBBDAPIError/g' {} \;
find tests -name "*.py" -type f -exec sed -i '' 's/CFBDValidationError/CBBDValidationError/g' {} \;

echo "Import updates completed." 