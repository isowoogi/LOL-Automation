from urllib.parse import urlparse, parse_qs

# URL
url = "lolimo://?path=C%3A%5CRiot%20Games%5CLeague%20of%20Legends%5CGame&server=lolimo.net%3A3000&observer=%2BFYHUMNkmseF6SpXMyHkmCokushu3JGr&game_id=5098431728&platform=NA1"

# Parse the URL
parsed_url = urlparse(url)

# Extract the query parameters
params = parse_qs(parsed_url.query)

# Print the parameters
for key, value in params.items():
    print(f"{key}: {value[0]}")
