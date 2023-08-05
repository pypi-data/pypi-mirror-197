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
    from dropbox_sign.model.template_response_document_custom_field_base import TemplateResponseDocumentCustomFieldBase


def lazy_import():
    from dropbox_sign.model.template_response_document_custom_field_base import TemplateResponseDocumentCustomFieldBase
    globals()['TemplateResponseDocumentCustomFieldBase'] = TemplateResponseDocumentCustomFieldBase


class TemplateResponseDocumentCustomFieldCheckbox(ModelComposed):
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
            'type': (str,),  # noqa: E501
            'api_id': (str,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'signer': (str, none_type,),  # noqa: E501
            'x': (int,),  # noqa: E501
            'y': (int,),  # noqa: E501
            'width': (int,),  # noqa: E501
            'height': (int,),  # noqa: E501
            'required': (bool,),  # noqa: E501
            'group': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None

    @staticmethod
    def init(data: any) -> TemplateResponseDocumentCustomFieldCheckbox:
        """
        Attempt to instantiate and hydrate a new instance of this class
        """
        try:
            obj_data = json.dumps(data)
        except TypeError:
            obj_data = data

        return ApiClient().deserialize(
            response=type('obj_dict', (object,), {'data': obj_data}),
            response_type=[TemplateResponseDocumentCustomFieldCheckbox],
            _check_type=True,
        )


    attribute_map = {
        'type': 'type',  # noqa: E501
        'api_id': 'api_id',  # noqa: E501
        'name': 'name',  # noqa: E501
        'signer': 'signer',  # noqa: E501
        'x': 'x',  # noqa: E501
        'y': 'y',  # noqa: E501
        'width': 'width',  # noqa: E501
        'height': 'height',  # noqa: E501
        'required': 'required',  # noqa: E501
        'group': 'group',  # noqa: E501
    }

    read_only_vars = {
    }

    @property
    def type(self) -> str:
        return self.get("type")

    @type.setter
    def type(self, value: str):
        setattr(self, "type", value)

    @property
    def api_id(self) -> str:
        return self.get("api_id")

    @api_id.setter
    def api_id(self, value: str):
        setattr(self, "api_id", value)

    @property
    def name(self) -> str:
        return self.get("name")

    @name.setter
    def name(self, value: str):
        setattr(self, "name", value)

    @property
    def signer(self) -> Optional[str]:
        return self.get("signer")

    @signer.setter
    def signer(self, value: Optional[str]):
        setattr(self, "signer", value)

    @property
    def x(self) -> int:
        return self.get("x")

    @x.setter
    def x(self, value: int):
        setattr(self, "x", value)

    @property
    def y(self) -> int:
        return self.get("y")

    @y.setter
    def y(self, value: int):
        setattr(self, "y", value)

    @property
    def width(self) -> int:
        return self.get("width")

    @width.setter
    def width(self, value: int):
        setattr(self, "width", value)

    @property
    def height(self) -> int:
        return self.get("height")

    @height.setter
    def height(self, value: int):
        setattr(self, "height", value)

    @property
    def required(self) -> bool:
        return self.get("required")

    @required.setter
    def required(self, value: bool):
        setattr(self, "required", value)

    @property
    def group(self) -> Optional[str]:
        return self.get("group")

    @group.setter
    def group(self, value: Optional[str]):
        setattr(self, "group", value)

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """TemplateResponseDocumentCustomFieldCheckbox - a model defined in OpenAPI

        Keyword Args:
            type (str): The type of this Custom Field. Only `text` and `checkbox` are currently supported.  * Text uses `TemplateResponseDocumentCustomFieldText` * Checkbox uses `TemplateResponseDocumentCustomFieldCheckbox`. defaults to "checkbox"  # noqa: E501
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
            api_id (str): The unique ID for this field.. [optional]  # noqa: E501
            name (str): The name of the Custom Field.. [optional]  # noqa: E501
            signer (str, none_type): The signer of the Custom Field. Can be `null` if field is a merge field (assigned to Sender).. [optional]  # noqa: E501
            x (int): The horizontal offset in pixels for this form field.. [optional]  # noqa: E501
            y (int): The vertical offset in pixels for this form field.. [optional]  # noqa: E501
            width (int): The width in pixels of this form field.. [optional]  # noqa: E501
            height (int): The height in pixels of this form field.. [optional]  # noqa: E501
            required (bool): Boolean showing whether or not this field is required.. [optional]  # noqa: E501
            group (str, none_type): The name of the group this field is in. If this field is not a group, this defaults to `null`.. [optional]  # noqa: E501
        """

        type = kwargs.get('type', "checkbox")
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        composed_info = validate_get_composed_info(
            constant_args, kwargs, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        discarded_args = composed_info[3]

        for var_name, var_value in kwargs.items():
            if var_name in discarded_args and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self._additional_properties_model_instances:
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
        '_composed_instances',
        '_var_name_to_model_instances',
        '_additional_properties_model_instances',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """TemplateResponseDocumentCustomFieldCheckbox - a model defined in OpenAPI

        Keyword Args:
            type (str): The type of this Custom Field. Only `text` and `checkbox` are currently supported.  * Text uses `TemplateResponseDocumentCustomFieldText` * Checkbox uses `TemplateResponseDocumentCustomFieldCheckbox`. defaults to "checkbox"  # noqa: E501
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
            api_id (str): The unique ID for this field.. [optional]  # noqa: E501
            name (str): The name of the Custom Field.. [optional]  # noqa: E501
            signer (str, none_type): The signer of the Custom Field. Can be `null` if field is a merge field (assigned to Sender).. [optional]  # noqa: E501
            x (int): The horizontal offset in pixels for this form field.. [optional]  # noqa: E501
            y (int): The vertical offset in pixels for this form field.. [optional]  # noqa: E501
            width (int): The width in pixels of this form field.. [optional]  # noqa: E501
            height (int): The height in pixels of this form field.. [optional]  # noqa: E501
            required (bool): Boolean showing whether or not this field is required.. [optional]  # noqa: E501
            group (str, none_type): The name of the group this field is in. If this field is not a group, this defaults to `null`.. [optional]  # noqa: E501
        """

        type = kwargs.get('type', "checkbox")
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        composed_info = validate_get_composed_info(
            constant_args, kwargs, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        discarded_args = composed_info[3]

        for var_name, var_value in kwargs.items():
            if var_name in discarded_args and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self._additional_properties_model_instances:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")

    @cached_property
    def _composed_schemas():
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        lazy_import()
        return {
          'anyOf': [
          ],
          'oneOf': [
          ],
        }
