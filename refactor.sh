#!/bin/bash

find . -type f -name "*.py" | while read file; do
	if grep -q "Packages" "$file"; then
		echo "Replacing 'Packages' with 'printerwatch' in $file"
		sed -i "s/Packages/printerwatch/g" "$file"
	fi
done
