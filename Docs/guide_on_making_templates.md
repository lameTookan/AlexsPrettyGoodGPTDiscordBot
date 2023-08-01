# Step-by-Step Guide to Creating Templates

## Introduction

In this guide, we'll walk you through creating `ChatWrapper` objects using templates. These templates are saved in the `templates.json` file within the template directory. Don't hesitate to create your own templates - the worst-case scenario is that you encounter an error message. If you happen to disrupt the `templates.json` file, there's a script named `reload_temps.py` in the template directory to revert to the default templates and back up your old file as `templates.json.bak`.

## Understanding ChatWrapper

`ChatWrapper` is the principal class that unifies this project. It's not necessary to understand it in-depth unless you plan to use it directly (i.e., programming with it). The key takeaway is that it facilitates communication with a GPT model.

`ChatWrapper` manages two main classes:

1. `TrimChatLog`: This class maintains your chat history. Given that the GPT model doesn't remember past interactions, your chat history must be included in each call for continuity. However, GPT models have a maximum input length, so the chat history must be trimmed to fit. `TrimChatLog` handles this for you.

2. `ChatCompletionWrapper`: This class is responsible for making API calls to the GPT model. It also manages a few model parameters and ensures they are valid before making the API call.

The `ChatWrapper` class, therefore, wraps these other classes to streamline the use of the GPT model, with each class having their own settings. The template system aids in creating these objects more easily.

## A Quick Overview of JSON

JSON (JavaScript Object Notation) is a straightforward method of storing data in a file, making it easy for programs to work with it. Despite its name, it isn't limited to just JavaScript and serves as a language-independent data format.

JSON data is written as key/value pairs, with key being a string and the value being a string, number, object, array, boolean, or null. JSON also supports more complex data structures like arrays and nested objects.

**Note**: JSON is strict in its formatting. All strings must be in double quotes, data must be separated by commas (but not after the last item in an object or array), and your JSON data should always be validated.

## Basic Template Structure

Templates have a few core components:

* `name`: The template's name, which should match the key in the `templates.json` file.
* `model`: The model to be used.
* `info`: A nested dictionary containing details about the template. These values can be left blank to avoid errors if an implementation wants to show users this information. It requires two nested keys:
  * `description`: A brief explanation of the template.
  * `tags`: A list of tags that describe the template.

Next, we have the two primary parts of the template - the parameters (settings) for the previously mentioned objects.

## Key Points

The `TrimChatLog` and `ChatCompletionWrapper` classes define the terms `max_tokens` and `max_completion_tokens` differently as they are used for different purposes.

### TrimChatLog Parameters

The parameters for `TrimChatLog` should be a nested dictionary with the key `trim_object`. It's advisable to include all of these keys, though `model` is the only required one.

* `model`: The model to use.
* `max_tokens`: The maximum number of tokens that the model can handle in a single call. This trims the chat history to fit the model's input length. It must be set to a value below the model's maximum input length.
* `max_completion_tokens`: The maximum length of the model's output. It should be at least the `max_token` value in the `ChatCompletionWrapper` parameters, but can be higher.
* `max_messages`: The maximum number of messages that can be included in the chat history. This is more about performance than any model limitation.
* `token_padding`: An extra allowance to account for any token counting errors or additional tokens sent over in the parameters.

### ChatCompletionWrapper Parameters

The parameters for `ChatCompletionWrapper` should also be a nested dictionary, with the key `chat_completion_wrapper`.

* `model`: The model to use.
* `max_tokens`: The maximum number of tokens the model can generate.
* `temperature`: The model's temperature.
* `top_p`: The model's top p value.
* `frequency_penalty`: The model's frequency penalty.
* `presence_penalty`: The model's presence penalty.

## Example Templates

```json
 "gpt-3.5-16k_default": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_default",
        "id": 5,
        "info": {
            "description": "The default configuration for the gpt-3.5-16k model",
            "tags": [
                "gpt-3.5-16k",
                "default",
                "chat"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 0.7
        }
    },
    "gpt-3.5-16k_creative": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_creative",
        "id": 6,
        "info": {
            "description": "Creative Mode for the gpt-3.5-16k model",
            "tags": [
                "gpt-3.5-16k",
                "creative",
                "chat",
                "high temperature"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 1.0
        }
    },
```

## Final Notes

Creating your own templates is encouraged. Remember that templates will be checked for correct data types and keys upon loading; however, this doesn't guarantee the template will function. If loading a template fails, an error message will be printed.

To reload the default templates, execute the `reload_temps.py` script in the template directory. This will also back up your old `templates.json` file as `templates.json.bak`.

```bash
python3 templates/reload_temps.py
```

Enjoy your conversations!
