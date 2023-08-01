# So how the heck does GPT work?

This is not going to be a detailed explanation of the technology behind the model, but will be an overview of how the API works. I also would like to debunk some common misconceptions.

## What's an API?

API stands for Application Programming Interface. It's a way for programs to communicate with each other, either on the same computer or over the internet. The OpenAI API is a web API, which means it's accessed over the internet.


Think of it like a website for computers, that allows for programs to communicate with it in a structured way and receive data back in a structured manner thats easy for programs to work with.

## What is a token?

GPT does not work with words or letters directly. Instead, the words are converted to tokens, or a number representing a string of characters or a punctuation mark.

It's a little bit complex. Some tokens represent a single character, some represent a word, and some represent a punctuation mark, but in general, you can roughly think of a token as a word.

For example, the previous paragraph was 42 tokens long. This is what the token representation looks like

```python
[20459, 257, 1310, 1643, 3716, 11, 617, 16326, 2380, 257, 2060, 2095, 11, 617, 2380, 257, 1573, 11, 290, 617, 2380, 257, 21025, 2288, 1317, 11, 475, 287, 2276, 345, 460, 7323, 892, 286, 257, 11241, 355, 257, 1573, 13, 220, 198]
```

This is how GPT sees the text. This is also why it struggles with games like hangman, because it doesn't know what a letter is, it only knows what a token is. From GPT's perspective, it gets a list of numbers and does some complex math to figure out what the next number should be.

To learn more about this or play around with an official tokenizer check out [this page](https://platform.openai.com/tokenizer).

## How does the API work?

Each request to the API needs to have two things:

1. The model
2. Chat history
There are also other optional parameters, which we will get into later.

### The Model

This is the  model (or AI system). There are many different models, and each one has different capabilities. The model is specified by a string, like "davinci" or "curie". The three big ones this project supports by default are "gpt-4", "gpt-3.5-16k", and "gpt-3.5-turbo".
GPT-4 is the most recent and the most advanced but it is also the most expensive.

### The Chat History

So here is the big kicker, and one of the biggest misconceptions I see floating around about how GPT works:

__GPT does not have any memory.__

That's right, the model has no system for 'remembering' things! Every request is completely independent of the last one. From GPT's perspective each request might as well be the first one it has ever received.

#### Wait, so how does it remember things?

This is where the chat history comes into play. In order for it to 'remember' your previous messages, you have to send them to it every time you make a request. This module's main purpose to make the process as easy as possible, trimming off old messages that go over the _maximum model tokens_

This is why gpt seems to forget things as a chat goes on. It's not that it's forgetting, it's that it's not being told about the previous messages.

The only context the model has must be included in each request in the form of chat history, or a list of previous messages. This is why the chat history is so important, it is the only way for the model to 'remember' things.

#### So, why do we need to trim the chat history?

Each model has a maximum amount of tokens it can process at once. If we try to send it too many tokens at once, it will throw an error. This is why we need to trim the chat history, to make sure we don't go over the limit.

Now, there is also another important parameter here: `max_tokens`, which refers to the maximum amount of tokens the model is allowed to produce in each request. This is worth mentioning because these tokens are also counted against the limit. So if you have a `max_tokens` of 1000 and a `max_model_tokens` of 4000, you can only send 3000 tokens of chat history to the model.

It does not matter how long the completion actually would have been, just how long it _could_ be. If the max model tokens is 4000, and the max tokens is 1000,  and we attempt to send a request with 3001 tokens it will fail. Even if the completion only would have been 100 tokens.

#### So, what happens if we go over the limit?

A big fat red error message. Nothing else.

## What about those other parameters?

To see a full list of parameters, check out the [OpenAI API docs](https://beta.openai.com/docs/api-reference/completions/create).

I will go over the parameters this project supports changing here, however.

### Temperature

This is a `float` (or a number with a decimal point) between 0.0 and 2.0. It controls how 'creative' the model is. The higher the temperature, the more creative the model is. The lower the temperature, the more it sticks to the training data.

I've found  that anything above 1.0 can produce some nonsensical results, but it can be fun to play around with.
Lower values produce more deterministic results, that are "boring" but more accurate to the training data.

Lower temperature = more accurate, less creative
Higher temperature = less accurate, more creative

In my testing I have found that a temperature of 0.7 produces the best results, but you can play around with it and see what you like. Values between .3 and .9 are the sweet spot in my opinion.

For example, I asked GPT-4 to generate a story with a temperature of 2.0 and this is what it came up with:

```text
Once upon a morning as beautiful and green as leaf on spring water, Michael Sharaska flipped the `SMITH POWER LTD'' token scried MoonBlack incscacs18432-64_xak135vlakien48sfastsea500.txt secretly propagated under dir //popusers.xset/access.token/port.snap [211 vispert_alpha257371715402_pop_xx/pop++] michaelarchsha_icon/code_system65431cryptlid_pathblastory-t that dicatorated his total cyber persona at system detected silicon operative.

Michael's freshly boaseau laid code unlocked cutting-edge quantum prototypes surrenost tightly al-nortsp stravesdwaste greyorg tap icessnipra users before disgavrilesced skytrammer slektepace routes logisty ticie printcards spent tapespike hours populated between nought needle reality felt crystallied some thrwell stiffors frethic bubombath dark byte duntry bad blue popblack plast icy history mission byte bits thrawing bull blob burns metallic clattering itself script digitalized savrene matrix skywhite several silverlong thousands spat tube glitter strangely clarga speciallo torch cry catcatcholles shadows here breakglass boundary thrust tep grand millions moment seems spectral spread shining tale ten unto started brevg grey.
```

### Top P

This is a `float` between 0.0 and 1.0. It is an alternative to temperature, and controls how 'creative' the model is. It's a bit like temperature however, its more of a hard limit. This is a bit more complex, so I asked for help from GPT-4 to explain it:
Note: It is recommended to use either temperature or top p, not both at the same time.

```text
The top_p parameter, sometimes referred to as "nucleus sampling", is a method used in language models to control the randomness of predictions by narrowing down the possible outcomes to a subset of the most likely tokens. It's a more sophisticated approach compared to the traditional method of just choosing the most probable next token or sampling from the entire distribution.

In specific, for a given value of top_p in (0, 1), the model sorts all the potential next tokens by their probability, then adds these probabilities starting from the most likely one until the cumulative probability exceeds the given top_p value. The model's next token is then randomly sampled from this "nucleus" of top tokens.

In contrast, the "temperature" parameter, another commonly used method for controlling randomness, works a bit differently. It modifies the distribution of the next-word predictions by scaling the logits before applying softmax.

When the temperature is set to 1, it means that the model will take the original output distribution from the logits. When the temperature is less than 1, the model tends to produce more confident and deterministic outputs, essentially amplifying the probabilities of the most likely tokens. On the other hand, when the temperature is greater than 1, the model's output becomes more diverse, effectively giving less likely tokens a better chance of being selected.
```

__Um, what?__
Think of top_p like a hard limit counterpart to the temperature. Temperature is like saying "Hey, try to use more tokens that are less likely to be used". Top p is like saying "You can ONLY use tokens that are unlikely to be used". I recommend doing your own research on this, as it is a bit complex.

### Presence Penalty

This is a value between -2 and 2. It controls how often  the model will repeat itself. Essentially, it reduces the likelihood of the model using tokens that are already in the chat history. Every time a token appears in a chat history, the model will be less likely to use it again.

### Frequency Penalty

This is a lot like presence penalty, but it penalizes tokens based on how often they appears in the models training data, instead of how often they appear in the chat history.

### Max Tokens

 We already described this, but for the sake of completeness, this is the maximum amount of tokens the model can produce in a single request. 

 I.E. How long the AI response can be, in tokens. 


## API Keys

 The OpenAI API requires an API key to use. You can get one by signing up  at <https://platform.openai.com>. Once you have an API key, you can set it in the the .env file, or you can set it as an environment variable called `OPENAI_API_KEY`.

 Be careful with your API key, as it is a secret and should not be shared with anyone. If you think your API key has been compromised, you can reset it at <https://platform.openai.com>.

 I recommend testing new projects(like this one!) with a "low trust" API key. Rotate this key out often and pay close attention to your usage. If you decide you like a project, and think that you will be using it often, switch to a dedicated key.

 Now, in this project, the only place that communicates with the internet is in the `ChatCompletionWrapper` class, using the official openai python library. However, its never a good idea to put your key into any code you don't understand. I can assure you that this project does not do anything malicious with your key, but if you are worried about it, you can use a tool like [Wireshark](https://www.wireshark.org/) to monitor the network traffic of the program and verify that it is not sending your key anywhere.

 Do not ever share your API key publicly. You are responsible for paying for any usage of your key, and if someone else uses it, you will be billed for it.

 If you leak your key, someone could potentially use it to rack up a huge bill. If you think your key has been compromised,  you can delete the key in question on [the API section on the OpenAI website](https://platform.openai.com/account/api-keys), and create a new one.

## Why is this in your docs?

 I want this project to be usable for anyone, regardless of their technical ability.
 It helps to have a basic understanding of how the API works to use this project.

I hope I explained this all in a simple enough way that anyone can understand it.
If you have any questions, feel free to open up a new thread on the discussions tab for this project.
