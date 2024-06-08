curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"must_haves": ["mother", "father"], "not_haves": [], "n_types": 3}' \
  https://islamic-inheritance-api-2f1f200c92b2.herokuapp.com/generate_problems
