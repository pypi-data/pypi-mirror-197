# pylint: skip-file
import json
import diskcache

import sys


# export export AWS_ACCESS_KEY_ID=AKIAWX5IWZ2QCGMXX2UN AWS_SECRET_ACCESS_KEY=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

CACHE = diskcache.Cache('~/.bf2pico')

print(json.dumps(list(CACHE), indent=2))
sys.exit(1)
print(json.dumps(CACHE['active_sessions'], indent=2))
print(json.dumps(CACHE['finished_sessions'], indent=2))
sys.exit(1)
data = CACHE['svBIOT7PHdhEV4gSpKEOvRkO1od2-104202']
print(json.dumps(data, indent=2))

num_of_events = len(data.get('SessionLogs', []))

print(data['SessionLogs'][num_of_events - 1].get('SecondsRemaining', 0))
