#%%
import json
import os
import re
import time

import openai
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown, MarkdownIt

c = Console(color_system="truecolor")


class CLIGPT:
    def __init__(self, openai_api_key, config_file, stream=True):
        with open(config_file, 'r') as f:
            self.configs = json.load(f)
        openai.api_key = openai_api_key
        self.history_length = 6
        self.history_buffer = []
        self.roles = [key for key in self.configs]
        self.default_role_index = 0
        self.delay_time = 0.001
        self.stream = stream
        self.welcome()

    def welcome(self):
        print(f'==> Loaded configs from ~/.cligpt/config.json:')
        for key in self.configs:
            print(f"    {key}: {self.configs[key]}")
        # c.print(Markdown("---"))
        print(f'==> Use @roles to switch role (e.g., @p or @proofread). End your input with [Enter], except in @code mode with [Ctrl]+[D].')
        print(f'==> Sessions are `remembered` for the past {self.history_length} prompt/response. Sessions will be reset once roles switched.')
        c.rule(style='grey46')


    def read_multiline(self) -> str:
        contents = []
        while True:
            try:
                line = input("> ")
            except EOFError:
                c.print("--- EOF ---")
                break
            except KeyboardInterrupt:
                return ""
            contents.append(line)
        return "\n".join(contents)

    def start(self):
        while True:
            try:
                if self.roles[self.default_role_index] == '@code': # (end with Ctrl+D)
                    user_input = self.read_multiline()
                else:
                    with c.capture() as capture:
                        c.print(f"[bold pale_violet_red1]{self.roles[self.default_role_index]}:[/] ", end="")
                    user_input = input(capture.get())
                if user_input in ['q', 'exit']:
                    break
                # check if user_input starts with @
                if user_input.startswith('@'):
                    user_input = re.sub(r'\n', '', user_input)
                    for role in self.roles:
                        if user_input in role:
                            self.default_role_index = self.roles.index(role)
                            break
                    self.history_buffer = []
                    continue
                self.history_buffer.append(user_input)
                self.history_buffer = self.history_buffer[-self.history_length:]
                user_input = ' '.join(self.history_buffer)
                if self.roles[self.default_role_index] == '@generic':
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{
                                                    "role": "user",
                                                    "content": f"{user_input}"
                                                }], stream=self.stream)
                else:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                            messages=[{
                                                                "role": "system",
                                                                "content": f"{self.configs[self.roles[self.default_role_index]]}"
                                                            }, {
                                                                "role": "user",
                                                                "content": f"{user_input}"
                                                            }], stream=self.stream)

                if self.stream == True:
                    answer = ''
                    md = Markdown("")
                    parser = MarkdownIt().enable("strikethrough")
                    with Live(md, auto_refresh=False) as lv:
                        for event in response:
                            event_text = event['choices'][0]['delta']
                            content = event_text.get('content', '')
                            answer += content
                            md.markup = answer
                            md.parsed = parser.parse(md.markup)
                            lv.refresh()
                            time.sleep(self.delay_time)
                    response_text = ''.join(answer)
                    # print('\n')
                else:
                    response_text = response.choices[0].message.content
                    c.print(Markdown(response_text))

                self.history_buffer.append(response_text)
                # c.print(Markdown("---", )
                c.rule(style='grey46')
            except KeyboardInterrupt:
                c.print('See you soon!')
                break
            except EOFError as e:
                c.print("See you soon!")
                break            


if __name__ == '__main__':
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not provided, please `export OPENAI_API_KEY=[Your API KEY]`")

    config_file = os.path.join('.', 'config.json')
    cligpt = CLIGPT(openai_api_key=OPENAI_API_KEY, config_file=config_file)
    cligpt.start()
