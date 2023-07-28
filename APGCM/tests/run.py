import chat 
import exceptions
import func 
import tiktoken
import json
import chat_completion_wrapper
from settings import OPENAI_API_KEY

# print("Some other basic tests: ")
# chat_log = chat.ChatLog('gpt-4')
# factory = chat_log.get_message_factory()
# user_message = factory(role = 'user', content = 'Hello, world!')
# assistant_message = factory(role = 'assistant', content = 'Hi, there!')
# chat_log.add_message(user_message)
# chat_log.add_message(assistant_message)
# print(chat_log)
# print(repr(chat_log))

# trim = chat.TrimChatLog()
# trim.system_prompt = "||date|| ||model|| ||cut_off||"
# test_chat = func.get_test_chat_log()
# trim.add_messages_from_dict(test_chat)
# with open("testing/finished_test_chat.json", "w") as f:
#     json.dump(trim.get_finished_chatlog(), f, indent=4)
# print(trim.make_save_dict())
# print(repr(trim))
# #print(trim)
# with open('testing/test_save.json', "w") as f:
#     json.dump(trim.make_save_dict(), f, indent=4)

# param = chat_completion_wrapper.ModelParameters()
# param.temperature = 0.9
# print(param.temperature)
# print(param.get_all_params_dict())
# print(param.get_param_kwargs())
# print(repr(param))

test_chat = func.get_test_chat_log("short_7K_tokens.json")

wrap = chat_completion_wrapper.ChatCompletionWrapper(model= "gpt-3.5-turbo-16k", API_KEY=OPENAI_API_KEY)
print(wrap.chat(test_chat))

