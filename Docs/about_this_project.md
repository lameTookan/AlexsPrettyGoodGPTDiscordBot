# About this Project / FAQ



Of course, no one has asked me any questions about this project, but I am going to answer some questions I think people might have anyway.

Also if anyone has even a slight interest in this project hit me up! I am assuming no one is really paying attention, but if someone is, I will focus more on this project and updating it!
You can hit me up on here, email me at lametoucan@gmail.com, or even message me on discord @lametookan!

## Ideas for updates

### Short Term

#### Discord Bot / Cleaning up Commands

* Clean up the command structure

* Integrate modals, auto-complete and other fancy discord features I have been playing around with
* Add the option for custom modes
* Incorporate the same context switching system I used with help mode into the other modes
* Consolidate the modes into a single command with auto-complete
* More options for the export command(text, pdfs, html etc)

### Bigger Features

* Sticky messages(won't be trimmed from the history) with an associated command to remove and manage them
* Modify previous message(s) with a command
* More on the fly customization options
  * Model
  * Other model params: frequency_penalty, top_p, presence_penalty, etc
  * Max model tokens and max completion tokens
* Add a database system to store the trimmed chat history and other data
* Add messages via uploading text files
* Default Mode Changing for new chats

### Long Term

* Embeddings for long term memory
* More advanced context switching system
* Web Interface for managing the bot
* Optimizations for larger servers
* More advanced chat history management
* Support for new function calls
  * Possible agent system for things like web searching , etc.
  * Integration into various public APIs for things like weather, jokes, fun facts, etc.
* More advanced template system
* Shifting context window
  * ie if you set the max tokens lower, and then increase it, the bot will use the previous messages to fill in the context window
* User Profiles
* More advanced accumulator system
  * ie. the ability to set the max number of messages to accumulate before sending them to the model
* Options to help manage and estimate costs for the API calls

## FAQ

### Do you really expect anyone to use Alex's Pretty Good Chat Module?

No, probably not. However, as a learning exercise I made it with the intention of it being used by other developers and tried to make it as flexible and easy to use as possible.

#### Did you succeed in making it flexible and easy to use?

Eh, I am like 50/50 on that. There is a lot of spaghetti code in there, and I am sure there are a lot of bugs. Theres a lot of little things I would have done differently if I had more experience.

### Will you continue to work on this project?

Possibly in the future. But for now, I think I will shift my focus back to learning more about programming and computer science in general. I have only been coding for a few months, and I have a looot to learn. I will likely come back to this project next month however.

### How long did it take you to make this project?

So I started this project in early july working on it on and off, however, in the last few days of I started a sprint trying to wrap it up and turn it into something folks can actually use, spending basically all my free time on it (6-8+  hours a day depending on how little sleep I was willing to make due with and other life stuff ).

### What did you learn from this project?

Oh boy a lot.

* Mainly how to manage a larger project like this, better adherence to paradigms like DRY, and how to use git and github better.
* Importance of logging(A good habit I managed to pick up through this project)
* When to stop iterating and optimizing and just get something working
* TDD and how much it helps
* Discord.py and the Discord API, getting more comfortable with async programming
* That I need to swear off monster classes some of them are just way too large and unwieldy
* Importance of planning before hand, roadmaps, etc.
* How much time it actually takes to make something like this
* How much I still have to learn
* How much I genuinely enjoy programming, and how thankful I am that I have had the time to get into it  in these last few months

### What was your favorite things you built for this project?

My file handlers are great and something I am def going to reuse in future projects. And weirdly enough, the quick_test script I made to test the bot before running it. I feel like its super user friendly. Also using pyfiglet to make the ascii art for the startup message is always a fun way to wrap up a project.

### Whats up with the ax file in MyStuff?

* I made my stuff the first week or two of my coding journey, but ax is a bit of an easter egg I wasted way too long on one evening. See if you can figure out what it does.
