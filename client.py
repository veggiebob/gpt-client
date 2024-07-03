import sys
import random
import json
from ai_writer import ask_raw, ask_with_messages, M_ASS, M_USER

if __name__ == '__main__':
    cmd_args = sys.argv[1:]
    bf = ''
    for line in sys.stdin:
        bf += line

    messages = json.loads(bf)
    response = ask_with_messages(messages)
    print(json.dumps(
        messages + [
            M_ASS(response)
        ]
    ))