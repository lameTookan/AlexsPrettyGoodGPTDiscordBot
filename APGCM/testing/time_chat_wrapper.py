from func import get_test_chat_log
import time 
import json 
import os 
from templates.cw_factory import ChatFactory

def main():
    divider = "-----------------------------------------------"*2
    divider_len = len(divider)
    print(divider )
    print(f"\u001b[35m<<<===============(CHAT WRAPPER TIMING SCRIPT)===============<<<\u001b[0m".center(divider_len, " "))
    print(divider )
    print("\n")
    print("Welcome to the chat wrapper timing script.")
    print("We will load an extremely long example chat log and see how long it takes to process it.")
    print("\n\n")
    input("Press enter to continue......(Or ctrl+c to exit)")


    with open("./testing/test_chat_logs/short_10000.json") as f:
        chat = json.load(f)
    print("Chat Length (messages):", len(chat))
    fact = ChatFactory()
    cw = fact.get_chat()



    print("Starting test")
    start = time.perf_counter()
    print("Start:", start)
    cw.trim_object.add_messages_from_dict(chat)

    done = time.perf_counter()
    print("Done:", done)
    elapsed_time = done - start
    print("Elapsed time:", elapsed_time)




    msg = "\n".join(
            [
                "Test Results:",
                f"Loaded a chat of length {str(len(chat))} ",
                f"Elapsed time while processing {str(elapsed_time)}",
                f"Average time per message: {str(elapsed_time / len(chat))}",
                "-+-+-+" * 10 ,
                f"Debug info:",
                "-+-+-+" * 10,
                "\n\n\n",
                cw.debug(),
            ]
        )
    print(msg)

    ans = input("Save Test Results? (y/n)")
    if ans == "y":
        files_numb = len(os.listdir("./testing/test_results/"))
        with open(f"./testing/test_results/time_add_msg__{str(files_numb)}.txt", "w") as f:
            f.write(msg)
        print("Saved test results to ./testing/test_results_<numb>.txt")
        print("The numb is the number of files in the test_results folder(Before saving this file)")
        print("This is to ensure that the file name is unique")
    else:
        print("Not saving test results")

    ans = input("Print chat? (y/n)")
    if ans == "y":
        print(cw)
    else: 
        print("Not printing chat")
    print("Done")


if __name__ == "__main__":
    main()