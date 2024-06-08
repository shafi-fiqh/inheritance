curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"must_haves": ["mother", "father"], "not_haves": [], "n_types": 3}' \
  http://localhost:"$1"/generate_problems
