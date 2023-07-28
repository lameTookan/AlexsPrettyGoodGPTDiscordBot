import logging
import sys
import uuid
from collections import namedtuple
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from log_config import BaseLogger, DEFAULT_LOGGING_LEVEL
import exceptions
import func
from log_config import DEFAULT_LOGGING_LEVEL

ParamInfo = namedtuple("ParamInfo", ["name", "type", "range", "description"])
param_info = {
    "max_tokens": ParamInfo(
        "max_tokens", int, None, "The maximum number of tokens to generate."
    ),
    "stream": ParamInfo("stream", bool, None, "Whether to stream the results or not.(output the tokens as they come in)"),
    "temperature": ParamInfo(
        "temperature",
        float,
        (0.0, 2.0),
        "Influences the randomness of the predictions. Lower values means the model will be more deterministic and repetitive. Higher values means the model will be more surprising and creative. Valid values are between 0.0 and 2.0, but values over 1.0 can lead to poor quality results.",
    ),
    "top_p": ParamInfo(
        "top_p",
        float,
        (0.0, 1.0),
        "Similar to temperature, but instead of sampling from the most likely tokens, it will sample from the tokens whose cumulative probability exceeds the value of top_p. Lower values of top_p means the model will be more deterministic. Higher values of top_p means the model will be more creative. Must be between 0.0 and 1.0. Recommended to either change top_p or temperature, but not both.",
    ),
    "presence_penalty": ParamInfo(
        "presence_penalty",
        float,
        (0.0, 2.0),
        "Controls how much the model favors repeating existing elements of the context. Lower values means the model is more likely to repeat existing elements. Higher values means the model is less likely to repeat existing elements.",
    ),
    "frequency_penalty": ParamInfo(
        "frequency_penalty",
        float,
        (0.0, 2.0),
        "Controls how much the model favors repeating elements of the response. Lower values means the model is more likely to repeat elements. Higher values means the model is less likely to repeat elements.",
    ),
}


class ModelParameters:
    """
    This class is used to store and validate the parameters for the model.
    The parameters are stored as private variables, and can be accessed and set using the properties.
    All parameters are validated using the param_info dict, which contains the name, type, range, and description of each parameter.
    These are all optional, if not provided they will not be outputted by get_param_kwargs(). (meant to be used directly in the ChatCompletion OpenAI object)
    Dependencies:
        - uuid
        - collections.namedtuple
        - Typing
    Raises:
        exceptions.InvalidParamNameError: If the name of the parameter is not in the param_info dict.
        exceptions.BadModelParamError: If the value of the parameter is not valid.
    Attributes:
        version: The version of the class.
        uuid: A unique identifier for the object.
        param_info_dict: A dict containing the name, type, range, and description of each parameter. Stored as a namedtuple.
        _max_tokens: The maximum number of tokens to generate.
        _temperature: Influences the randomness of the predictions. Lower values means the model will be more deterministic and repetitive. Higher values means the model will be more surprising and creative. Valid values are between 0.0 and 2.0, but values over 1.0 can lead to poor quality results.
        _top_p: Similar to temperature, but instead of sampling from the most likely tokens, it will sample from the tokens whose cumulative probability exceeds the value of top_p. Lower values of top_p means the model will be more deterministic. Higher values of top_p means the model will be more creative. Must be between 0.0 and 1.0. Recommended to either change top_p or temperature, but not both.
        _presence_penalty: Controls how much the model favors repeating existing elements of the context. Lower values means the model is more likely to repeat existing elements. Higher values means the model is less likely to repeat existing elements.
        _frequency_penalty: Controls how much the model favors repeating elements of the response. Lower values means the model is more likely to repeat elements. Higher values means the model is less likely to repeat elements.
    Methods:
        Setters And Getters for each parameter.add()
        Core Methods:
            get_param_kwargs: Returns a dict of the parameters and their values. Values are only included if they are not None.
            set_params: Sets the parameters using a dict of the parameters and their values. 
            get_all_params: Returns a dict of all the parameters and their values.(including None values)
        Private Methods:
            _process_special_values: Returns a tuple of (True, value) if the value is a special value, or (False, value) if the value is not a special value. Special values are "None" and "Zero".
            _validate_params: Uses the param_info dict to validate the parameters.
        Save And Load Methods:
            make_save_dict: Returns a dict of the parameters and their values. All values are included as well as the param_info_dict.add()
            _verify_save_dict: Verifies that the save dict is valid.
            load_from_save_dict: Loads the parameters from a save dict.
            
    Example Usage:
        params = ModelParameters()
        params.max_tokens = 1000
        params.temperature = 0.5
        params.top_p = "zero"
        params.presence_penalty = 0.5
        openai.ChatCompletion.create(model="gpt-4", messages = [<messages], **params.get_param_kwargs()
    
    
    """
  
    version = "2.2.0"
    #added stream parameter
    def __init__(
        self,
        param_info_dict: dict = param_info,
        max_tokens: int = None,
        temperature: float = None,
        top_p: float = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        stream: bool = False,
    ):
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._presence_penalty = presence_penalty
        self._frequency_penalty = frequency_penalty
        self._top_p = top_p
        self.param_info_dict = param_info_dict
        self.uuid = str(uuid.uuid4())
        self._stream = stream
        
        
        self.logger = BaseLogger(__file__, "model_parameters.log", identifier="ModelParameters", level=DEFAULT_LOGGING_LEVEL)
        #self.logger.addHandler(stream_handler) 
        self.logger.info(f"Created ModelParameters Object with the following parameters: {self.get_all_params_dict()}")  
    def __repr__(self):
        msg_list = [
            "ModelParameters Object with the following parameters:",
            "uuid: " + self.uuid,
            "Model Parameters:",
                
        ]
        indents = " " * 4
        for param in self.get_all_params_dict():
            msg_list.append(f"{indents}{param}: {str(self.get_all_params_dict()[param])}")
        return "\n".join(msg_list)
            
    
             
    def _process_special_values(
        self, value: str | float | int
    ) -> tuple[bool, int | float]:
        """Returns a tuple of (True, value) if the value is a special value, or (False, value) if the value is not a special value."""
        val = str(value)
        if val.lower() == "none":
            return (True, None)
        elif val.lower() == "zero":
            return (True, 0)
        else:
            return (False, value)
    ParamInfo = namedtuple("ParamInfo", ["name", "type", "range", "description"])

    def _validate_params(self, name: str, value: int | float) -> dict:
    
        """Uses the param_info dict to validate the parameters"""
        if name not in self.param_info_dict:
            raise exceptions.InvalidParamNameError(
                name=name, allowed_params=self.param_info_dict.keys()
            )
        param_info: ParamInfo = self.param_info_dict[name]
        try:
            value = param_info.type(value)
        except Exception as e:
            self.logger.error(f"Invalid value for {name}: {value}") 
            self.logger.debug(f"Raising BadModelParamError, id: {id(exceptions.BadModelParamError)}")

            raise exceptions.BadModelParamError(param={name: value}, param_info_dict=self.param_info_dict) from e
        if not isinstance(value, param_info.type):
            raise exceptions.BadModelParamError({name: value}, self.param_info_dict)
        if param_info.range is not None:
            if value < param_info.range[0] or value > param_info.range[1]:
                raise exceptions.BadModelParamError({name: value}, self.param_info_dict)
        else:
            if value < 0:
                raise exceptions.BadModelParamError({name: value}, self.param_info_dict)
        return {name: value}
    @property
    def stream(self) -> bool:
        """Gets the stream parameter"""
        return self._stream
    @stream.setter
    def stream(self, value: bool) -> None:
        """Sets the stream parameter, value must be a bool"""
        if not isinstance(value, bool):
            raise exceptions.BadModelParamError({"stream": value}, self.param_info_dict)
        self._stream = value
        self.logger.debug(f"Set stream to {value}")
    def toggle_stream(self) -> None:
        """If the stream parameter is True, sets it to False, and vice versa"""
        self.stream = not self.stream
    @property
    def top_p(self) -> float:
        return self._top_p
    

    @top_p.setter
    def top_p(self, value: float):
        """Sets the top_p, value must be between 0 and 1."""
        special, new_val = self._process_special_values(value)
        if special is True:
            self._top_p = new_val
            self.logger.debug(f"Set top_p to {new_val}, using special value")
            return None
            
        value = self._validate_params("top_p", value)["top_p"]
        self._top_p = value
        self.logger.debug(f"Set top_p to {value}")

    @property
    def max_tokens(self) -> int:
        """Gets the max tokens."""
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value) -> None:
        """Sets the max tokens, value must be an positive integer."""
        special, new_val = self._process_special_values(value)
        if special is True:
            self._max_tokens = new_val
            self.logger.debug(f"Set max tokens to {new_val}, using special value")
            return None
        value = self._validate_params("max_tokens", value)["max_tokens"]
        self._max_tokens = value
        self.logger.debug(f"Set max tokens to {value}")

    @property
    def temperature(self) -> float:
        """Gets the temperature, ."""
        return self._temperature

    @temperature.setter
    def temperature(self, value) -> None:
        """Sets the temperature, value must be between 0 and 2."""
        special, new_val = self._process_special_values(value)
        if special is True:
            self._temperature = new_val
            self.logger.debug(f"Set temperature to {new_val}, using special value")
            return None
        value = self._validate_params("temperature", value)["temperature"]
        self._temperature = value
        self.logger.debug(f"Set temperature to {value}")

    @property
    def presence_penalty(self) -> float:
        return self._presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, value) -> None:
        """Sets the presence penalty, value must be between 0 and 2."""
        special, new_val = self._process_special_values(value)
        if special is True:
            self._presence_penalty = new_val
            self.logger.debug(f"Set presence penalty to {new_val}, using special value")
            return None
        value = self._validate_params("presence_penalty", value)["presence_penalty"]
        self._presence_penalty = value
        self.logger.debug(f"Set presence penalty to {value}")

    @property
    def frequency_penalty(self) -> float:
        """Gets the frequency penalty"""
        return self._frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, value) -> None:
        """Sets the frequency penalty, value must be between 0 and 2."""
        special, new_val = self._process_special_values(value)
        if special is True:
            self._frequency_penalty = new_val
            self.logger.debug(f"Set frequency penalty to {new_val}, using special value")
            return None
        value = self._validate_params("frequency_penalty", value)["frequency_penalty"]
        self._frequency_penalty = value
        self.logger.debug(f"Set frequency penalty to {value}")

    def get_param_kwargs(self) -> dict:
        """Gets all the parameters of the model as a dictionary, does not include ones that are not currently set(ie. None). For all parameters, use get_all_params_dict()"""
        def add_to_dict_if_not_none(d: dict, name: str, value: int | float):
            if value is not None:
                d[name] = value

        kwargs = {}
        add_to_dict_if_not_none(kwargs, "max_tokens", self.max_tokens)
        add_to_dict_if_not_none(kwargs, "temperature", self.temperature)
        add_to_dict_if_not_none(kwargs, "top_p", self.top_p)
        add_to_dict_if_not_none(kwargs, "presence_penalty", self.presence_penalty)
        add_to_dict_if_not_none(kwargs, "frequency_penalty", self.frequency_penalty)
        if self.stream is True:
            kwargs["stream"] = self.stream
        self.logger.debug(f"Got param kwargs: {kwargs}")
        return kwargs

    def get_all_params_dict(self):
        """Gets all the parameters of the model as a dictionary, includes ones that are not currently set(ie. None)"""

        d=  {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "stream": self.stream,
        }
        self.logger.debug(f"Got all params dict: {d}")
        return d

    def set_params(self, **kwargs):
        """Validates and changes the parameters of the model. Raises a BadModelParamError if the parameters are invalid.
        Valid parameters are:
            max_tokens: int
            temperature: float
            presence_penalty: float
            frequency_penalty: float
            top_p: float
            stream: bool

        """
        if len(kwargs) == 0:
            return None
        for name, value in kwargs.items():
            if name not in self.param_info_dict:
                self.logger.error(f"Invalid param name: {name}")
                raise exceptions.InvalidParamNameError(
                    param_name=name, allowed_params=self.param_info_dict.keys()
                )
            if name == "max_tokens":
                self.max_tokens = value
                self.logger.debug(f"Set max tokens to {value}")
            elif name == "temperature":
                self.temperature = value
            elif name == "presence_penalty":
                self.presence_penalty = value
            elif name == "frequency_penalty":
                self.frequency_penalty = value
            elif name == "top_p":
                self.top_p = value
            elif name == "stream":
                self.stream = value
                
                
    def make_save_dict(self):
        """Returns a dictionary that can be used to save the model"""
        save = self.get_all_params_dict()
        
        save.update({"uuid": str(self.uuid)})
        self.logger.debug(f"Made save dict: {save}")
        return save
    def _check_save_dict(self, save_dict: dict ) -> dict:
        """Checks if the save dict is valid, returns the save dict if it is valid, otherwise raises an error"""
        if "uuid" not in save_dict or not isinstance(save_dict["uuid"], str):
            raise exceptions.BadSaveDictionaryError("ModelParameter Save Dictionary must have a uuid key")
        if not isinstance(save_dict, dict):
            raise exceptions.BadSaveDictionaryError("ModelParameter Save Dictionary must be a dictionary")
        
        if  {"max_tokens", "temperature", "top_p", "presence_penalty", "frequency_penalty", "stream"} -  set(save_dict.keys()) != set():
            raise exceptions.BadSaveDictionaryError("ModelParameter Save Dictionary's Must have the keys: max_tokens, temperature, presence_penalty, frequency_penalty, top_p")
        return save_dict
    def load_from_save_dict(self, save_dict: dict):
        """Loads the model parameters from a save dict"""
        save_dict = self._check_save_dict(save_dict)
        self.uuid = save_dict["uuid"]
        self.max_tokens = save_dict["max_tokens"]
        self.temperature = save_dict["temperature"]
        self.presence_penalty = save_dict["presence_penalty"]
        self.frequency_penalty = save_dict["frequency_penalty"]
        self.top_p = save_dict["top_p"]
        self.logger.debug(f"Loaded from save dict: {save_dict}")
    
    
        
        
