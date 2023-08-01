# TemplateSelector

The TemplateSelector class provides functionality for managing and selecting templates for chatbot configurations.

## Overview

The TemplateSelector is initialized with a dictionary of templates:

```python
template_dict = {
  "template1": {...},
  "template2": {...} 
}

selector = TemplateSelector(template_dict)
```

It provides methods to:

- Get a template by name
- Check if a template exists
- Get all template names
- Search templates by tags
- Get template info in different formats

## Template Format

The templates are dictionaries with the following structure:

```python
{
  "model": "model_name",
  
  "trim_object": {...}, 
  
  "chat_completion_wrapper": {...},

  "info": {
    "description": "Some details",
    "tags": ["tag1", "tag2"]
  },

  "name": "template_name"
} 
```

Required keys are "model", "name", "id", "info", "trim_object", and "chat_completion_wrapper".

See method `_check_template()` for detailed validation.

## Methods

### `get_template(name)`

Get a template by name.

Returns the default template if no name provided.

Raises `TemplateNotFoundError` if template does not exist.

### `check_template_exists(name)`

Checks if a template with the given name exists.

Returns `True/False`.

### `search_templates_by_tag(tag)`

Returns a list of template names containing the given tag.

### `get_template_info(name, format)`

Get template info dict or string for a name.

`format` can be `"dict"` or `"string"`

### `add_template(name, template)`

Add a new template dict with the given name.

Template is validated before adding.

## Properties

- `default_template`: Name of default template
- `default_template_name`: Get default template dict

## Private Methods

- `_check_templates(templates)`: Validate full template dict
- `_check_template(template)`: Validate a single template dict

## Template Validation

The `TemplateSelector` performs basic validation on the structure and types of the template dictionaries.

It does **not** do full validation of all parameters.

For example, it will check:

- Temperature is a float
- But not that it is within the valid range of 0-2

So invalid values may pass the `TemplateSelector` checks but then fail when creating the `ChatWrapper` object.

The main validations are:

- Required keys exist
- Values are expected types
- Info and parameter sub-dicts have required keys

But it does not validate:

- Ranges of numerical values
- Options for string values
- Details of trim and chat completion objects

So the templates should still be created carefully to avoid errors.

The `_check_template` method performs this limited validation.

Full validation occurs later when actually creating the chatbot with the template.
