#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p docs/doxygen/output

# Run Doxygen
doxygen docs/doxygen/Doxyfile

# Check if Doxygen ran successfully
if [ $? -eq 0 ]; then
    echo "Documentation generated successfully!"
    echo "You can find the documentation in docs/doxygen/output/html/index.html"
else
    echo "Error generating documentation"
    exit 1
fi 