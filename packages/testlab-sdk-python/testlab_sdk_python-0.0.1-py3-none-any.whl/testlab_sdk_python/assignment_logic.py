import datetime
import hashlib

def hash_message(message):
    # Convert the message to bytes
    message_bytes = message.encode('utf-8')

    # Hash the message using the SHA-256 algorithm
    hash_bytes = hashlib.sha256(message_bytes).digest()

    # Convert the hash bytes to a float between 0 and 1
    hash_value = int.from_bytes(hash_bytes, byteorder='big') / (2**256 - 1)

    return hash_value


def is_active(start_date, end_date):
    current_date = datetime.datetime.now()
    return start_date <= current_date <= end_date


def is_enabled(features, name, user_id):
    # Find target feature based on name
    feature = next((f for f in features['experiments'] + features['toggles'] + features['rollouts'] if f['name'] == name), None)
    if not feature:
        return False
    
    # Return false if current date is outside of date range for feature or if the feature is not running
    
    start_date = datetime.datetime.strptime(feature['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    end_date = datetime.datetime.strptime(feature['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    if not is_active(start_date, end_date) or not feature['is_running']:
        return False
    

    # Return false if the hashed ID is outside of the target user_percentage range or outside of the range of a given block
    if feature['type_id'] == 2:
        hashed_id = hash_message(user_id + name)
        return hashed_id < feature['user_percentage']
    elif feature['type_id'] == 3:
        hashed_id = hash_message(user_id)
        blocks = features['userblocks']
        block_id = int(hashed_id * len(blocks)) + 1

        return any(b['id'] == block_id and b['feature_id'] == feature['id'] for b in blocks)

    return False


def get_variant(features, name, user_id):
    hashed_id = hash_message(user_id)
    print(hashed_id)

    feature = next((f for f in features['experiments'] + features['toggles'] + features['rollouts'] if f['name'] == name), None)
    if not feature:
        return False

    variants = feature['variant_arr']
    blocks = features['userblocks']
    block_id = int(hashed_id * len(blocks)) + 1

    target_block = next((b for b in blocks if b['id'] == block_id and b['feature_id'] == feature['id']), None)
    if not target_block:
        return False

    segment_end = target_block['id'] / len(blocks)
    segment_start = segment_end - 1 / len(blocks)

    running_total = segment_start
    for variant in variants:
        running_total += float(variant['weight']) * (1 / len(blocks))
        if hashed_id <= running_total:
            return {'id': variant['id'], 'value': variant['value']}
    return False