"""
    Dropbox Sign API

    Dropbox Sign v3 API  # noqa: E501

    The version of the OpenAPI document: 3.0.0
    Contact: apisupport@hellosign.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List, Dict, Union
import json  # noqa: F401
import re  # noqa: F401
import sys  # noqa: F401

from dropbox_sign import ApiClient
from dropbox_sign.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from dropbox_sign.exceptions import ApiAttributeError
if TYPE_CHECKING:
    from dropbox_sign.model.sub_o_auth import SubOAuth
    from dropbox_sign.model.sub_options import SubOptions
    from dropbox_sign.model.sub_white_labeling_options import SubWhiteLabelingOptions


def lazy_import():
    from dropbox_sign.model.sub_o_auth import SubOAuth
    from dropbox_sign.model.sub_options import SubOptions
    from dropbox_sign.model.sub_white_labeling_options import SubWhiteLabelingOptions
    globals()['SubOAuth'] = SubOAuth
    globals()['SubOptions'] = SubOptions
    globals()['SubWhiteLabelingOptions'] = SubWhiteLabelingOptions


class ApiAppUpdateRequest(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('domains',): {
            'max_items': 2,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'callback_url': (str,),  # noqa: E501
            'custom_logo_file': (file_type,),  # noqa: E501
            'domains': ([str],),  # noqa: E501
            'name': (str,),  # noqa: E501
            'oauth': (SubOAuth,),  # noqa: E501
            'options': (SubOptions,),  # noqa: E501
            'white_labeling_options': (SubWhiteLabelingOptions,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None

    @staticmethod
    def init(data: any) -> ApiAppUpdateRequest:
        """
        Attempt to instantiate and hydrate a new instance of this class
        """
        try:
            obj_data = json.dumps(data)
        except TypeError:
            obj_data = data

        return ApiClient().deserialize(
            response=type('obj_dict', (object,), {'data': obj_data}),
            response_type=[ApiAppUpdateRequest],
            _check_type=True,
        )

    attribute_map = {
        'callback_url': 'callback_url',  # noqa: E501
        'custom_logo_file': 'custom_logo_file',  # noqa: E501
        'domains': 'domains',  # noqa: E501
        'name': 'name',  # noqa: E501
        'oauth': 'oauth',  # noqa: E501
        'options': 'options',  # noqa: E501
        'white_labeling_options': 'white_labeling_options',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @property
    def callback_url(self) -> str:
        return self.get("callback_url")

    @callback_url.setter
    def callback_url(self, value: str):
        setattr(self, "callback_url", value)

    @property
    def custom_logo_file(self) -> file_type:
        return self.get("custom_logo_file")

    @custom_logo_file.setter
    def custom_logo_file(self, value: file_type):
        setattr(self, "custom_logo_file", value)

    @property
    def domains(self) -> List[str]:
        return self.get("domains")

    @domains.setter
    def domains(self, value: List[str]):
        setattr(self, "domains", value)

    @property
    def name(self) -> str:
        return self.get("name")

    @name.setter
    def name(self, value: str):
        setattr(self, "name", value)

    @property
    def oauth(self) -> SubOAuth:
        return self.get("oauth")

    @oauth.setter
    def oauth(self, value: SubOAuth):
        setattr(self, "oauth", value)

    @property
    def options(self) -> SubOptions:
        return self.get("options")

    @options.setter
    def options(self, value: SubOptions):
        setattr(self, "options", value)

    @property
    def white_labeling_options(self) -> SubWhiteLabelingOptions:
        return self.get("white_labeling_options")

    @white_labeling_options.setter
    def white_labeling_options(self, value: SubWhiteLabelingOptions):
        setattr(self, "white_labeling_options", value)

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """ApiAppUpdateRequest - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            callback_url (str): The URL at which the API App should receive event callbacks.. [optional]  # noqa: E501
            custom_logo_file (file_type): An image file to use as a custom logo in embedded contexts. (Only applies to some API plans). [optional]  # noqa: E501
            domains ([str]): The domain names the ApiApp will be associated with.. [optional]  # noqa: E501
            name (str): The name you want to assign to the ApiApp.. [optional]  # noqa: E501
            oauth (SubOAuth): [optional]  # noqa: E501
            options (SubOptions): [optional]  # noqa: E501
            white_labeling_options (SubWhiteLabelingOptions): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """ApiAppUpdateRequest - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            callback_url (str): The URL at which the API App should receive event callbacks.. [optional]  # noqa: E501
            custom_logo_file (file_type): An image file to use as a custom logo in embedded contexts. (Only applies to some API plans). [optional]  # noqa: E501
            domains ([str]): The domain names the ApiApp will be associated with.. [optional]  # noqa: E501
            name (str): The name you want to assign to the ApiApp.. [optional]  # noqa: E501
            oauth (SubOAuth): [optional]  # noqa: E501
            options (SubOptions): [optional]  # noqa: E501
            white_labeling_options (SubWhiteLabelingOptions): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
