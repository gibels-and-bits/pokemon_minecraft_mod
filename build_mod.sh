#!/bin/bash

echo "ETB Mod Build Script"
echo "===================="

# Set Java compatibility
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8"

# Clean previous builds
echo "Cleaning previous builds..."
./gradlew clean

# Build the mod
echo "Building mod..."
./gradlew build --no-daemon -Dorg.gradle.java.installations.auto-download=false

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "Build successful!"
    echo "JAR file location: build/libs/"
    ls -la build/libs/*.jar 2>/dev/null
else
    echo ""
    echo "Build failed. Trying with Java 8 compatibility workaround..."
    # Try a different approach
    ./gradlew jar --no-daemon -Dorg.gradle.java.installations.auto-download=false
fi