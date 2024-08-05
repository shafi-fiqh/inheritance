curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"must_haves": ["mother", "father", "son", "daughter"], "not_haves": ["father_of_father"], "n_types": 4}' \
  http://localhost:3000/generate_problems
