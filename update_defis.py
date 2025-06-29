import json
from collections import OrderedDict

# Load translations lookup
with open('defisfridpt.json', encoding='utf-8') as f:
    trans = json.load(f, object_pairs_hook=OrderedDict)
lookup = {str(t['id']).zfill(3): t for t in trans}

# Load main dataset preserving order
with open('defis.json', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

missing_fr_mismatch = []

for entry in data['defis']:
    norm_id = str(entry['id']).zfill(3)
    tr = lookup.get(norm_id)
    if not tr:
        continue
    if entry.get('intitule') != tr.get('fr'):
        missing_fr_mismatch.append(norm_id)
        continue
    # Update idn
    entry['idn'] = tr['idn']
    # Insert pt before ptbr
    if 'pt' in entry:
        entry['pt'] = tr['pt']
    else:
        new_entry = OrderedDict()
        for k, v in entry.items():
            if k == 'ptbr':
                new_entry['pt'] = tr['pt']
            new_entry[k] = v
        entry.clear()
        entry.update(new_entry)

# Write back
out = json.dumps(data, ensure_ascii=False, indent=2)
with open('defis.json', 'w', encoding='utf-8') as f:
    f.write(out)

if missing_fr_mismatch:
    print('Mismatched IDs:', ', '.join(missing_fr_mismatch))
