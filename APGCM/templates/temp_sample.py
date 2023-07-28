
template_sample = {
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
    "gpt-4_creative": {
        "model": "gpt-4",
        "info": {
            "description": "Creative Mode for the gpt-4 model",
            "tags": ["gpt-4", "creative", "chat", "high temperature"],
        },
        "name": "gpt-4_creative",
        "id": 2,
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
            "temperature": 1.0,
        },
    },
    "gpt-4_small": {
        "model": "gpt-4",
        "name": "gpt-4_small",
        "id": 3,
        "info": {
            "description": "A small configuration for the gpt-4 model, meant to save on API costs(billed per token)",
            "tags": ["gpt-4", "small", "chat", "low cost"],
        },
        "trim_object": {
            "model": "gpt-4",
            "max_tokens": 4000,
            "token_padding": 100,
            "max_completion_tokens": 500,
            "max_messages": 100,
        },
        "chat_completion_wrapper": {
            "model": "gpt-4",
            "max_tokens": 500,
            "temperature": 0.7,
        },
    },
    "gpt-4_precise": {
        "model": "gpt-4",
        "name": "gpt-4_precise",
        "id": 4,
        "info": {
            "description": "A precise configuration for the gpt-4 model, meant to be used for precise responses. Low temp",
            "tags": ["gpt-4", "precise", "chat", "low temp", "conservative"],
        },
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
            "temperature": 0.1,
        },
    },
    "gpt-3.5-16k_default": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_default",
        "id": 5,
        "info": {
            "description": "The default configuration for the gpt-3.5-16k model",
            "tags": ["gpt-3.5-16k", "default", "chat"],
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500,
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 0.7,
        },
    },
    "gpt-3.5-16k_creative": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_creative",
        "id": 6,
        "info": {
            "description": "Creative Mode for the gpt-3.5-16k model",
            "tags": ["gpt-3.5-16k", "creative", "chat", "high temperature"],
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500,
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 1.0,
        },
    },
    "gpt-3.5-16k_precise": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_precise",
        "id": 7,
        "info": {
            "description": "A precise configuration for the gpt-3.5-16k model, meant to be used for precise responses. Low temp",
            "tags": ["gpt-3.5-16k", "precise", "chat", "low temp", "conservative"],
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500,
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 0.1,
        },
    },
    "gpt-3.5-16k_default": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_default",
        "id": 5,
        "info": {
            "description": "The default configuration for the gpt-3.5-16k model",
            "tags": [
                "gpt-3.5-16k",
                "default",
                "chat"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 0.7
        }
    },
    "gpt-3.5-16k_creative": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_creative",
        "id": 6,
        "info": {
            "description": "Creative Mode for the gpt-3.5-16k model",
            "tags": [
                "gpt-3.5-16k",
                "creative",
                "chat",
                "high temperature"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 1.0
        }
    },
    "gpt-3.5-16k_precise": {
        "model": "gpt-3.5-16k",
        "name": "gpt-3.5-16k_precise",
        "id": 7,
        "info": {
            "description": "A precise configuration for the gpt-3.5-16k model, meant to be used for precise responses. Low temp",
            "tags": [
                "gpt-3.5-16k",
                "precise",
                "chat",
                "low temp",
                "conservative"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-16k",
            "max_tokens": 16000,
            "token_padding": 500,
            "max_completion_tokens": 2000,
            "max_messages": 500
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-16k",
            "max_tokens": 2000,
            "temperature": 0.1
        }
    },
    "gpt-3.5-turbo_default":{
        "model": "gpt-3.5-turbo",
        "name": "gpt-3.5-turbo_default",
        "id": 8,
        "info":{
            "description": "The default configuration for the gpt-3.5-turbo model",
            "tags": [
                "gpt-3.5-turbo",
                "default",
                "chat"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "token_padding": 50,
            "max_completion_tokens": 1000,
            "max_messages": 100
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.7
        }
    },
    "gpt-3.5-turbo_creative":{
        "model": "gpt-3.5-turbo",
        "name": "gpt-3.5-turbo_creative",
        "id": 9,
        "info":{
            "description": "Creative Mode for the gpt-3.5-turbo model",
            "tags": [
                "gpt-3.5-turbo",
                "creative",
                "chat",
                "high temperature"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "token_padding": 50,
            "max_completion_tokens": 1000,
            "max_messages": 100
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 1.0
        }
    },
    "gpt-3.5-turbo_precise":{
        "model": "gpt-3.5-turbo",
        "name": "gpt-3.5-turbo_precise",
        "id": 10,
        "info":{
            "description": "A precise configuration for the gpt-3.5-turbo model, meant to be used for precise responses. Low temp",
            "tags": [
                "gpt-3.5-turbo",
                "precise",
                "chat",
                "low temp",
                "conservative"
            ]
        },
        "trim_object": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "token_padding": 50,
            "max_completion_tokens": 1000,
            "max_messages": 100
        },
        "chat_completion_wrapper": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.1
        }}
}
# used as a quick way to generate a template json file
     