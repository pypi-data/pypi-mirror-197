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
    from dropbox_sign.model.sub_bulk_signer_list import SubBulkSignerList
    from dropbox_sign.model.sub_cc import SubCC
    from dropbox_sign.model.sub_custom_field import SubCustomField


def lazy_import():
    from dropbox_sign.model.sub_bulk_signer_list import SubBulkSignerList
    from dropbox_sign.model.sub_cc import SubCC
    from dropbox_sign.model.sub_custom_field import SubCustomField
    globals()['SubBulkSignerList'] = SubBulkSignerList
    globals()['SubCC'] = SubCC
    globals()['SubCustomField'] = SubCustomField


class SignatureRequestBulkCreateEmbeddedWithTemplateRequest(ModelNormal):
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
        ('message',): {
            'max_length': 5000,
        },
        ('metadata',): {
        },
        ('subject',): {
            'max_length': 255,
        },
        ('title',): {
            'max_length': 255,
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
            'template_ids': ([str],),  # noqa: E501
            'client_id': (str,),  # noqa: E501
            'signer_file': (file_type,),  # noqa: E501
            'signer_list': ([SubBulkSignerList],),  # noqa: E501
            'allow_decline': (bool,),  # noqa: E501
            'ccs': ([SubCC],),  # noqa: E501
            'custom_fields': ([SubCustomField],),  # noqa: E501
            'message': (str,),  # noqa: E501
            'metadata': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)},),  # noqa: E501
            'signing_redirect_url': (str,),  # noqa: E501
            'subject': (str,),  # noqa: E501
            'test_mode': (bool,),  # noqa: E501
            'title': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None

    @staticmethod
    def init(data: any) -> SignatureRequestBulkCreateEmbeddedWithTemplateRequest:
        """
        Attempt to instantiate and hydrate a new instance of this class
        """
        try:
            obj_data = json.dumps(data)
        except TypeError:
            obj_data = data

        return ApiClient().deserialize(
            response=type('obj_dict', (object,), {'data': obj_data}),
            response_type=[SignatureRequestBulkCreateEmbeddedWithTemplateRequest],
            _check_type=True,
        )

    attribute_map = {
        'template_ids': 'template_ids',  # noqa: E501
        'client_id': 'client_id',  # noqa: E501
        'signer_file': 'signer_file',  # noqa: E501
        'signer_list': 'signer_list',  # noqa: E501
        'allow_decline': 'allow_decline',  # noqa: E501
        'ccs': 'ccs',  # noqa: E501
        'custom_fields': 'custom_fields',  # noqa: E501
        'message': 'message',  # noqa: E501
        'metadata': 'metadata',  # noqa: E501
        'signing_redirect_url': 'signing_redirect_url',  # noqa: E501
        'subject': 'subject',  # noqa: E501
        'test_mode': 'test_mode',  # noqa: E501
        'title': 'title',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @property
    def template_ids(self) -> List[str]:
        return self.get("template_ids")

    @template_ids.setter
    def template_ids(self, value: List[str]):
        setattr(self, "template_ids", value)

    @property
    def client_id(self) -> str:
        return self.get("client_id")

    @client_id.setter
    def client_id(self, value: str):
        setattr(self, "client_id", value)

    @property
    def signer_file(self) -> file_type:
        return self.get("signer_file")

    @signer_file.setter
    def signer_file(self, value: file_type):
        setattr(self, "signer_file", value)

    @property
    def signer_list(self) -> List[SubBulkSignerList]:
        return self.get("signer_list")

    @signer_list.setter
    def signer_list(self, value: List[SubBulkSignerList]):
        setattr(self, "signer_list", value)

    @property
    def allow_decline(self) -> bool:
        return self.get("allow_decline")

    @allow_decline.setter
    def allow_decline(self, value: bool):
        setattr(self, "allow_decline", value)

    @property
    def ccs(self) -> List[SubCC]:
        return self.get("ccs")

    @ccs.setter
    def ccs(self, value: List[SubCC]):
        setattr(self, "ccs", value)

    @property
    def custom_fields(self) -> List[SubCustomField]:
        return self.get("custom_fields")

    @custom_fields.setter
    def custom_fields(self, value: List[SubCustomField]):
        setattr(self, "custom_fields", value)

    @property
    def message(self) -> str:
        return self.get("message")

    @message.setter
    def message(self, value: str):
        setattr(self, "message", value)

    @property
    def metadata(self) -> Dict[str, Union[bool, date, datetime, dict, float, int, list, str, none_type]]:
        return self.get("metadata")

    @metadata.setter
    def metadata(self, value: Dict[str, Union[bool, date, datetime, dict, float, int, list, str, none_type]]):
        setattr(self, "metadata", value)

    @property
    def signing_redirect_url(self) -> str:
        return self.get("signing_redirect_url")

    @signing_redirect_url.setter
    def signing_redirect_url(self, value: str):
        setattr(self, "signing_redirect_url", value)

    @property
    def subject(self) -> str:
        return self.get("subject")

    @subject.setter
    def subject(self, value: str):
        setattr(self, "subject", value)

    @property
    def test_mode(self) -> bool:
        return self.get("test_mode")

    @test_mode.setter
    def test_mode(self, value: bool):
        setattr(self, "test_mode", value)

    @property
    def title(self) -> str:
        return self.get("title")

    @title.setter
    def title(self, value: str):
        setattr(self, "title", value)

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, template_ids, client_id, *args, **kwargs):  # noqa: E501
        """SignatureRequestBulkCreateEmbeddedWithTemplateRequest - a model defined in OpenAPI

        Args:
            template_ids ([str]): Use `template_ids` to create a SignatureRequest from one or more templates, in the order in which the template will be used.
            client_id (str): Client id of the app you're using to create this embedded signature request. Used for security purposes.

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
            signer_file (file_type): `signer_file` is a CSV file defining values and options for signer fields. Required unless a `signer_list` is used, you may not use both. The CSV can have the following columns:  - `name`: the name of the signer filling the role of RoleName - `email_address`: email address of the signer filling the role of RoleName - `pin`: the 4- to 12-character access code that will secure this signer's signature page (optional) - `sms_phone_number`: An E.164 formatted phone number that will receive a code via SMS to access this signer's signature page. (optional)      **Note**: Not available in test mode and requires a Standard plan or higher. - `*_field`: any column with a _field\" suffix will be treated as a custom field (optional)      You may only specify field values here, any other options should be set in the custom_fields request parameter.  Example CSV:  ``` name, email_address, pin, company_field George, george@example.com, d79a3td, ABC Corp Mary, mary@example.com, gd9as5b, 123 LLC ```. [optional]  # noqa: E501
            signer_list ([SubBulkSignerList]): `signer_list` is an array defining values and options for signer fields. Required unless a `signer_file` is used, you may not use both.. [optional]  # noqa: E501
            allow_decline (bool): Allows signers to decline to sign a document if `true`. Defaults to `false`.. [optional] if omitted the server will use the default value of False  # noqa: E501
            ccs ([SubCC]): Add CC email recipients. Required when a CC role exists for the Template.. [optional]  # noqa: E501
            custom_fields ([SubCustomField]): When used together with merge fields, `custom_fields` allows users to add pre-filled data to their signature requests.  Pre-filled data can be used with \"send-once\" signature requests by adding merge fields with `form_fields_per_document` or [Text Tags](https://app.hellosign.com/api/textTagsWalkthrough#TextTagIntro) while passing values back with `custom_fields` together in one API call.  For using pre-filled on repeatable signature requests, merge fields are added to templates in the Dropbox Sign UI or by calling [/template/create_embedded_draft](/api/reference/operation/templateCreateEmbeddedDraft) and then passing `custom_fields` on subsequent signature requests referencing that template.. [optional]  # noqa: E501
            message (str): The custom message in the email that will be sent to the signers.. [optional]  # noqa: E501
            metadata ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}): Key-value data that should be attached to the signature request. This metadata is included in all API responses and events involving the signature request. For example, use the metadata field to store a signer's order number for look up when receiving events for the signature request.  Each request can include up to 10 metadata keys (or 50 nested metadata keys), with key names up to 40 characters long and values up to 1000 characters long.. [optional]  # noqa: E501
            signing_redirect_url (str): The URL you want signers redirected to after they successfully sign.. [optional]  # noqa: E501
            subject (str): The subject in the email that will be sent to the signers.. [optional]  # noqa: E501
            test_mode (bool): Whether this is a test, the signature request will not be legally binding if set to `true`. Defaults to `false`.. [optional] if omitted the server will use the default value of False  # noqa: E501
            title (str): The title you want to assign to the SignatureRequest.. [optional]  # noqa: E501
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

        self.template_ids = template_ids
        self.client_id = client_id
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
    def __init__(self, template_ids, client_id, *args, **kwargs):  # noqa: E501
        """SignatureRequestBulkCreateEmbeddedWithTemplateRequest - a model defined in OpenAPI

        Args:
            template_ids ([str]): Use `template_ids` to create a SignatureRequest from one or more templates, in the order in which the template will be used.
            client_id (str): Client id of the app you're using to create this embedded signature request. Used for security purposes.

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
            signer_file (file_type): `signer_file` is a CSV file defining values and options for signer fields. Required unless a `signer_list` is used, you may not use both. The CSV can have the following columns:  - `name`: the name of the signer filling the role of RoleName - `email_address`: email address of the signer filling the role of RoleName - `pin`: the 4- to 12-character access code that will secure this signer's signature page (optional) - `sms_phone_number`: An E.164 formatted phone number that will receive a code via SMS to access this signer's signature page. (optional)      **Note**: Not available in test mode and requires a Standard plan or higher. - `*_field`: any column with a _field\" suffix will be treated as a custom field (optional)      You may only specify field values here, any other options should be set in the custom_fields request parameter.  Example CSV:  ``` name, email_address, pin, company_field George, george@example.com, d79a3td, ABC Corp Mary, mary@example.com, gd9as5b, 123 LLC ```. [optional]  # noqa: E501
            signer_list ([SubBulkSignerList]): `signer_list` is an array defining values and options for signer fields. Required unless a `signer_file` is used, you may not use both.. [optional]  # noqa: E501
            allow_decline (bool): Allows signers to decline to sign a document if `true`. Defaults to `false`.. [optional] if omitted the server will use the default value of False  # noqa: E501
            ccs ([SubCC]): Add CC email recipients. Required when a CC role exists for the Template.. [optional]  # noqa: E501
            custom_fields ([SubCustomField]): When used together with merge fields, `custom_fields` allows users to add pre-filled data to their signature requests.  Pre-filled data can be used with \"send-once\" signature requests by adding merge fields with `form_fields_per_document` or [Text Tags](https://app.hellosign.com/api/textTagsWalkthrough#TextTagIntro) while passing values back with `custom_fields` together in one API call.  For using pre-filled on repeatable signature requests, merge fields are added to templates in the Dropbox Sign UI or by calling [/template/create_embedded_draft](/api/reference/operation/templateCreateEmbeddedDraft) and then passing `custom_fields` on subsequent signature requests referencing that template.. [optional]  # noqa: E501
            message (str): The custom message in the email that will be sent to the signers.. [optional]  # noqa: E501
            metadata ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}): Key-value data that should be attached to the signature request. This metadata is included in all API responses and events involving the signature request. For example, use the metadata field to store a signer's order number for look up when receiving events for the signature request.  Each request can include up to 10 metadata keys (or 50 nested metadata keys), with key names up to 40 characters long and values up to 1000 characters long.. [optional]  # noqa: E501
            signing_redirect_url (str): The URL you want signers redirected to after they successfully sign.. [optional]  # noqa: E501
            subject (str): The subject in the email that will be sent to the signers.. [optional]  # noqa: E501
            test_mode (bool): Whether this is a test, the signature request will not be legally binding if set to `true`. Defaults to `false`.. [optional] if omitted the server will use the default value of False  # noqa: E501
            title (str): The title you want to assign to the SignatureRequest.. [optional]  # noqa: E501
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

        self.template_ids = template_ids
        self.client_id = client_id
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
