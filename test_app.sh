curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"must_haves": ["mother", "father"], "not_haves": ["father"], "n_types": 3}' \
  http://localhost:3000/generate_problems
