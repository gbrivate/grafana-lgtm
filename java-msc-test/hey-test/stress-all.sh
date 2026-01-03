#!/usr/bin/env bash

BASE_URL="http://localhost/java/api"
DURATION="5m"

echo "Starting parallel stress test for ${DURATION}..."
echo "Target: ${BASE_URL}"
echo "============================================="

# /hello – baseline throughput
hey -z $DURATION -q 50 -c 25 \
  "${BASE_URL}/hello" &
PID_HELLO=$!

# /slow – latency & thread blocking
hey -z $DURATION -q 10 -c 10 \
  "${BASE_URL}/slow" &
PID_SLOW=$!

# /loop – CPU + blocking stress
hey -z $DURATION -q 5 -c 5 \
  "${BASE_URL}/loop?id=100" &
PID_LOOP=$!

# /user – JSON POST
hey -z $DURATION -q 20 -c 15 \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Gabriel","email":"gabriel@test.com"}' \
  "${BASE_URL}/user" &
PID_USER=$!

# /error – constant 500s
hey  -q 10 -c 10 \
  "${BASE_URL}/error?status=500&message=boom" &
PID_ERROR_500=$!

# /error – 404s
hey  -q 10 -c 10 \
  "${BASE_URL}/error?status=404&message=notfound" &
PID_ERROR_404=$!

echo "All tests running in parallel..."
echo "PIDs: $PID_HELLO $PID_SLOW $PID_LOOP $PID_USER $PID_ERROR_500 $PID_ERROR_404"
echo "============================================="

wait

echo "Stress test completed."

