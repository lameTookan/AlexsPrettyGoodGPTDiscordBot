import exceptions
from settings import settings_bag as settings
from typing import Callable, Union, Optional, Any
from chat_wrapper import ChatWrapper
from templates.template_selector import template_select, TemplateSelector
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL

"""
An example of a template:
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


class ChatFactory:
    """A relatively simple factory class for creating chat wrapper objects from templates. These are common configurations for various models and use cases. Simplifies all of the nested objects and settings that ChatWrapper requires(eg model params, token info, etc).
    See documentation and docstrings for more information on how the template system works. Or see the template directory for a list of possible templates(built in ones at least)
    Dependencies:
        Custom:
            chat_wrapper.ChatWrapper -> Object this factory creates(and its dependencies)
            templates.TemplateSelector -> The template selector object for selecting templates(defaults to an instance loaded with built in templates from templates/template.json)
            settings -> Settings for the program, used for OPENAI_API_KEY
            exceptions -> Custom exceptions
            log_config -> Logging object for logging, BaseLogger(pre-configured logging object ) and DEFAULT_LOGGING_LEVEL
        Python:
            Typing -> For type hinting
    Raises:
        exceptions.IncorrectObjectTypeError: Raised if the template selector object is not a TemplateSelector object
        ChatWrapper can raise exceptions from corrupt templates and template selector will raise a TemplateNotFoundError if the template is not found

    Args:
        template_selector (TemplateSelector, optional): The template selector object for selecting templates(defaults to an instance loaded with built in templates from templates/template.json). Defaults to template_select.
        API_KEY (str, optional): The API key to use for the chat wrapper objects. Defaults to settings.OPENAI_API_KEY.
        default_template_name (str, optional): The default template name to use when creating a chat wrapper object. Defaults to settings.DEFAULT_TEMPLATE_NAME.
        model (str, optional): The model to use for the chat wrapper objects. Defaults to settings.DEFAULT_MODEL.

    Properties:
        Objects:
            template_selector (TemplateSelector): The template selector object for selecting templates
            logger (BaseLogger): The logger object for logging(pre-configured logging object )
        Other:
            selected_template (dict): The currently selected template, defaults to the default template name
            default_template_name (str): The default template name to use when creating a chat wrapper object
            API_KEY (str): The API key to use for the chat wrapper objects
            model (str): The model to use for the chat wrapper objects
    Methods:
        Core/Public:
            -select_template(template_name: str ) -> None: Selects a template from the template selector, stores it in the selected_template property. Will raise a -TemplateNotFoundError if the template is not found
            -get_chat() -> ChatWrapper: Returns a chat wrapper object from the selected template
            -search_templates_by_tag(tag: str ) -> list[str]: Searches the templates for a tag, returns a list of template names that have the tag
            -get_template_info(name: str, format = "dict" ) -> dict | str: Gets the info for a template, returns a dictionary with the info
            -check_if_template_exists(name: str ) -> bool: Checks if a template exists, returns True if it does, False otherwise
        Private:
            -_make_chat(template: dict) -> ChatWrapper: Makes a chat wrapper object from a template
    Example Usage:
        factory = ChatFactory()
        chat_wrapper = factory.get_chat()
        # that's it, you now have a chat wrapper object with the default template and model(set in .env file)



    """

    def __init__(
        self,
        template_selector=template_select,
        API_KEY=settings.OPENAI_API_KEY,
        model=settings.DEFAULT_MODEL,
        default_template_name=settings.DEFAULT_TEMPLATE_NAME,
        default_system_prompt = settings.DEFAULT_SYSTEM_PROMPT,
    ):
        if not isinstance(template_selector, TemplateSelector):
            raise exceptions.IncorrectObjectTypeError(
                f"template_selector must be a TemplateSelector object, not {type(template_selector)}"
            )

        self.template_selector = template_selector
        self.default_system_prompt = default_system_prompt
        self.model = model
        self.default_template_name = default_template_name
        self.selected_template = self.template_selector.get_template(
            self.default_template_name
        )
        self.API_KEY = API_KEY
        self.logger = BaseLogger(
            __file__,
            filename="ChatFactory.log",
            identifier="ChatFact",
            level=DEFAULT_LOGGING_LEVEL,
        )
        self.logger.info("ChatFactory object created")

    def _make_chat(self, template: dict) -> ChatWrapper:
        """Makes a chat wrapper object from a template"""
        chat = ChatWrapper(API_KEY=self.API_KEY, model=self.model, template=template)
        try:
            chat.auto_setup_from_template()
        except exceptions.PrettyGoodError as e:
            self.logger.error(
                f"Error while auto setting up chat wrapper from template: {template['name']}"
            )
            raise e
        self.logger.info(
            f"ChatWrapper object created from template: {template['name']}"
        )
        chat.system_prompt = self.default_system_prompt
        return chat

    def select_template(self, template_name: str) -> None:
        """Selects a template from the template selector"""
        self.selected_template = self.template_selector.get_template(template_name)
        self.model = self.selected_template["model"]
        self.logger.info(f"Template selected: {template_name}")

    def get_chat(self) -> ChatWrapper:
        """Returns a chat wrapper object from the selected template"""
        chat = self._make_chat(self.selected_template)
        self.logger.info(
            f"ChatWrapper object returned from template: {self.selected_template['name']}"
        )
        return chat

    def search_templates_by_tag(self, tag: str) -> list[str]:
        """Searches the templates for a tag"""
        self.logger.info(f"Searching templates for tag: {tag}")
        return self.template_selector.search_template_by_tag(tag)

    def get_template_info(self, name: str, format="dict") -> dict | str:
        """Gets the info for a template format can be either dict or str
        Will raise a TemplateNotFoundError if the template is not found, so either catch this error or use check_if_template_exists to check if the template exists before getting info for it(meant to prevent the dreaded NoneType does not have attribute error)
        """

        self.logger.info(f"Getting template info for template: {name}")
        return self.template_selector.get_template_info(
            name,
            format=format,
        )

    def check_if_template_exists(self, name: str) -> bool:
        """Checks if a template exists"""
        self.logger.info(f"Checking if template exists: {name}")
        return self.template_selector.check_template_exists(name)

    def __repr__(self):
        if self.API_KEY == settings.OPENAI_API_KEY:
            api_stat = "DEFAULT"
        elif self.API_KEY == None:
            api_stat = "NOT SET"
        else:
            api_stat = "CUSTOM"
        return f"ChatFactory(template_selector={self.template_selector}, API_KEY={api_stat}, model={self.model}, default_template_name={self.default_template_name})\n Selected Template: {self.selected_template['name']}"
