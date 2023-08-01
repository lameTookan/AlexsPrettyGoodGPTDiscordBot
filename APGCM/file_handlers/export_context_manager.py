import datetime
import os
from pathlib import Path

import exceptions
from chat import Message, export_data
from log_config import DEFAULT_LOGGING_LEVEL, BaseLogger
from settings import SETTINGS_BAG


class ExportContextManager:
    def __init__(
        self,
        folder: str = SETTINGS_BAG.EXPORTER_CONTEXT_MANAGER_DIR,
        base_name: str = SETTINGS_BAG.BASE_NAME,
        data: list[dict] = None,
        model: str = "GPT-4",
        system_prompt: str = None,
        **kwargs,
    ):
        self.logger = BaseLogger(
            module_name=__name__,
            filename="export_context_manager.log",
            identifier="export_context_manager",
            level=DEFAULT_LOGGING_LEVEL,
        )
        self.logger.debug("Initializing ExportContextManager")
        self.folder: str = folder
        self.base_name: str = base_name
        self._make_dir(self.folder)
        self.filename: str = None
        # our data to export
        self.data: list[dict] = self._check_data(data)
        self.model: str = model
        self.system_prompt: str = None or ""
        self.extra_data: dict = kwargs
        # the file object
        self.fp = None
        self.filepath: str = None

    def _make_dir(self, folder: str) -> None:
        """Creates a directory if it does not exist."""
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)

        self.logger.debug(f"Created directory {folder}")

    def _make_filename(self) -> str:
        """Creates a filename for the export."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        return f"{self.base_name}__{timestamp}.md"

    def _check_data(self, data: list[dict]) -> list[dict]:
        """Raises an error if the data is not a list of dictionaries."""
        if not isinstance(data, list):
            raise TypeError("data must be a list")
        if not isinstance(data[0], dict) and not isinstance(data[0], Message):
            raise TypeError("data must be a list of dictionaries or Message objects")
        return data

    def set_data(
        self,
        data: list[dict],
        system_prompt: str = None,
        model: str = "GPT-4",
        **kwargs,
    ) -> None:
        """Sets data to the export. Should be a list of dictionaries."""

        self.data = self._check_data(data)
        self.model = model
        self.system_prompt = system_prompt
        self.extra_data = kwargs

    def _get_markdown_data(self) -> str:
        """Gets the markdown data."""
        return export_data(
            self.data,
            system_prompt=self.system_prompt,
            model=self.model,
            **self.extra_data,
        )

    def make_file(self) -> str:
        """Makes the file."""
        if self.filename is None:
            self.filename = self._make_filename()
        if self.data is None:
            raise ValueError("No data to export.")
        self.filepath = os.path.join(self.folder, self.filename)
        with open(self.filepath, "w") as f:
            f.write(self._get_markdown_data())
        self.logger.info("Wrote data to file: {self.filepath}")
        return self.filepath

    def _delete_file(self) -> None:
        """Deletes the file."""
        if self.filepath is None:
            raise ValueError("No file to delete.")
        os.remove(self.filepath)
        self.logger.info(f"Deleted file: {self.filepath}")

    def __enter__(self):
        """Creates the file, and then returns the file object. Must have entered the data before calling this."""
        if self.filepath is None:
            filepath = self.make_file()
        self.fp = open(self.filepath, "r")
        return self.fp

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Closes the file, and deletes it."""

        self.fp.close()
        self._delete_file()
        self.logger.info("Closed file, and deleted it.")
        # reset state
        self.data = []
        self.model = "GPT-4"
        self.system_prompt = ""
        self.extra_data = {}
        self.filename = None
        self.filepath = None
        self.fp = None
        



if __name__ == "__main__":
    test_data = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am doing well, how are you?"},
        {"role": "user", "content": "I am doing well, thanks for asking."},
    ]
    test_extra_data = {
        "name": "test",
        "age": 20,
        "yo": "hello",
    }
    test_system_prompt = "System: Hello, This is a test."
    ecm = ExportContextManager(
        data=test_data, system_prompt=test_system_prompt, **test_extra_data
    )
    with ecm as f:
        print(f.read())
    print(ecm.data)
