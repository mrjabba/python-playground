from openai import OpenAI
import json
import random
import matplotlib.pyplot as plt
import networkx as nx
import re

"""
Some local ollama hacking.
Note that these distances are wildly inaccurate, b/c this model really isn't very realiable in this area.
But, it was fun to practice using this in a network graph with Python.

This script generates a network visualization of US cities and their driving distances. 
It leverages a local LLM (smollm3) to dynamically fetch approximate driving distances between city pairs, 
then visualizes the resulting network as an interactive graph.
"""
# Same LLM configuration
BASE_URL = "http://localhost:12434/engines/llama.cpp/v1"
client = OpenAI(base_url=BASE_URL, api_key="whatever", timeout=300.0)  # 5 minute timeout
MODEL_NAME = "smollm3"

# Random city names
cities = [
    "Portland", "Seattle", "Denver", "Phoenix", "Salt Lake City",
    "Las Vegas", "San Francisco", "Los Angeles", "San Diego", "Austin"
]

print("=" * 60)
print("City Distance Graph Generator")
print("=" * 60)
print(f"\nCities: {', '.join(cities)}\n")

# Build a prompt asking the LLM for distances between cities
city_pairs = []
for i in range(len(cities)):
    for j in range(i + 1, len(cities)):
        city_pairs.append((cities[i], cities[j]))

# Create a structured prompt
prompt = f"""Given these cities: {', '.join(cities)}

Please provide the approximate driving distances (in miles) between the following city pairs. 
Return ONLY a JSON object with no other text, where keys are "City1-City2" and values are distances as numbers.

Pairs needed:
{', '.join([f'{c1}-{c2}' for c1, c2 in city_pairs])}

Example format:
{{"Portland-Seattle": 174, "Seattle-Denver": 1315}}

Provide distances for all pairs:"""

print("Requesting distances from LLM...\n")

# Send to LLM
messages = [
    {"role": "system", "content": "You are a geography expert. Provide accurate approximate driving distances between US cities in JSON format."},
    {"role": "user", "content": prompt}
]

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages
)

response_text = response.choices[0].message.content.strip()
print(f"LLM Response:\n{response_text}\n")

# Try to parse the JSON response
try:
    # Extract JSON from the response (in case there's extra text)
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        distances_dict = json.loads(json_match.group())
    else:
        distances_dict = json.loads(response_text)
    
    print("Parsed distances successfully!\n")
except json.JSONDecodeError as e:
    print(f"Could not parse JSON from LLM response: {e}")
    print("Creating a sample distance dictionary instead...\n")
    # Create sample distances as fallback
    distances_dict = {}
    for city1, city2 in city_pairs:
        distances_dict[f"{city1}-{city2}"] = random.randint(200, 2000)

# Build a graph
G = nx.Graph()

# Add all cities as nodes
for city in cities:
    G.add_node(city)

# Add edges with distances as weights
for pair_key, distance in distances_dict.items():
    parts = pair_key.split('-')
    if len(parts) == 2:
        city1, city2 = parts[0].strip(), parts[1].strip()
        G.add_edge(city1, city2, weight=distance)

# Create visualization
plt.figure(figsize=(14, 10))

# Use spring layout for better visualization
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)

# Draw edges
nx.draw_networkx_edges(G, pos, width=2, alpha=0.6)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

# Draw edge labels (distances)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

plt.title("City Distance Network Graph", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('city_distance_graph.png', dpi=300, bbox_inches='tight')
print(f"Graph saved as 'city_distance_graph.png'")

# Print some statistics
print(f"\nNetwork Statistics:")
print(f"Number of cities: {len(G.nodes())}")
print(f"Number of connections: {len(G.edges())}")
print(f"\nSample distances:")
for (city1, city2), distance in list(edge_labels.items())[:5]:
    print(f"  {city1} to {city2}: {distance} miles")

plt.show()
print("\nDone!!!!")
