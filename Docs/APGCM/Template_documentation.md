# Template Documentation

In the ChatWrapper system, Templates are used to ease the creation of ChatWrapper objects. These templates contain preconfigured settings for models and use cases. The key components of the Template System are the `TemplateSelector` class, `ChatFactory` class, and the Template File.

| Component | Description |
|-----------|-------------|
| TemplateSelector Class | This class performs basic validation of the template file and provides methods to retrieve templates.|
| ChatFactory Class | This class is designed to create ChatWrapper objects from templates.|
| Template File | This is a JSON file which is the actual template for creating ChatWrapper objects.|

## TemplateSelector Class

The `TemplateSelector` class is primarily designed to verify the template file. It comes with an instance, *template_select*, preloaded with all built-in templates from templates.json. You can create a new instance and load it with a template dictionary of your choice.

**Caution:** This class verifies the template dictionary but doesn't validate the templates. For instance, incorrect parameters for the model will not be caught by this class, instead they will be caught by the `ChatFactory` class. It's recommended to check the model's documentation for valid parameters.

## ChatFactory Class

The `ChatFactory` class facilitates the creation of ChatWrapper objects from templates. By default, it uses preconfigured settings but you can override these settings by passing arguments to the constructor.

This class provides several convenience methods for working with templates:

- `.select_template()`: Selects a template. Requires the template name as a string.
- `.get_chat()`: Creates a ChatWrapper object. Uses the default template if no template name is specified.

## Template File

The template file, `template.json`, serves as the default template and is located in the templates folder. It provides a JSON representation of the template to be used for creating the `ChatWrapper` objects.

A helper script, `reload_temps.py`, is provided to reload the default built-in templates. It's located in the templates folder as well.

## Template Format

Here's an example of a template structure:

```json
"gpt-4_default": {
    "model": "gpt-4",
    "trim_object": {
        "model": "gpt-4",
        "max_tokens": 8000,
        "token_padding": 500,
        "max_completion_tokens": 1000,
        "max_messages": 200
    },
    "chat_completion_wrapper": {
        "model": "gpt-4",
        "max_tokens": 1000,
        "temperature": 0.7
    },
    "info": {
        "description": "The default configuration for the gpt-4 model",
        "tags": ["gpt-4", "default", "chat"]
    },
    "name": "gpt-4_default",
    "id": 1
}
```

| Field | Description |
|-------|-------------|
| model | The model to be used for the ChatWrapper. |
| trim_object | It is used to trim chat logs to a certain number of tokens, messages, etc. |
| chat_completion_wrapper | Manages parameters and makes API calls to the OpenAI API. |
| info | Contains meta information about the template such as description and tags. |
| name | Name of the template. |
| id | Unique identifier for the template. |

## Docstrings

Detailed explanations of the functionality of `TemplateSelector` and `ChatFactory` classes can be found in their respective docstrings within the source code.
