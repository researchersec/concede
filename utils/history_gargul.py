import json
import os

if os.path.exists('gargulexport.json'):
    with open('out.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    gargul_history = {}

    for entry in data:
        raid_id = entry.get('softresID', 'unknown_raid')
        player_full_name = entry.get('awardedTo')
        item_id = entry.get('itemID')
        # Extract rolls associated with this specific item award
        item_rolls = entry.get('Rolls', [])

        if player_full_name and item_id and entry.get('received') is True:
            # Strip server name if present
            player_name = player_full_name.split('-')[0]

            if player_name not in gargul_history:
                gargul_history[player_name] = []

            # Group by raidId
            raid_entry = next((item for item in gargul_history[player_name] if item['raidId'] == raid_id), None)

            item_record = {
                'itemId': item_id,
                'rolls': item_rolls
            }

            if raid_entry:
                raid_entry['items'].append(item_record)
            else:
                gargul_history[player_name].append({
                    'raidId': raid_id,
                    'items': [item_record]
                })

    output_file = 'gargul_history.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gargul_history, f, indent=4, ensure_ascii=False)

    print(f'Successfully created {output_file} with history and rolls for {len(gargul_history)} players.')
else:
    print('Error: out.json not found.')
