import csv
import datetime
import json
import logging
from abc import ABC, abstractmethod

import exceptions
from chat.message import Message, MessageFactory
from log_config import (DEFAULT_LOGGING_LEVEL, LOGGING_FILE_PATH,
                        LOGGING_FORMAT, BaseLogger)
"""These classes are used to export data from the chat log to a file as a text file or markdown file."""

class Exporter(ABC):
    """Abstract base class for all exporters.
    Requires the following methods:
        _format_message
        make_header()
        make_body()
        make_footer()
    Comes with the following methods:
        export()
        __init__()
    """
    exporter_type = "exporter"
    def __init__(self, data: list[Message], model: str, system_prompt: str = None, **kwargs):
        self.data = data
        self.model = model
        self.system_prompt = system_prompt
        self.logger = BaseLogger(__file__, filename=f"{self.exporter_type}.log", identifier= self.exporter_type, file_path=LOGGING_FILE_PATH)
        self.logger.set_logging_level(DEFAULT_LOGGING_LEVEL)
        self.logger.debug("Initializing Exporter")
        self.extra_meta = kwargs
        if type(self.data[0]) is not Message:
            self.data = [Message(model=model, **msg) for msg in self.data]
    @abstractmethod
    def _format_message(self, msg: Message) -> str:
        pass
    @abstractmethod
    def make_body(self):
        pass
    @abstractmethod
    def make_header(self) -> list[str]:
        pass
    @abstractmethod
    def make_body(self) -> list[str]:
        pass
    @abstractmethod
    def make_footer(self) -> list[str]:
        pass
    
    def export(self):
        """Uses the make_header, make_body, and make_footer methods to create a list of strings, then joins them together with newlines."""
        results = [
            "\n".join(self.make_header()),
            "\n".join(self.make_body()),
            "\n".join(self.make_footer())
        ]
        return "\n".join(results)
        
    

class TextExporter(Exporter):
    """Text exporter. Exports the chat log as a text file.
    
    """
    exporter_type = "text"
    def __init__(self, data: list[Message], model: str, system_prompt: str = None, **kwargs ):
        
        super().__init__(data, model, system_prompt, **kwargs)
        self.logger.info("Initializing TextExporter")
    def _format_extra_meta(self) -> list[str]:
        """Formats the extra meta data for export."""
        formatted = []
        for key, value in self.extra_meta.items():
            key = key.replace("_", " ").title()
            formatted.append(f"{key}: {value}")
        return formatted
    def _format_message(self, msg: Message) -> str:
        """Formats a message for export."""
        
        if msg.role == "system":
            return f"System: {msg.content}"
        elif msg.role == "user":
            return "User: " + msg.content
        elif msg.role == "assistant":
            return "Assistant: " + msg.content
        else:
            return f"{msg.role}: {msg.content}"
    
    def make_header(self) -> list[str]:
        self.logger.info("Making header")
        divider = "-+-" * 10
        result = [
            "Chat Log",
            divider, 
            "Meta Data:",
            "Model: " + self.model,
            "Total Messages: " + str(len(self.data)),
            "Time: " + str(datetime.datetime.now()),
            "Date: " + str(datetime.date.today()),
            "System Prompt: " + str(self.system_prompt) if self.system_prompt is not None else "System Prompt: None",
            "Extra Meta Data:",]
        result.extend(self._format_extra_meta())
        result.extend([divider, "Messages:", ""])
        return result
    def make_body(self) -> list[str]:
        self.logger.info("Making body")
        short_divider = "-" * 5
        result = []
        for msg in self.data:
            result.append(self._format_message(msg))
            result.append(short_divider)
        return result
    def make_footer(self) -> list[str]:
        return []
    
class MarkdownExporter(Exporter):
    """Markdown exporter. Exports the chat log as a markdown file.
    Adds a static method, italics, which adds italics to a string.
    
    """
    def __init__(self, data: list[Message], model: str, system_prompt: str = None, **kwargs):
        super().__init__(data, model, system_prompt , **kwargs)
        self.logger.debug("Initializing MarkdownExporter")
    @staticmethod
    def italics(string: str) -> str:
        return f"*{string.strip()}*"
    def _format_message(self, msg: Message) -> str:
       
        """Formats a message for export."""
        
        if msg.role == "system":
            return f"**System:** {MarkdownExporter.italics(msg.content)}"
        elif msg.role == "user":
            return "**User:** " + MarkdownExporter.italics(msg.content)
        elif msg.role == "assistant":
            return "**Assistant:** " + MarkdownExporter.italics(msg.content)
        else:
            return f"_{msg.role}_: *{msg.content}*"
    def _format_extra_meta(self) -> list[str]:
        """Formats any extra meta data for export (Passed to __init__ as **kwargs)"""
        formatted_meta = []
        for key, value in self.extra_meta.items():
            formatted_meta.append('')
            
            key = key.replace("_", " ").title()
            formatted_meta.append (f"**{key}:** *{value}*")
        return formatted_meta
    def make_header(self) -> list[str]:
        divider = "---"
        result =  [
            "# Chat Log",
            "",
            "## Meta Data",
            "",
            ]
        if self.model is not None:
            result.append("**Model**: " + MarkdownExporter.italics(str(self.model)))
        
        more = [
            "",
            "**Total Messages**: " + MarkdownExporter.italics(str(len(self.data))),
            "",
            "**Time**: " + MarkdownExporter.italics(str(datetime.datetime.now())),
            "",
            "**Date**: " + MarkdownExporter.italics(str(datetime.date.today())),
            "",
           ]
        result.extend(more)
        if self.system_prompt is not None:
            result.append( "**System Prompt**: " + MarkdownExporter.italics(str(self.system_prompt)) )
        result.extend(self._format_extra_meta())
        result.extend(["",
            divider,
            "",])
        return result
    def make_body(self) -> list[str]:
        result = [
            "## Messages",
            "",
        ]
        divider = "---"
        count = 0
        for msg in self.data:
            count += 1
            result.append(self._format_message(msg).strip())
            result.append("")
            result.append(divider)
            
            if count != len(self.data):
                result.append("")
                
            
        return result
    def make_footer(self) -> list[str]:
        return []
    
def export_data(data: list, model: str = None, system_prompt: str = None, exporter_type: str = "markdown", **kwargs) -> str:
    """Exports the chat log as a text file.
    Args:
        data (list): A list of Message objects.
        model (str): The model used to generate the chat log.
        system_prompt (str, optional): The system prompt used to generate the chat log. Defaults to None.
        exporter_type (str, optional): The type of exporter to use. Defaults to "text".
    Supported exporter types:
        text
        markdown 
        
    Raises:
        exceptions.InvalidExporterError: Raised if the exporter_type is not a valid exporter.
    Returns:
        str: The exported chat log.
    Example Usage:
        chat_log = ChatLog()
        chat_log.load_from_save_dict(save_dict)
        extra_meta = {
            "user_name": "Bob",
            "description": "A chat log with Bob",
            "tags": ["Bob", "chat log", "gpt-4"]
        }
        with open("chat_log.md", "w") as f:
            f.write(export_data(chat_log.data, chat_log.model, chat_log.system_prompt, exporter_type="markdown",  **extra_meta))
    """
    if exporter_type == "text":
        exporter = TextExporter(data, model, system_prompt, **kwargs)
        return exporter.export()
    elif exporter_type == "markdown":
        exporter = MarkdownExporter(data, model, system_prompt, **kwargs)
        return exporter.export()
    else:
        raise exceptions.BadFormatError(f"Invalid exporter type: {exporter_type}")
    
    
