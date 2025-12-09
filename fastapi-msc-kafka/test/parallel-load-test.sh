#!/usr/bin/env bash
clear
set -e

# Colors for nicer logs
GREEN="\033[0;32m"
NC="\033[0m"

echo -e "${GREEN}Starting PRODUCE and CONSUME Hey load tests in parallel...${NC}"

# -----------------------------
# PRODUCE TEST
# -----------------------------
produce_test() {
  hey -n 20000 -c 100 \
    -m POST \
    -H "Content-Type: application/json" \
    -d '{"key":"user15","value":"The ancient lighthouse, a stoic sentinel against the churning indigo expanse, cast its sweeping, melancholic beam across the obsidian shore. A biting, salt-laden wind, carrying the distant, mournful shriek of gulls, whipped around the solitary figure standing on the volcanic sand. She was wrapped tightly in a thick, hand-knitted shawl, her gaze fixed on the tempest-tossed horizon where the jagged silhouettes of hidden sea stacks battled the dawn. The air tasted of ozone and deep-sea mystery, an intoxicating, wild fragrance that spoke of untold voyages and forgotten shipwrecks buried beneath the ruthless waves. Every few seconds, the rhythmic percussion of a breaking wave punctuated the vast silence, a primal heartbeat in the colossal, indifferent cathedral of the sea. She was waiting for a sign, a glimmer of light on the dark, restless water, clutching a smooth, water-worn pebble—a tiny, precious fragment of a lost memory—as the first, tentative rays of sunlight finally broke through the heavy, grey cloud cover, promising a momentary reprieve from the perpetual, dramatic gloom of the northern ocean."}' \
    http://localhost:8004/produce
}

# -----------------------------
# CONSUME TEST
# -----------------------------
consume_test() {
  hey -n 100 -c 1 \
    -m GET \
    -H "Content-Type: application/json" \
    "http://localhost:8004/consume?limit=1000"
}

# Run in parallel
produce_test &
PID1=$!

consume_test &
PID2=$!

echo -e "${GREEN}Both tests running in parallel...${NC}"
echo "produce PID = $PID1"
echo "consume PID = $PID2"

# Wait for both processes
wait $PID1
wait $PID2

echo -e "${GREEN}All tests completed!${NC}"
