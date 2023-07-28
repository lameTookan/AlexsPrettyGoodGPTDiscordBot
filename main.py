import sys

sys.path.append("./APGCM")
from APGCM import (
    DEFAULT_LOGGING_LEVEL,
    BaseLogger,
    ChatFactory,
    ChatWrapper,
    JsonSaveHandler,
    exceptions,
    
)
from APGCM.settings import DEFAULT_TEMPLATE_NAME, OPENAI_API_KEY

fact = ChatFactory()

cw = fact.get_chat()

while True:
    ans = input("> ")
    print(cw.chat(ans))
