import json
import os

softres_dir = 'softres'
history = {}

# Iterate through each raid file in the softres directory
for filename in os.listdir(softres_dir):
    if filename.endswith('.json'):
        raid_id = filename.replace('.json', '')
        file_path = os.path.join(softres_dir, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            raid_data = json.load(f)

            # Extract reservations: usually in the 'reserved' key
            reservations = raid_data.get('reserved', [])

            for res in reservations:
                player_name = res.get('name')
                item_ids = res.get('items', []) # Extract the list of item IDs

                if player_name:
                    if player_name not in history:
                        history[player_name] = []

                    # Check if an entry for this raid_id already exists for the player
                    raid_entry_found = False
                    for raid_entry in history[player_name]:
                        if raid_entry['raidId'] == raid_id:
                            # If entry exists, extend its 'itemIds' list with new items
                            raid_entry['itemIds'].extend(item_ids)
                            raid_entry_found = True
                            break

                    if not raid_entry_found:
                        # If no entry for this raid_id, create a new one
                        history[player_name].append({
                            'raidId': raid_id,
                            'itemIds': item_ids # Store the list of item IDs
                        })

# Save the aggregated history to a file
output_file = 'softres_history.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=4)

print(f"Successfully created {output_file} with history for {len(history)} players.")
