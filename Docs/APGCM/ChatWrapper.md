
# ChatWrapper Class Documentation

## Overview

The ChatWrapper class is the main facade class for the chat wrapper module. It combines the TrimChatLog and ChatCompletionWrapper classes to provide a simple interface for chatbots.

Key features:

- Combines trimming, completion, and message management into one class
- Highly configurable with templates and parameters
- Persistence through saving and loading
- Handlers allow streaming output and saving chat logs
- Auto saving to prevent data loss

## Initialization

Creating a ChatWrapper requires an OpenAI API key, and takes several optional parameters:

```python
chat_wrapper = ChatWrapper(API_KEY, 
                           return_type="Message",
                           model=None,
                           template=None,
                           save_handler=None, 
                           is_auto_saving=True)
```

- `API_KEY`: OpenAI API key string
- `return_type`: String specifying return type of responses. Options are "Message", "str", "dict", "pretty". Default is "Message".
- `model`: String specifying OpenAI model to use. Default is None.
- `template`: Dictionary template to configure ChatWrapper. See templates.py. Default is None.
- `save_handler`: Save handler instance for persistence. Default is None.
- `is_auto_saving`: Whether to enable auto saving. Default is True.

## Core Methods

The main methods for using the ChatWrapper:

```python
# Send message and get response
response = chat_wrapper.chat(user_message) 

# Reset chat log
chat_wrapper.reset()
```

- `chat()`: Main method to get AI response. Returns response based on return_type.
- `reset()`: Resets the chat log but not the AI model.

## Setup Methods

Convenience methods to configure the ChatWrapper:

```python
# Setup from template
chat_wrapper.auto_setup_from_template(template)

# Setup trim and completion objects
chat_wrapper.auto_setup(trim_params, completion_params) 

# Change completion parameters
chat_wrapper.set_chat_completion_params(**params)
```

- `auto_setup_from_template()`: Configure based on template.
- `auto_setup()`: Manually configure trim and completion.  
- `set_chat_completion_params()`: Update completion parameters.

## TrimChatLog Methods

TrimChatLog handles trimming the chat log. Common accessors:

```python
# System prompt
prompt = chat_wrapper.system_prompt 
chat_wrapper.system_prompt = "New prompt"

# Get recent messages
msg = chat_wrapper.get_most_recent_Message() 
```

- `system_prompt`: Get/set system prompt.
- `get_most_recent_Message()`: Get most recent message object.

## Return Type

Set return type of responses:

```python
chat_wrapper.return_type = "pretty" 
```

Options are "Message", "str", "dict", "pretty".

## Saving and Loading

Requires save handler. Common methods:

```python
# Save chat wrapper
chat_wrapper.save("my_chat")

# Load chat wrapper
chat_wrapper.load("my_chat")  

# Get save names
names = chat_wrapper.all_entry_names
```

- `save() / load()`: Save to / load from entry name.  
- `all_entry_names`: Get list of save entry names.

## Handlers

Used to enable streaming and saving:

```python
# Create save handler
save_handler = JsonSaveHandler()

# Add handler  
chat_wrapper.add_save_handler(save_handler)
```

## Auto Saving

Automatically saves chat log periodically:

```python
# Enable auto saving
chat_wrapper.auto_setup_autosaving(save_handler) 

# Manually trigger save
chat_wrapper.manual_auto_save() 
```

- `auto_setup_autosaving()`: Enable and configure auto saving.
- `manual_auto_save()`: Manually trigger auto save.

## Example Usage

```python
# Create chat wrapper
chat_wrapper = ChatWrapper(API_KEY, model="gpt-3.5-turbo")

# Setup 
chat_wrapper.auto_setup()

# Add save handler
save_handler = JsonSaveHandler()
chat_wrapper.add_save_handler(save_handler)

# Chat loop
while True:
   msg = input("You: ")
   response = chat_wrapper.chat(msg)
   print(response)
```

This shows a simple usage flow:

1. Create ChatWrapper instance
2. Auto configure trim and completion
3. Add save handler for persistence
4. Chat loop to send messages and print responses

See the class docstring and docstrings for more details on all methods and features.

## Class Attributes

```python
chat_wrapper.version # Version number 
chat_wrapper.uuid # Unique ID
chat_wrapper.template # Loaded template
chat_wrapper.trim_object # TrimChatLog instance  
chat_wrapper.completion_wrapper # ChatCompletionWrapper instance
chat_wrapper.message_factory # MessageFactory instance
```

Key attributes:

- `version`: Version string of ChatWrapper class.
- `uuid`: Unique ID string generated on creation. Used for logging.
- `template`: Dictionary template if loaded.
- `trim_object`: TrimChatLog instance.
- `completion_wrapper`: ChatCompletionWrapper instance.
- `message_factory`: MessageFactory instance.

## Debugging

```python
# Print debug info
print(chat_wrapper.debug())
```

The `debug()` method prints detailed debugging information including:

- ChatWrapper configuration
- TrimChatLog info
- ChatCompletionWrapper info
- Auto saving status

## ChatCompletionWrapper

The ChatCompletionWrapper handles communicating with the OpenAI API.

Key methods:

```python
# Update parameters
chat_wrapper.set_chat_completion_params(**params) 

# Stream output
for token in chat_wrapper.stream_chat(msg):
   print(token)
```

- `set_chat_completion_params()`: Update parameters like temperature, top_p, etc.
- `stream_chat()`: Generator to stream output token-by-token.

## Templates

Templates provide an easy way to configure ChatWrapper on creation.

```python
template = {
  "model": "gpt-3.5-turbo",
  
  "trim_object": {
    "max_tokens": 1000 
  },
  
  "chat_completion_wrapper": {
    "temperature": 0.5
  }
}

chat_wrapper = ChatWrapper(API_KEY, template=template) 
```

Templates must define:

- `model`: OpenAI model to use
- `trim_object`: Parameters for TrimChatLog
- `chat_completion_wrapper`: Parameters for ChatCompletionWrapper

See `templates.py` for examples.

## Persistence

In addition to `save()` and `load()`, ChatWrapper provides lower level persistence methods:

```python
# Get save dictionary
save_dict = chat_wrapper.make_save_dict()

# Load from dict 
chat_wrapper.load_from_save_dict(save_dict)
```

- `make_save_dict()`: Generate dictionary representing state.
- `load_from_save_dict()`: Load state from dictionary.

This allows saving/loading the chat wrapper without a handler.

## Exceptions

ChatWrapper can raise various custom exceptions:

- `IncorrectObjectTypeError`: Invalid object type passed.
- `ObjectNotSetupError`: Required object not configured.
- `BadRoleError`: Invalid role string passed.
- `InvalidReturnTypeError`: Invalid return type string.
- `MissingValueError`: Required value not provided.

See `exceptions.py` for details.

## Conclusion

In summary, the ChatWrapper provides a high-level interface for chatbots by combining:

- Trimming
- Completions
- Configuration
- Persistence
- Streaming
- Automated saving

See the documentation and docstrings for full details on usage and capabilities.
