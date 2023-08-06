# Command Line Inferface for ChatGPT

### Installation 
```shell
pip install --upgrade cligpt
```

### Getting Started
```shell
# Fill in your OpenAI API key
export OPENAI_API_KEY=[sk-xxxx]

# Launch
cligpt

# Switch roles (you may use abbreviations as long as they do not clash with other roles)
@revise (or @revis | @revi | @rev | @re | @r)
```

### Advanced Options

- Customize your roles
    
    Edit the configuration file:
    ```
    vim ~/.cligpt/config.json
    ```

- Turn on/off Auto-copy (default=on)
    
    `cligpt` automatically copies the last response to your clipboard. To enable/disable it, launch `cligpt` with the following command:
    ```
    cligpt --no_auto_copy
    ```
- Adjust context length (default=6)
    
    Context length refers to the number of prompts+responses `cligpt` should remember. For example, if you want it to remember the last 3 prompts + 3 responses, launch `cligpt` with the following command:
    ```
    cligpt --context_length=6
    ```

- Turn on/off stream mode (default=on)

    Stream mode displays words popping up one by one. To enable/disable it, launch `cligpt` with the following command:
    ```
    cligpt --no_stream
    ```
- Proxy (default=None)

    Use a proxy for the OpenAI API:

    ```
    cligpt --proxy=http:127.0.0.1:9000
    ```



### Uninstallation
```shell
pip uninstall cligpt
(rm -rf ~/.cligpt)
```
