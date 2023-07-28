import exceptions
import json 
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
from collections import namedtuple
from typing import Union, Optional, Any, List, Dict, Tuple
from pathlib import Path

templates_path = Path(__file__).parent / "templates.json"
with open(templates_path, "r") as f:
    templates = json.load(f)
"""
TO BE MOVED TO DEDICATED DOCUMENTATION FILE, (Once created)
 Args: 
        _template_dict: A dictionary of templates, with the template name as the key and the template dict as the value. The template dict must be in the following format:
        {
            "model": str,
            "name": str,
            "id" : int(should be unique, used for sorting),
            "info": dict,
                description: str,
                tags: list[str],
            "trim_object": dict (See TrimChatLog for more info),
                model: str,
                "max_tokens": int(optional but defaults to 8000),
                "token_padding": int(optional but defaults to 500),
                "max_completion_tokens": int(optional but defaults to 1000),
                "max_messages": int(optional but defaults to 200),
            "chat_completion_wrapper": dict (See ChatCompletionWrapper for more info),
                model: str(required),
                temperature: float(optional),
                top_p: float(optional),
                presence_penalty: float(optional),
                top_p: float(optional),
                frequency_penalty: float(optional),
        Note that max_completion_tokens in the trim object section refers to the same thing as max_tokens in the chat_completion_wrapper section. They are both the maximum number of tokens to use for completion. 
        See documentation for more information on these classes and their parameters
        
        Sample Dict:
         "gpt-4_default": {
        "model": "gpt-4",
        "trim_object": {
            "model": "gpt-4",
            "max_tokens": 8000,
            "token_padding": 500,
            "max_completion_tokens": 1000,
            "max_messages": 200,
        },
        "chat_completion_wrapper": {
            "model": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.7,
        },
        "info": {
            "description": "The default configuration for the gpt-4 model",
            "tags": ["gpt-4", "default", "chat"],
        },
        "name": "gpt-4_default",
        "id": 1,
    },    
            
                
                            
        }
    """


class TemplateSelector:
    """
    A class used to manage and retrieve templates, see the documentation for more info
    Dependencies:
        log_config: BaseLogger, DEFAULT_LOGGING_LEVEL
        exceptions
        typing: Union, Optional, Any, List, Dict, Tuple
        collections: namedtuple
    Raises:
        TemplateNotFoundError: Raised if the template does not exist
        BadTemplateError: Raised if the template is not valid
        


    Attributes:
        _template_dict: A dictionary of templates, with the template name as the key and the template dict as the value. Will be checked with _check_templates, see documentation for more info
        logger: A BaseLogger object, used for logging, see log_config for more info
        default_template_name: The default template name, used if no template name is specified, will raise a TemplateNotFoundError if it does not exist in the template dict
    Methods:
        Private:
            _check_templates(self, templates): Checks that the template dict is valid, raises a BadTemplateError if it is not. Each template is checked with check_template. Returns the template dict if it is valid
            _check_template(self, template: dict, template_key: str = "template"): Checks that the template is valid, raises a BadTemplateError if it is not it will raise a BadTemplateError. Returns the template dict if it is valid
        Public:
            check_template_exists(self, template_name: str) -> bool: Checks if a template exists
            get_template(self, template_name: str = None) -> dict: Returns a template dict from the template name. If no template name is specified, it will return the default template. If the template does not exist, it will raise a TemplateNotFoundError. To avoid this, use check_template_exists, or simply catch the exception
            get_template_names(self) -> list[str]: Returns a list of all template names
            search_template_by_tag(self, tag: str ) -> list[str]: Returns a list of template names that have the tag. Will return an empty list if no templates have the tag
            get_template_info(self, template_name: str = None, format: str = "dict") -> dict | str: Returns template information in a dict or string format. Possible formats: "dict", "str". String format will return the info dict formatted as a string, dict format will return the info dict. Will return the default template info if no template name is specified
            get_all_template_names(self) -> list[str]: Returns a list of all template names, including the default template name, as a list of strings
            get_template_info_from_list(self, template_list: list[str]| str, format: str = "dict") -> Union[list[dict], list[str], dict, str]: Returns template information from a list of template names or a single template name.
    Example Usage:
        template_selector = TemplateSelector(_template_dict=_template_dict)
        default_template = template_selector.get_template()
        search_results = template_selector.search_template_by_tag("chat")
        template_info = template_selector.get_template_info("gpt-4_default")
        print(template_info)
        chat_wrapper_obj = make_chat_wrapper_from_template(template_selector.get_template("gpt-4_default")) #[This function does not exist and it's final form is TBD, maybe an entire class]


    """

    def __init__(
        self, template_dict: dict, default_template_name: str = "gpt-4_default"
    ):
        self.logger = BaseLogger(
            __file__,
            filename="template_selector.log",
            identifier="template_selector",
            level=DEFAULT_LOGGING_LEVEL,
        )
        self.logger.info(f"Template Selector Initialized ")
        self._template_dict = self._check_templates(template_dict)
        self.logger.debug(
            f"{len(self._template_dict)} templates loaded, default template name: {default_template_name} "
        )
        if self.check_template_exists(default_template_name):
            self.default_template_name = default_template_name
        else:
            raise exceptions.TemplateNotFoundError(
                f"Default template name {default_template_name} does not exist in template dict"
            )

    def check_template_exists(self, template_name: str) -> bool:
        """Checks if a template exists"""
        return template_name in self._template_dict

    def _check_templates(self, _template_dict: dict) -> dict:
        """Checks that the template dict is valid, raises a BadTemplateError if it is not. Each template is checked with _check_template. Returns the template dict if it is valid"""
        if not isinstance(_template_dict, dict):
            raise exceptions.BadTemplateError("Template must be a dictionary")
        for key, template in _template_dict.items():
            self._check_template(template, key_name=key)
        return _template_dict

    def _check_template(self, template: dict, key_name: str = "template") -> dict:
        """
        Key name is the name of the key in the template dict, used for error messages. Optional, defaults to "template" but recommended to be set to the key name in the template dict
        Checks that the template is valid, raises a BadTemplateError if it is not it will raise a BadTemplateError. Returns the template dict if it is valid This is a private method, it should not be called outside of the class. It is also fairly long, but the majority of it is just defining the possible keys and their types.
        Be sure to add new keys to the dictionaries if the template format is updated. Extra keys will not cause an error, but missing keys will(unless they are optional, see the PosKeyInfo namedtuple for more info)
        Returns the template dict if it is valid
        """
        """Sample Dict:
         "gpt-4_default": {
        "model": "gpt-4",
        "trim_object": {
            "model": "gpt-4",
            "max_tokens": 8000,
            "token_padding": 500,
            "max_completion_tokens": 1000,
            "max_messages": 200,
        },
        "chat_completion_wrapper": {
            "model": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.7,
        },
        "info": {
            "description": "The default configuration for the gpt-4 model",
            "tags": ["gpt-4", "default", "chat"],
        },
        "name": "gpt-4_default",
        "id": 1,
        },
        """
        if not isinstance(template, dict):
            self.logger.error(f"{key_name} Template must be a dictionary")
            raise exceptions.BadTemplateError(
                f"{key_name}Template must be a dictionary"
            )

        required_keys = {
            "model": str,
            "name": str,
            "id": int,
            "info": dict,
            "trim_object": dict,
            "chat_completion_wrapper": dict,
        }
        info_dict_keys = {
            "description": str,
            "tags": list,
        }
        # required: bool , type: type, key: str
        PosKeyInfo = namedtuple("PosKeyInfo", ["key", "type", "required"])

        possible_keys_trim = {
            "model": PosKeyInfo("model", str, True),
            "max_tokens": PosKeyInfo("max_tokens", int, False),
            "token_padding": PosKeyInfo("token_padding", int, False),
            "max_completion_tokens": PosKeyInfo("max_completion_tokens", int, False),
            "max_messages": PosKeyInfo("max_messages", int, False),
        }
        possible_keys_chat = {
            "model": PosKeyInfo("model", str, True),
            "max_tokens": PosKeyInfo("max_tokens", int, False),
            "temperature": PosKeyInfo("temperature", float, False),
            "presence_penalty": PosKeyInfo("presence_penalty", float, False),
            "frequency_penalty": PosKeyInfo("frequency_penalty", float, False),
            "top_p": PosKeyInfo("top_p", float, False),
        }

        for key, value in required_keys.items():
            if key not in template:
                raise exceptions.BadTemplateError(
                    f"{key_name} Template must have a {key} key"
                )
            if not isinstance(template[key], value):
                raise exceptions.BadTemplateError(
                    f"{key_name}Template {key} must be a {value}"
                )
        template_info = f"{key_name} : {template['name']}"
        for key, value in info_dict_keys.items():
            if key not in template["info"]:
                raise exceptions.BadTemplateError(
                    f"{template_info} :Template info must have a {key} key"
                )
            if not isinstance(template["info"][key], value):
                raise exceptions.BadTemplateError(
                    f"{template_info} : Template info {key} must be a {value}"
                )
        for key, value in possible_keys_trim.items():
            if key not in template["trim_object"]:
                if value.required:
                    raise exceptions.BadTemplateError(
                        f"{template_info} : Template trim_object must have a {key} key"
                    )
                else:
                    continue
            if not isinstance(template["trim_object"][key], value.type):
                raise exceptions.BadTemplateError(
                    f"{template_info} : Template trim_object {key} must be a {value.type}"
                )
        for key, value in possible_keys_chat.items():
            if key not in template["chat_completion_wrapper"]:
                if value.required:
                    raise exceptions.BadTemplateError(
                        f"{template_info} : Template chat_completion_wrapper must have a {key} key"
                    )
                else:
                    continue
            if not isinstance(template["chat_completion_wrapper"][key], value.type):
                raise exceptions.BadTemplateError(
                    f"{template_info}: Template chat_completion_wrapper {key} must be a {value.type}"
                )
        return template

    @property
    def default_template(self) -> dict:
        return self.get_template()

    def get_template(self, template_name: str = None) -> dict:
        """Returns a template dict from the template name
        If no template name is specified, it will return the default template
        If the template does not exist, it will raise a TemplateNotFoundError
        To avoid this, use check_template_exists, or simply catch the exception
        """
        if template_name is None:
            template_name = self.default_template_name
        if not self.check_template_exists(template_name):
            raise exceptions.TemplateNotFoundError(
                f"Template {template_name} does not exist"
            )
        return self._template_dict[template_name]

    def add_template(self, name: str, template: dict) -> None:
        """Adds a template to the template dict
        Args:
            name: The name of the template
            template: The template dict
        """

        self._check_template(template)
        self._template_dict[name] = template
        self.logger.debug(f"Added template {name} to template dict")

    def get_template_names(self) -> list:
        """Returns a list of all template names"""
        return list(self._template_dict.keys())

    def search_template_by_tag(self, tag: str) -> list[str]:
        """Returns a list of template names that have the tag
        Will return an empty list if no templates have the tag
        """
        result = [
            template_name
            for template_name, template in self._template_dict.items()
            if tag in template["info"]["tags"]
        ]
        self.logger.debug(f"Search for tag {tag} returned {len(result)} results")
        return result

    def get_template_info(
        self, template_name: str = None, format: str = "dict"
    ) -> dict | str:
        """Returns template information in a dict or string format
        Possible formats: "dict", "str"
        String format will return the info dict formatted as a string, dict format will return the info dict
        Will return the default template info if no template name is specified

        """
        possible_formats = ["dict", "str"]
        if format not in possible_formats:
            raise exceptions.BadTemplateError(
                f"Format must be one of {possible_formats}"
            )
        if format == "dict":
            return self.get_template(template_name)["info"]
        elif format == "str":
           
            info_dict = self.get_template(template_name)["info"]
            indent = "  "
            description = f"{indent}Description: {info_dict['description']}"
            tags = f"{indent}Tags: {', '.join(info_dict['tags'])}"
            result = [
                f"Template: {template_name}",
                description,
                tags,
            ]
            return "\n".join(result)
            

    def get_all_template_names(self) -> list[str]:
        """Returns a list of all template names, including the default template name, as a list of strings"""
        return list(self._template_dict.keys())

    def get_template_info_from_list(
        self, template_list: list[str] | str, format: str = "dict"
    ) -> Union[list[dict], list[str], dict, str]:
        """
        Returns template information from a list of template names or a single template name
        Args:
            template_list: A list of template names or a single template name
            format: The format to return the template info in, either "dict" or "str". If a list is passed, it will return a list of the specified format. String format will return the info dict formatted as a string, dict format will return the info dict
        """
        possible_formats = ["dict", "str"]
        if format not in possible_formats:
            raise exceptions.BadTemplateError(
                f"Format must be one of {possible_formats}"
            )
        if not isinstance(template_list, list):
            return self.get_template_info(template_list, format)

        return [
            self.get_template_info(template_name, format)
            for template_name in template_list
        ]

    def __repr__(self):
        return f"TemplateSelector(template_dict={self._template_dict}, default_template_name={self.default_template_name}) With {len(self._template_dict)} templates"

   

    def __len__(self):
        return len(self._template_dict)
    def __str__(self):
        return self.pretty_format_templates()
    def _format_template(self, template_dict: dict) -> str:
        """Returns a formatted string of a template"""
        template_dict = self._check_template(template_dict)
        result = ""
        for key, value in template_dict.items():
            result += f"{key}:\n"
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    result += f"  {subkey}: "
                    if isinstance(subvalue, list):
                        result += ", ".join(subvalue) + "\n"
                    elif isinstance(subvalue, dict):
                        for subsubkey, subsubvalue in subvalue.items():
                            result += f"\n    {subsubkey}: {subsubvalue}"
                        result += "\n"
                    else:
                        result += f"{subvalue}\n"
            else:
                result += f"  {value}\n"
        return result

    def pretty_format_templates(self):
        """Returns a formatted string of all templates"""
        msg_list = []
        for name, template in self._template_dict.keys():
            msg_list.append(f"Template: {name}")

            msg_list.append(self._format_template(template))

            msg_list.append("\n")

        return "\n".join(msg_list)
template_select = TemplateSelector(template_dict=templates)