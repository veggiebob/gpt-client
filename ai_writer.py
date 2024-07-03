import os

from openai import OpenAI
import datetime

OPENAI_KEY = open('openai-key.private', 'r').readline().strip()
client = OpenAI(api_key=OPENAI_KEY)

M_USER = lambda x: {'role':'user', 'content':x}
M_SYS = lambda x: {'role':'system', 'content':x}
M_ASS = lambda x: {'role':'assistant', 'content':x}

class AIResponse:
    def __init__(self, response: str, args: tuple[str], messages: list, api_response: dict):
        self.response = response
        self.args = args
        self.messages = messages
        self.api_response = api_response

class AIResponseLogger:
    def __init__(self, filename: str, dir: str=''):
        # set filename using current date and parameter
        now = datetime.datetime.now()
        filename = now.strftime('%Y-%m-%d-%H-%M-%S') + '-' + filename
        self.filename = os.path.join(dir, filename)

    def log(self, user_msg: str, ai_response: AIResponse):
        with open(self.filename, 'a') as f:
            f.write('-'*80 + '\n')
            f.write(f'User: {user_msg}\n')
            for msg in ai_response.messages[2:]:
                f.write(f'{msg["role"]}: {msg["content"]}\n')
            f.write('\nParsed args: [' + ', '.join(ai_response.args) + ']\n')

    def log_plain(self, user_msg: str, ai_response: str):
        with open(self.filename, 'a') as f:
            f.write('-'*80 + '\n')
            f.write(f'User: {user_msg}\nAI: {ai_response}\n\n')

def ask_raw(user_msg: str, **kwargs) -> str:
    response = client.chat.completions.create(model='gpt-3.5-turbo',
    messages=[
        M_USER(user_msg)
    ],
    **kwargs)
    return ''.join(response.choices[0].message.content)

def ask_with_messages(msgs: list, **kwargs) -> str:
    """
    Should be in the format
    [
        {
            role: 'user'|'assistant'|'system',
            content: string
        }
    ]
    :param msgs:
    :param kwargs:
    :return:
    """
    response = client.chat.completions.create(model='gpt-3.5-turbo',
    messages=msgs,
    **kwargs)
    return ''.join(response.choices[0].message.content)
