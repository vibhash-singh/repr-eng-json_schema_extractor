# Copyright 2024, Vibhash Kumar Singh <singh13@ads.uni-passau.de>
# SPDX-License-Identifier: GPL-2.0-only

JSON_FILE=/JSONSchemaDiscovery/package.json
NAME=$(node -pe "JSON.parse(fs.readFileSync('$JSON_FILE', 'utf8')).name")
VERSION=$(node -pe "JSON.parse(fs.readFileSync('$JSON_FILE', 'utf8')).version")
echo $NAME $VERSION