# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5314
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class AborRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'code': 'str',
        'portfolio_ids': 'list[PortfolioEntityId]',
        'description': 'str',
        'abor_config': 'ResourceId',
        'properties': 'dict(str, ModelProperty)'
    }

    attribute_map = {
        'code': 'code',
        'portfolio_ids': 'portfolioIds',
        'description': 'description',
        'abor_config': 'aborConfig',
        'properties': 'properties'
    }

    required_map = {
        'code': 'required',
        'portfolio_ids': 'required',
        'description': 'optional',
        'abor_config': 'required',
        'properties': 'optional'
    }

    def __init__(self, code=None, portfolio_ids=None, description=None, abor_config=None, properties=None, local_vars_configuration=None):  # noqa: E501
        """AborRequest - a model defined in OpenAPI"
        
        :param code:  The code given for the Abor. (required)
        :type code: str
        :param portfolio_ids:  The list with the portfolio ids which are part of the Abor. For now the only supported value is SinglePortfolio. (required)
        :type portfolio_ids: list[lusid.PortfolioEntityId]
        :param description:  The description for the Abor.
        :type description: str
        :param abor_config:  (required)
        :type abor_config: lusid.ResourceId
        :param properties:  Properties to add to the Abor.
        :type properties: dict[str, lusid.ModelProperty]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._code = None
        self._portfolio_ids = None
        self._description = None
        self._abor_config = None
        self._properties = None
        self.discriminator = None

        self.code = code
        self.portfolio_ids = portfolio_ids
        self.description = description
        self.abor_config = abor_config
        self.properties = properties

    @property
    def code(self):
        """Gets the code of this AborRequest.  # noqa: E501

        The code given for the Abor.  # noqa: E501

        :return: The code of this AborRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this AborRequest.

        The code given for the Abor.  # noqa: E501

        :param code: The code of this AborRequest.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) > 64):
            raise ValueError("Invalid value for `code`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 1):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', code)):  # noqa: E501
            raise ValueError(r"Invalid value for `code`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._code = code

    @property
    def portfolio_ids(self):
        """Gets the portfolio_ids of this AborRequest.  # noqa: E501

        The list with the portfolio ids which are part of the Abor. For now the only supported value is SinglePortfolio.  # noqa: E501

        :return: The portfolio_ids of this AborRequest.  # noqa: E501
        :rtype: list[lusid.PortfolioEntityId]
        """
        return self._portfolio_ids

    @portfolio_ids.setter
    def portfolio_ids(self, portfolio_ids):
        """Sets the portfolio_ids of this AborRequest.

        The list with the portfolio ids which are part of the Abor. For now the only supported value is SinglePortfolio.  # noqa: E501

        :param portfolio_ids: The portfolio_ids of this AborRequest.  # noqa: E501
        :type portfolio_ids: list[lusid.PortfolioEntityId]
        """
        if self.local_vars_configuration.client_side_validation and portfolio_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `portfolio_ids`, must not be `None`")  # noqa: E501

        self._portfolio_ids = portfolio_ids

    @property
    def description(self):
        """Gets the description of this AborRequest.  # noqa: E501

        The description for the Abor.  # noqa: E501

        :return: The description of this AborRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this AborRequest.

        The description for the Abor.  # noqa: E501

        :param description: The description of this AborRequest.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    @property
    def abor_config(self):
        """Gets the abor_config of this AborRequest.  # noqa: E501


        :return: The abor_config of this AborRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._abor_config

    @abor_config.setter
    def abor_config(self, abor_config):
        """Sets the abor_config of this AborRequest.


        :param abor_config: The abor_config of this AborRequest.  # noqa: E501
        :type abor_config: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and abor_config is None:  # noqa: E501
            raise ValueError("Invalid value for `abor_config`, must not be `None`")  # noqa: E501

        self._abor_config = abor_config

    @property
    def properties(self):
        """Gets the properties of this AborRequest.  # noqa: E501

        Properties to add to the Abor.  # noqa: E501

        :return: The properties of this AborRequest.  # noqa: E501
        :rtype: dict[str, lusid.ModelProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this AborRequest.

        Properties to add to the Abor.  # noqa: E501

        :param properties: The properties of this AborRequest.  # noqa: E501
        :type properties: dict[str, lusid.ModelProperty]
        """

        self._properties = properties

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AborRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AborRequest):
            return True

        return self.to_dict() != other.to_dict()
