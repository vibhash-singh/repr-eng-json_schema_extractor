JSON_FILE=/JSONSchemaDiscovery/package.json
NAME=$(node -pe "JSON.parse(fs.readFileSync('$JSON_FILE', 'utf8')).name")
VERSION=$(node -pe "JSON.parse(fs.readFileSync('$JSON_FILE', 'utf8')).version")
echo $NAME $VERSION
python3 /scripts/main.py
echo "Generating report"
cd .. && make report
echo "Report successfully generated"

