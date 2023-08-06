#%%
import json
import os
import re
import time

import openai
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown, MarkdownIt
from rich.table import Table
from rich.panel import Panel
from rich.logging import RichHandler
import logging
import pyperclip
import readline

logger = logging.getLogger(__name__)
handler = RichHandler()

# Set the logging level and add the handler to the logger
logger.setLevel(logging.INFO)
logger.addHandler(handler)


c = Console(color_system="truecolor", soft_wrap=True)


class CLIGPT:
    def __init__(self, openai_api_key, config_file, stream=True, proxy=None, context_length=6, auto_copy=True):
        with open(config_file, 'r') as f:
            self.configs = json.load(f)
        openai.api_key = openai_api_key
        if proxy:
            openai.proxy = proxy
            # proxy="http://127.0.0.1:7890" # http proxy
        self.context_length = context_length
        self.context_buffer = []
        self.roles = [key for key in self.configs]
        self.default_role_index = 0
        self.delay_time = 0.001
        self.stream = stream
        self.auto_copy = True
        self.welcome()

    def welcome(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Role", style="dim")
        table.add_column("System", style="dim")
        c.print(f'OpenAI proxy: {openai.proxy}.')
        c.print(f'Loaded configs from ~/.cligpt/config.json.')
        for key in self.configs:
            table.add_row(f"{key}", f"{self.configs[key]}")
        c.print(table)
        l1 = f"Use @roles to switch role (e.g., @p or @proofread)."
        l2 = f"End your input with [Enter], except in @code mode with [Ctrl]+[D]."
        l3 = f"Contexts are `remembered` for the past {self.context_length} prompts/responses. "
        l4 = f"Contexts will be reset once roles switched."
        c.print(Panel(f"{l1}\n{l2}\n{l3}\n{l4}", width=c.width))

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
                    self.context_buffer = []
                    continue
                self.context_buffer.append(user_input)
                self.context_buffer = self.context_buffer[-self.context_length:]
                user_input = ' '.join(self.context_buffer)
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

                    # # comment because markdown doesn't support soft wrap
                    # md = Markdown("")
                    # parser = MarkdownIt().enable("strikethrough")
                    # with Live(md, auto_refresh=False) as lv:
                    #     for event in response:
                    #         event_text = event['choices'][0]['delta']
                    #         content = event_text.get('content', '')
                    #         answer += content
                    #         md.markup = answer
                    #         md.parsed = parser.parse(md.markup)
                    #         lv.refresh()
                    #         time.sleep(self.delay_time)
                    # response_text = ''.join(answer)
                    c.print(f"[bold deep_sky_blue3]@GPT: ", end="")
                    for event in response:
                        event_text = event['choices'][0]['delta']
                        content = event_text.get('content', '')
                        c.print(content, end='')
                        answer += content
                        time.sleep(self.delay_time)
                    response_text = ''.join(answer)
                    if self.auto_copy:
                        pyperclip.copy(response_text)
                    c.print('\n')
                else:
                    response_text = response.choices[0].message.content
                    c.print(Markdown(response_text))

                self.context_buffer.append(response_text)
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
