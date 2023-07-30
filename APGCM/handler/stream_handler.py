import sys 
import os
from abc import ABC, abstractmethod
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
import asyncio 

class AbstractStreamOutputHandler(ABC):
    name = "Abstract_Stream_Output_Handler"
    """
    This abstract class is meant to enforce what the ChatCompletionWrapper expects from a StreamOutputHandler.
    For use with the OpenAI API when the stream parameter is set to True, which outputs the tokens as they come in.
    
    The write method is called for each token that comes in, and the done method is called when the API is done streaming.
    Dependencies:
        log_config.BaseLogger, log_config.DEFAULT_LOGGING_LEVEL,
        ABC, abstractmethod from abc
    Attributes:
        name: str = "Abstract_Stream_Output_Handler" The name of the class. Used for logging purposes, and debugging.
        logger: BaseLogger pre-configured base logger for the class.
        content: str = "" The full content of the stream, as it comes in. Completely optional, but can be useful for debugging purposes.
        
    Methods:
    
        write(content: str, full_event: dict) -> None Takes the content(usually an individual token) and outputs them somewhere, as they come in from the API. Full event is the entire event object from the API.
        done(stop_reason, full_response: str) -> None Called when the API is done streaming. Stop reason is the reason the API stopped streaming, str is the final response.
    Example usage:
        How ChatCompletionWrapper uses it:
            def chat(self, messages: list[dict]) -> str:
                chat_completion = openai.Completion.create(..args and kwargs.., stream=True)
                respond_str = ""
                if self.stream_handler is not None and self.stream is True:
                    
                    for event in chat_completion:
                        if event.choices[0].finish_reason is not None:
                            text = chat_completion.choices[0].delta.content
                            response_str += text
                            self.stream_handler.write(text, event)
                        else:
                            self.stream_handler.done(event.choices[0].finish_reason)
                            break
                    return respond_str
                else:
                    return chat_completion.choices[0].message.content
    Dirt Simple Example of a StreamOutputHandler:
        class PrintStreamOutputHandler(AbstractStreamOutputHandler):
            name = "Print_Stream_Output_Handler"
            def __init__(self):
                super().__init__("print_stream_handler.log")
            def write(self, content: str, full_event: dict) -> None:
                print(content)
            def done(self, stop_reason, full_response: str) -> None:
                print("Done!")
        Output(For the message Hello World!)): 
            Hello
            World!
            Done!
            
        See StdoutStreamHandler for a more practical  example.
       
    """
    def __init__(self, log_filename: str = "StreamHandler.log") -> None:
        self.logger = BaseLogger(__file__, identifier=f"{self.name}_StreamHandler",   filename=log_filename, level=DEFAULT_LOGGING_LEVEL)
        self.logger.info(f"Initializing {self.name} Stream Handler")
        self.full_content: str = ""
    @abstractmethod
    def write(self, content: str, full_event: dict) -> None:
        """Takes the content(usually an individual token) and outputs them somewhere, as they come in from the API. Full event is the entire event object from the API."""
        self.full_content += content
    @abstractmethod
    def done(self, stop_reason) -> None:
        """Called when the API is done streaming. Stop reason is the reason the API stopped streaming."""
        pass

    def __repr__(self) -> str:
        return f"{self.name} Stream Handler"
    def __str__(self):
        return self.full_content
class StdoutStreamHandler(AbstractStreamOutputHandler):
    """A simple StreamOutputHandler that writes to stdout, and logs the content.
    About as simple as these things can get. However, will be useful for CLI applications, and serves as a good example of how to implement a StreamOutputHandler. 
    Dependencies:
        AbstractStreamOutputHandler from this module
        sys (for stdout) the biggest dependency
        BaseLogger, DEFAULT_LOGGING_LEVEL from log_config
    Raises:
        None
    Attributes:
        name: str = "Stdout_Stream_Handler" The name of the class. Used for logging purposes, and debugging.
        self.logger: BaseLogger pre-configured base logger for the class.
        self.full_content: str = "" The full content of the stream, as it comes in. Completely optional, but can be useful for debugging purposes.
        self.record_of_events: list = [] A record of all the events that came in, as they came in. Useful for debugging purposes.
    Methods:
        write(content: str, full_event: dict) -> None Takes the content(usually an individual token) and prints them to stdout, on the same line, and then flushes stdout. Also logs the content.
        done(stop_reason, full_response: str) -> None resets the full_content and record_of_events attributes so they don't clog up memory. Also logs the stop reason and the full response.
    Example usage:
        Example 1(Directly with CCW):
            ...already have made a chat_completion_wrapper object called chat_completion_wrapper...
            handler = StdoutStreamHandler()
            chat_completion_wrapper.add_stream_handler(handler)
        Example 2(With ChatWrapper):
            ...made chat wrapper object called chat_wrapper...
            stream_handler = StdoutStreamHandler()
            chat_wrapper.add_stream_handler(stream_handler)
            chat_wrapper.chat("Hello, I am a chat wrapper object. I am using a stream handler to print to stdout as I chat.")
            # as the tokens come in, they will be printed to stdout, and then flushed.

        
        """
    name = "Stdout_Stream_Handler"
    def __init__(self, color: str = "\033[0;32m", prefix: str =">> "):
        super().__init__("stdout_stream_handler.log")
        self.logger.info(f"Initializing {self.name} Stream Handler")
        self.record_of_events = []
        self.is_first = True
        self.color = color
        self.prefix = prefix
        self.reset_color = "\033[0m"
    def write(self, content: str, full_event: dict) -> None:
        """Writes the content to stdout, and then flushes it. Also logs the content."""
        if self.is_first:
            self.is_first = False
            sys.stdout.write(self.color + self.prefix)
        sys.stdout.write(content)
        sys.stdout.flush()
        self.full_content += content
        self.logger.info(f"Writing {content} to stdout")
        self.record_of_events.append(full_event)
    def _reset(self):
        self.full_content = ""
        self.record_of_events = []
        self.is_first = True
    def done(self, stop_reason, response_str: str = None ) -> None:
        """Writes a new line to stdout, and then flushes it. Also logs the stop reason and the full response, and resets the full_content and record_of_events attributes so they don't clog up memory. """
        self.logger.info(f"Done streaming. Stop reason: {stop_reason}")
        sys.stdout.write(self.reset_color)
        sys.stdout.write("\n")
        sys.stdout.flush()
        
        # reset everything so it doesn't clog up memory, no need to record it here, as ChatCompletionWrapper will have a record of it.
        self._reset()
    

        
class DisMessageSplitStreamHandler(AbstractStreamOutputHandler):
    name = "DisMessageSplit_Stream_Handler"
    def __init__(self, chunk_size: int = 1000, ):
        self.logger = BaseLogger(__name__, identifier=f"{self.name}_StreamHandler",   filename="discord_stream_handler.log", level=DEFAULT_LOGGING_LEVEL)
        self.chunk_size = chunk_size
        self.logger.info(f"Initializing {self.name} Stream Handler")
        self.accumulator = ""
        self.queue = asyncio.Queue()
    def write(self, content: str, full_event: dict) -> None:
        """Writes the content to stdout, and then flushes it. Also logs the content."""
        self.logger.info(f"Writing {content} to stdout")
        self.accumulator += content
        if len(self.accumulator) >= self.chunk_size:
            self.queue.put_nowait(self.accumulator)
            self.accumulator = ""
    def done(self, stop_reason):
        self.queue.put_nowait(self.accumulator)
        self.accumulator = ""
        self.queue.put_nowait(None)
        self.logger.info(f"Done streaming. Stop reason: {stop_reason}")
    async def get_messages(self):
        while True:
            message = await self.queue.get()
            if message is None:
                break
            yield message
            self.queue.task_done()
discord_handler = DisMessageSplitStreamHandler()