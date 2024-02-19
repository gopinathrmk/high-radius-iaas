hycu_policy_map = "@@{hycu_policy_map}@@"
print(",".join([x['name'] for x in json.loads(hycu_policy_map)]))