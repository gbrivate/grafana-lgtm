## Docker
docker build --tag corban-msc-kafka:latest .
kind load docker-image corban-msc-kafka 
kubectl rollout restart deployment corban-msc-kafka-deployment -n corban
kubectl port-forward svc/corban-msc-kafka-service 8001:8001 -n corban


docker run -p 8002:8002 corban-msc-kafka:latest

docker build --tag corban-msc-kafka:latest .
kind load docker-image corban-msc-kafka
kubectl apply -f k8s.yaml

docker build --tag corban-msc-kafka:latest .
kind load docker-image corban-msc-kafka
kubectl rollout restart deployment corban-msc-kafka-deployment -n corban
kubectl logs deployments/corban-msc-kafka-deployment  -n corban


hey -n 1000 -c 10 -q 2 http://localhost:8002/rolldice


kubectl -n corban exec -it deploy/corban-msc-kafka-deployment -- sh
curl localhost:9464/metrics | grep kafka

## docker cleaning up
docker container stop fastapi-kafka
docker container remove fastapi-kafka
docker build --no-cache  --tag corban-msc-kafka:1.0 .
docker run -p 8004:8004 \
--name fastapi-kafka \
--network=mynet \
-t corban-msc-kafka:1.0


## hey tests

hey -n 1000 -c 50 \
-m POST \
-H "Content-Type: application/json" \
-d '{"key":"user15","value":"Ola mundo!! "}' \
http://localhost:8004/produce


hey -n 100 -c 1 -q 1 http://localhost:8080/fastapi-kafka/consume?limit=1

## Very high load
hey -n 20000 -c 100 -q 1 \
-m POST \
-H "Content-Type: application/json" \
-d '{"key":"user15","value":"The ancient lighthouse, a stoic sentinel against the churning indigo expanse, cast its sweeping, melancholic beam across the obsidian shore. A biting, salt-laden wind, carrying the distant, mournful shriek of gulls, whipped around the solitary figure standing on the volcanic sand. She was wrapped tightly in a thick, hand-knitted shawl, her gaze fixed on the tempest-tossed horizon where the jagged silhouettes of hidden sea stacks battled the dawn. The air tasted of ozone and deep-sea mystery, an intoxicating, wild fragrance that spoke of untold voyages and forgotten shipwrecks buried beneath the ruthless waves. Every few seconds, the rhythmic percussion of a breaking wave punctuated the vast silence, a primal heartbeat in the colossal, indifferent cathedral of the sea. She was waiting for a sign, a glimmer of light on the dark, restless water, clutching a smooth, water-worn pebble—a tiny, precious fragment of a lost memory—as the first, tentative rays of sunlight finally broke through the heavy, grey cloud cover, promising a momentary reprieve from the perpetual, dramatic gloom of the northern ocean."}' \
http://localhost:8004/produce

hey -n 20000 -c 100 - \
-m POST \
-H "Content-Type: application/json" \
-d '{"key":"user15","value":"The ancient lighthouse, a stoic sentinel against the churning indigo expanse, cast its sweeping, melancholic beam across the obsidian shore. A biting, salt-laden wind, carrying the distant, mournful shriek of gulls, whipped around the solitary figure standing on the volcanic sand. She was wrapped tightly in a thick, hand-knitted shawl, her gaze fixed on the tempest-tossed horizon where the jagged silhouettes of hidden sea stacks battled the dawn. The air tasted of ozone and deep-sea mystery, an intoxicating, wild fragrance that spoke of untold voyages and forgotten shipwrecks buried beneath the ruthless waves. Every few seconds, the rhythmic percussion of a breaking wave punctuated the vast silence, a primal heartbeat in the colossal, indifferent cathedral of the sea. She was waiting for a sign, a glimmer of light on the dark, restless water, clutching a smooth, water-worn pebble—a tiny, precious fragment of a lost memory—as the first, tentative rays of sunlight finally broke through the heavy, grey cloud cover, promising a momentary reprieve from the perpetual, dramatic gloom of the northern ocean."}' \
http://localhost:8004/produce