import json
import logging
from pathlib import Path

import chat
import exceptions
import file_handlers
import func

print(dir(chat))
print(dir())
# gen = file_handlers.GeneralFileHandler(save_folder = "../files/", file_extension=".txt")
# gen.write_to_file("test.txt", "Hello World!")

#cause an error to be raised
test_chat_log =json.loads( Path("./testing/test_chat_logs/super_short.json").read_text())

# trim = chat.TrimChatLog()
# trim.system_prompt = "This is a test prompt ||model||, ||date||, ||time||, ||cut_off||"

# trim.add_messages_from_dict(test_chat_log)
# json_file_handler = file_handlers.JsonFileHandler(save_folder = "./testing/test_json_outputs" )
# json_file_handler.set_logging_level(logging.INFO)
# json_file_handler.write_to_file("test_trim2.json", trim.make_save_dict(), overwrite=True)

chat_log = chat.ChatLog("gpt-4")

chat_log.add_messages_as_dict(test_chat_log)

exporter_text = chat.TextExporter(chat_log.data, chat_log.model, system_prompt="This is a test prompt ||model||, ||date||, ||time||, ||cut_off||")
exporter_md = chat.MarkdownExporter(chat_log.data, chat_log.model, system_prompt="This is a test prompt ||model||, ||date||, ||time||, ||cut_off||")

with open("./testing/test_text_outputs/test_text_exporter.txt", "w") as f:
    f.write(exporter_text.export())
with open("./testing/test_text_outputs/test_md_exporter.md", "w") as f:
    f.write(exporter_md.export())