JSON_FILE=/JSONSchemaDiscovery/package.json
VERSION=$(node -pe "JSON.parse(fs.readFileSync('$JSON_FILE', 'utf8')).version")
echo "JSONSchemaDiscovery $VERSION"