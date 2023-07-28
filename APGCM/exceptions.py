from collections import namedtuple


class PrettyGoodError(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "Alex's Pretty Good Error"
        self.message = message
    def __str__(self):
        return self.message
#general purpose errors 
class MissingValueError(PrettyGoodError):
    def __init__(self, msg = None):
        if msg is None:
            msg = "A required value is missing."
        self.message = msg
class BadFormatError(PrettyGoodError):
    pass
# for chat.message.Message class/MessageFactory class
class BadRoleError(PrettyGoodError):
    def __init__(self, role: str = None, allowed_roles: set = {"user, assistant, system"}):
        if role is None:
            role = "bad"
        self.role = role
        self.allowed_roles = allowed_roles
        self.message = f"Role must be one of {self.allowed_roles} not {self.role}"
class NoRoleProvidedError(PrettyGoodError):
    def __init__(self, message: str = None):
        if message is None:
            self.message = "No role provided."
        else: 
            self.message = message
            
#following is for ChatLog class, in chat module
class NotAMessageError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Must provide a message."
        else:
            self.message = message
            
class BadSaveDictionaryError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Bad or corrupt save dictionary."
        else:
            self.message = message
class BadMessageDictionaryError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Bad or corrupt message dictionary. Message dictionary must have 'role' and 'content' keys."
        else:
            self.message = message
            
# for paramater validation
# copy of param help dict
ParamInfo = namedtuple('ParamInfo', ['name', 'type', 'range', 'description'])
param_info = {
    'max_tokens': ParamInfo('max_tokens', int, None, 'The maximum number of tokens to generate.'),
    "temperature": ParamInfo("temperature", float, (0.0, 2.0), "Influences the randomness of the predictions. Lower values means the model will be more deterministic and repetitive. Higher values means the model will be more surprising and creative. Valid values are between 0.0 and 2.0, but values over 1.0 can lead to poor quality results."),
    "top_p": ParamInfo("top_p", float, (0.0, 1.0), "Similar to temperature, but instead of sampling from the most likely tokens, it will sample from the tokens whose cumulative probability exceeds the value of top_p. Lower values of top_p means the model will be more deterministic. Higher values of top_p means the model will be more creative. Must be between 0.0 and 1.0. Recommended to either change top_p or temperature, but not both."),
    "presence_penalty": ParamInfo("presence_penalty", float, (0.0, 2.0), "Controls how much the model favors repeating existing elements of the context. Lower values means the model is more likely to repeat existing elements. Higher values means the model is less likely to repeat existing elements."),
    "frequency_penalty": ParamInfo("frequency_penalty", float, (0.0, 2.0), "Controls how much the model favors repeating elements of the response. Lower values means the model is more likely to repeat elements. Higher values means the model is less likely to repeat elements."),
    
}

class InvalidParamNameError(PrettyGoodError):
    def __init__(self, param_name: str = None, allowed_params: set = {"temperature", "top_p", "max_tokens",  "presence_penalty", "frequency_penalty", }):
        if param_name is None:
            param_name = "bad"
        self.message =f"Parameter name must be one of {allowed_params} not {param_name}"
class BadModelParamError(PrettyGoodError):
    def __init__(self, param: dict = None , param_info_dict: dict = param_info):
        msg_list = []
        if param is None: 
            msg_list.append("An Invalid parameter was provided.")
            msg_list.append("More information about the parameters:")
            for key, value in param_info_dict.items():
                msg_list.append("Parameter name: " + value.name)
                msg_list.append("Parameter type: " + str(value.type))
                if value.range is not None:
                    msg_list.append("Parameter range: " + str(value.range))
                msg_list.append("Parameter description: " + value.description)
                msg_list.append('====================')
        else:
            param_name = list(param.keys())[0]
            param_value = list(param.values())[0]
            param_type = type(param_value)
            info = param_info_dict.get(param_name, None)
            msg_list.append(f"Parameter {param_name} has value {param_value} and a type of {param_type}, which is invalid.")
            if info is not None:
                msg_list.append("More information about the parameters:")
                msg_list.append("Parameter name: " + info.name)
                msg_list.append("Parameter type: " + str(info.type))
                if info.range is not None:
                    msg_list.append("Parameter range: " + str(info.range))
                msg_list.append("Parameter description: " + info.description)
            self.message = "\n".join(msg_list)
                
                
class BadMessageError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Bad or corrupt message dictionary. Message dictionary must have 'role' and 'content' keys."
        else:
            self.message = message
                
# for chat wrapper 
class IncorrectObjectTypeError(PrettyGoodError):
    def __init__(self, message = None):
        
        if message is None:
            self.message = "Incorrect object type."
        else:
            self.message = message
            
class ObjectNotSetupError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Object not setup, please ensure that all required objects are either passed in or created."
        else:
            self.message = message
class InvalidReturnTypeError(PrettyGoodError):
    def __init__(self, message = None, bad_type: str = None,allowed_types: set ={"str", "dict", "Message", "pretty"}):
        msg_list = []
        if message is None:
            msg_list.append( "Invalid return type.")
        else:
            msg_list.append(message)
        msg_list.append(f"Return type must be one of {allowed_types}")
        if bad_type is not None:
            msg_list.append(f"Not {bad_type}")
        self.message = "\n".join(msg_list)  

# for file manager 
class FileExistsError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "File already exists."
        else:
            self.message = message
            
            
class FileNotFoundError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "File not found."
        else:
            self.message = message
            
class BadTypeError(PrettyGoodError):
    def __init__(self, message = None):
        if message is None:
            self.message = "Incorrect type."
        else:
            self.message = message
class BadJSONFileError(PrettyGoodError):
    def __init__(self, message: str = None ):
        if message is None:
            self.message = "Bad or corrupt JSON file."
        else:
            self.message = message
            
# for template manager
class BadTemplateDict(PrettyGoodError):
    def __init__(self, message: str = None):
        if message is None:
            self.message = "Bad or corrupt template dictionary."
        else:
            self.message = message
class BadTemplateError(PrettyGoodError):
    def __init__(self, message: str = None):
        if message is None:
            self.message = "Bad or corrupt template."
        else:
            self.message = message
class TemplateNotFoundError(PrettyGoodError):
    def __init__(self, message: str = None):
        if message is None:
            self.message = "Template not found."
        else:
            self.message = message
            
class BadFileNameError(PrettyGoodError):
    def __init__(self, message: str = None):
        if message is None:
            self.message = "Bad file name."
        else:
            self.message = message
            
            
class BadMessageReturnTypeError(PrettyGoodError):
    """Raised when the return type of a message is not one of the allowed types."""
    def __init__(self, msg: str = None):
        if msg is None:
            msg = "Bad message return type. Must be one of the following: 'str', 'dict', 'Message', 'pretty'"
        self.message = msg
    