# Notes On APGCM 

The documentation for this module is currently not finished. Much is left out as of now. This will hopefully be fixed in the future.

## What is APGCM?

APGCM stands for *Alex's Pretty Good Chat Module*. I am a beginner python developer, and this project was primarily for learning. However, I imagined during development it being used by other developers, so its made with that in mind.

The system is designed to be highly customizable and extendable. It's interface and file system agnostic, meaning it can be used in any project that requires a chatbot. Here's a quick example of creating a CLI chatbot with APGCM in just a few lines of code:

```python
import APGCM
def save_entry(chat_wrapper: APGCM.ChatWrapper) -> None:
    """Saves the chat log and provides user feedback"""
    while True:
        overwrite = False
        filename = input("Enter a filename: ")
        if chat_wrapper.check_entry(filename):
           print("File already exists. Do you want to overwrite it?")
            overwrite = input("Y/N: ").lower() == "y"
            if overwrite is False:
                continue
        chat_wrapper.save_entry(filename, overwrite=overwrite)
        print("Chat saved successfully!")
        return 
def load_entry(chat_wrapper: APGCM.ChatWrapper) -> None:
    """Loads the chat log and provides user feedback"""
    while True:
        filename = input("Enter a filename: ")
        if chat_wrapper.check_entry(filename):
            chat_wrapper.load_entry(filename)
            print("Chat loaded successfully!")
            return
        print("File does not exist. Try again.")
        
factory = APGCM.ChatFactory()
factory.select_template("gpt-4_creative")
chat = factory.get_chat()
save_handler = APGCM.handlers.SaveHandler.JsonSaveHandler()
chat.add_save_handler(save_handler)
while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    if user_input == "save":
        save_entry(chat)
        continue
    elif user_input == "load":
        load_entry(chat)
        continue
    else:
        print("Bot: " + chat.chat(user_input))

  
```

As you can see, its pretty simple to create chatbots using this module. The module will automatically keep track of the chat history, trimming it when necessary. It also provides a convenient way to save and load chat logs.
It includes an autosaving feature as well

## Key Parts of APGCM

### `TrimChatLog` class

 This class is responsible for trimming the chat log, keeping it under the max token limit for the module, while attempting to cram as many messages as possible in the chat log. It uses several subclasses to handle this task:

* `Chatlog` - This class is responsible for storing the full chat history, and provides methods to manage the history. It is a child of the AbstractChatlog class allowing for the creation of chatlogs that use different data structures.(eg, database, json file, etc). It is also optional -- simply use trim_chat_log.`add_chatlog(None)` to disable this feature
* `Message` and `MessageFactory`- The message class is a user dict meant to manage the messages. It will automatically count the tokens on creation, and create a pretty representation of the message. The message factory is a callable class that allows for setting the role and model(used for token counting) of the message. Factories can be retrieved using the `.get_message_factory()` method of the trim_chat_log class.
* `SystemPrompt` and `Reminder` both work similarly. They handle token counting and adding "wildcards" to the prompts. System prompts are prepended to the chat log, while the reminder gets the prepend `System Reminder:` and is appended to the end of the chat log. The wildcards are:
        | Wildcard | Description |
        |----------|-------------|
        |`||cut_off||` | Is always replaced with September 21, 2021, the last time GPT has had its training data updated. |
        |`||date||` | Is replaced with the current date. |
        |`||time||` | Is replaced with the current time. |
        |`||model||` | Is replaced with the model name. |
    Wild cards can be easily added by modifying the `wildcards` dictionary in the `SystemPrompt` and `Reminder` classes.
* The class's main method is the `.get_finished_chatlog()` that will output a properly formatted list of dictionaries to be sent off to the model
* Class will automatically count the maximum tokens that can be included in the chat log by subtracting the `max_completion_tokens`, the tokens in both the system prompt and reminder, and a special token padding value from the maximum from the model.
* According to my tests, its relatively efficient. Its able to process 10K messages in just over .1 seconds.

### `ChatCompletionWrapper` class

This class wraps the openai `ChatCompletion` end point, while using a subclass called `ModelParameters` to validate and keep track of model parameters and their values. Supports streaming from the `.stream_chat` and the `.chat` method if a stream output handler has been added and streaming is true.

### `ChatWrapper` class

The meat and potatoes of this project. It is the primary facade class for this entire module, and combines the `ChatCompletionWrapper` and `TrimChatLog` classes to provide a simple interface for creating chatbots. It also provides a convenient way to save and load chat logs, using a save handler system. It also includes an autosaving feature as well.

### `ChatFactory` class

Provides a simple way to create `ChatWrapper` objects from templates. Templates can be custom made and loaded into a `TemplateSelector` instance. By default it uses a pre-made `TemplateSelector` class loading with built in templates from the `templates.json` file.

## Closing Notes

If you find this module useful, please let me know! I am bringing this project to a close for now, but if even one person finds it useful or is interested in it I will keep working on it.

Thanks for giving this module a look, and Happy Chatting!
