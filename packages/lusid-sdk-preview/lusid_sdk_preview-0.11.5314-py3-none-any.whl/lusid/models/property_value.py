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


class PropertyValue(object):
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
        'label_value': 'str',
        'metric_value': 'MetricValue',
        'label_value_set': 'LabelValueSet'
    }

    attribute_map = {
        'label_value': 'labelValue',
        'metric_value': 'metricValue',
        'label_value_set': 'labelValueSet'
    }

    required_map = {
        'label_value': 'optional',
        'metric_value': 'optional',
        'label_value_set': 'optional'
    }

    def __init__(self, label_value=None, metric_value=None, label_value_set=None, local_vars_configuration=None):  # noqa: E501
        """PropertyValue - a model defined in OpenAPI"
        
        :param label_value:  The text value of a property defined as having the 'Label' type.
        :type label_value: str
        :param metric_value: 
        :type metric_value: lusid.MetricValue
        :param label_value_set: 
        :type label_value_set: lusid.LabelValueSet

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._label_value = None
        self._metric_value = None
        self._label_value_set = None
        self.discriminator = None

        self.label_value = label_value
        if metric_value is not None:
            self.metric_value = metric_value
        if label_value_set is not None:
            self.label_value_set = label_value_set

    @property
    def label_value(self):
        """Gets the label_value of this PropertyValue.  # noqa: E501

        The text value of a property defined as having the 'Label' type.  # noqa: E501

        :return: The label_value of this PropertyValue.  # noqa: E501
        :rtype: str
        """
        return self._label_value

    @label_value.setter
    def label_value(self, label_value):
        """Sets the label_value of this PropertyValue.

        The text value of a property defined as having the 'Label' type.  # noqa: E501

        :param label_value: The label_value of this PropertyValue.  # noqa: E501
        :type label_value: str
        """

        self._label_value = label_value

    @property
    def metric_value(self):
        """Gets the metric_value of this PropertyValue.  # noqa: E501


        :return: The metric_value of this PropertyValue.  # noqa: E501
        :rtype: lusid.MetricValue
        """
        return self._metric_value

    @metric_value.setter
    def metric_value(self, metric_value):
        """Sets the metric_value of this PropertyValue.


        :param metric_value: The metric_value of this PropertyValue.  # noqa: E501
        :type metric_value: lusid.MetricValue
        """

        self._metric_value = metric_value

    @property
    def label_value_set(self):
        """Gets the label_value_set of this PropertyValue.  # noqa: E501


        :return: The label_value_set of this PropertyValue.  # noqa: E501
        :rtype: lusid.LabelValueSet
        """
        return self._label_value_set

    @label_value_set.setter
    def label_value_set(self, label_value_set):
        """Sets the label_value_set of this PropertyValue.


        :param label_value_set: The label_value_set of this PropertyValue.  # noqa: E501
        :type label_value_set: lusid.LabelValueSet
        """

        self._label_value_set = label_value_set

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
        if not isinstance(other, PropertyValue):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PropertyValue):
            return True

        return self.to_dict() != other.to_dict()
