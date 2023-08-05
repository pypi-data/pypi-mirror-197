# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5314
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from lusid.api_client import ApiClient
from lusid.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)
from lusid.models.allocation import Allocation
from lusid.models.allocation_set_request import AllocationSetRequest
from lusid.models.deleted_entity_response import DeletedEntityResponse
from lusid.models.lusid_problem_details import LusidProblemDetails
from lusid.models.lusid_validation_problem_details import LusidValidationProblemDetails
from lusid.models.paged_resource_list_of_allocation import PagedResourceListOfAllocation
from lusid.models.resource_list_of_allocation import ResourceListOfAllocation


class AllocationsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_allocation(self, scope, code, **kwargs):  # noqa: E501
        """[EARLY ACCESS] DeleteAllocation: Delete allocation  # noqa: E501

        Delete an allocation. Deletion will be valid from the allocation's creation datetime.  This means that the allocation will no longer exist at any effective datetime from the asAt datetime of deletion.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_allocation(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The allocation scope. (required)
        :type scope: str
        :param code: The allocation's code. This, together with the scope uniquely identifies the allocation to delete. (required)
        :type code: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DeletedEntityResponse
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_allocation_with_http_info(scope, code, **kwargs)  # noqa: E501

    def delete_allocation_with_http_info(self, scope, code, **kwargs):  # noqa: E501
        """[EARLY ACCESS] DeleteAllocation: Delete allocation  # noqa: E501

        Delete an allocation. Deletion will be valid from the allocation's creation datetime.  This means that the allocation will no longer exist at any effective datetime from the asAt datetime of deletion.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_allocation_with_http_info(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The allocation scope. (required)
        :type scope: str
        :param code: The allocation's code. This, together with the scope uniquely identifies the allocation to delete. (required)
        :type code: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (DeletedEntityResponse, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'scope',
            'code'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_allocation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'scope' is set
        if self.api_client.client_side_validation and ('scope' not in local_var_params or  # noqa: E501
                                                        local_var_params['scope'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `scope` when calling `delete_allocation`")  # noqa: E501
        # verify the required parameter 'code' is set
        if self.api_client.client_side_validation and ('code' not in local_var_params or  # noqa: E501
                                                        local_var_params['code'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `code` when calling `delete_allocation`")  # noqa: E501

        if self.api_client.client_side_validation and ('scope' in local_var_params and  # noqa: E501
                                                        len(local_var_params['scope']) > 64):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `delete_allocation`, length must be less than or equal to `64`")  # noqa: E501
        if self.api_client.client_side_validation and ('scope' in local_var_params and  # noqa: E501
                                                        len(local_var_params['scope']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `delete_allocation`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'scope' in local_var_params and not re.search(r'^[a-zA-Z0-9\-_]+$', local_var_params['scope']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `delete_allocation`, must conform to the pattern `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('code' in local_var_params and  # noqa: E501
                                                        len(local_var_params['code']) > 64):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `code` when calling `delete_allocation`, length must be less than or equal to `64`")  # noqa: E501
        if self.api_client.client_side_validation and ('code' in local_var_params and  # noqa: E501
                                                        len(local_var_params['code']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `code` when calling `delete_allocation`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'scope' in local_var_params:
            path_params['scope'] = local_var_params['scope']  # noqa: E501
        if 'code' in local_var_params:
            path_params['code'] = local_var_params['code']  # noqa: E501

        query_params = []

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"


        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '0.11.5314'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "DeletedEntityResponse",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/allocations/{scope}/{code}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def get_allocation(self, scope, code, **kwargs):  # noqa: E501
        """[EARLY ACCESS] GetAllocation: Get Allocation  # noqa: E501

        Fetch an Allocation matching the provided identifier  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_allocation(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the allocation belongs. (required)
        :type scope: str
        :param code: The allocation's unique identifier. (required)
        :type code: str
        :param as_at: The asAt datetime at which to retrieve the allocation. Defaults to return the latest version of the allocation if not specified.
        :type as_at: datetime
        :param property_keys: A list of property keys from the \"Allocations\" domain to decorate onto the allocation.              These take the format {domain}/{scope}/{code} e.g. \"Allocations/system/Name\".
        :type property_keys: list[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Allocation
        """
        kwargs['_return_http_data_only'] = True
        return self.get_allocation_with_http_info(scope, code, **kwargs)  # noqa: E501

    def get_allocation_with_http_info(self, scope, code, **kwargs):  # noqa: E501
        """[EARLY ACCESS] GetAllocation: Get Allocation  # noqa: E501

        Fetch an Allocation matching the provided identifier  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_allocation_with_http_info(scope, code, async_req=True)
        >>> result = thread.get()

        :param scope: The scope to which the allocation belongs. (required)
        :type scope: str
        :param code: The allocation's unique identifier. (required)
        :type code: str
        :param as_at: The asAt datetime at which to retrieve the allocation. Defaults to return the latest version of the allocation if not specified.
        :type as_at: datetime
        :param property_keys: A list of property keys from the \"Allocations\" domain to decorate onto the allocation.              These take the format {domain}/{scope}/{code} e.g. \"Allocations/system/Name\".
        :type property_keys: list[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (Allocation, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'scope',
            'code',
            'as_at',
            'property_keys'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_allocation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'scope' is set
        if self.api_client.client_side_validation and ('scope' not in local_var_params or  # noqa: E501
                                                        local_var_params['scope'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `scope` when calling `get_allocation`")  # noqa: E501
        # verify the required parameter 'code' is set
        if self.api_client.client_side_validation and ('code' not in local_var_params or  # noqa: E501
                                                        local_var_params['code'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `code` when calling `get_allocation`")  # noqa: E501

        if self.api_client.client_side_validation and ('scope' in local_var_params and  # noqa: E501
                                                        len(local_var_params['scope']) > 64):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `get_allocation`, length must be less than or equal to `64`")  # noqa: E501
        if self.api_client.client_side_validation and ('scope' in local_var_params and  # noqa: E501
                                                        len(local_var_params['scope']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `get_allocation`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'scope' in local_var_params and not re.search(r'^[a-zA-Z0-9\-_]+$', local_var_params['scope']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `scope` when calling `get_allocation`, must conform to the pattern `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('code' in local_var_params and  # noqa: E501
                                                        len(local_var_params['code']) > 64):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `code` when calling `get_allocation`, length must be less than or equal to `64`")  # noqa: E501
        if self.api_client.client_side_validation and ('code' in local_var_params and  # noqa: E501
                                                        len(local_var_params['code']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `code` when calling `get_allocation`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'scope' in local_var_params:
            path_params['scope'] = local_var_params['scope']  # noqa: E501
        if 'code' in local_var_params:
            path_params['code'] = local_var_params['code']  # noqa: E501

        query_params = []
        if 'as_at' in local_var_params and local_var_params['as_at'] is not None:  # noqa: E501
            query_params.append(('asAt', local_var_params['as_at']))  # noqa: E501
        if 'property_keys' in local_var_params and local_var_params['property_keys'] is not None:  # noqa: E501
            query_params.append(('propertyKeys', local_var_params['property_keys']))  # noqa: E501
            collection_formats['propertyKeys'] = 'multi'  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"


        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '0.11.5314'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "Allocation",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/allocations/{scope}/{code}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def list_allocations(self, **kwargs):  # noqa: E501
        """[EARLY ACCESS] ListAllocations: List Allocations  # noqa: E501

        Fetch the last pre-AsAt date version of each allocation in scope (does not fetch the entire history).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_allocations(async_req=True)
        >>> result = thread.get()

        :param as_at: The asAt datetime at which to retrieve the allocation. Defaults to return the latest version of the allocation if not specified.
        :type as_at: datetime
        :param page: The pagination token to use to continue listing allocations from a previous call to list allocations.              This value is returned from the previous call. If a pagination token is provided the sortBy, filter, effectiveAt, and asAt fields              must not have changed since the original request. Also, if set, a start value cannot be provided.
        :type page: str
        :param sort_by: Allocation the results by these fields. Use use the '-' sign to denote descending allocation e.g. -MyFieldName.
        :type sort_by: list[str]
        :param start: When paginating, skip this number of results.
        :type start: int
        :param limit: When paginating, limit the number of returned results to this many.
        :type limit: int
        :param filter: Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.
        :type filter: str
        :param property_keys: A list of property keys from the \"Allocations\" domain to decorate onto each allocation.                  These take the format {domain}/{scope}/{code} e.g. \"Allocations/system/Name\".
        :type property_keys: list[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PagedResourceListOfAllocation
        """
        kwargs['_return_http_data_only'] = True
        return self.list_allocations_with_http_info(**kwargs)  # noqa: E501

    def list_allocations_with_http_info(self, **kwargs):  # noqa: E501
        """[EARLY ACCESS] ListAllocations: List Allocations  # noqa: E501

        Fetch the last pre-AsAt date version of each allocation in scope (does not fetch the entire history).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.list_allocations_with_http_info(async_req=True)
        >>> result = thread.get()

        :param as_at: The asAt datetime at which to retrieve the allocation. Defaults to return the latest version of the allocation if not specified.
        :type as_at: datetime
        :param page: The pagination token to use to continue listing allocations from a previous call to list allocations.              This value is returned from the previous call. If a pagination token is provided the sortBy, filter, effectiveAt, and asAt fields              must not have changed since the original request. Also, if set, a start value cannot be provided.
        :type page: str
        :param sort_by: Allocation the results by these fields. Use use the '-' sign to denote descending allocation e.g. -MyFieldName.
        :type sort_by: list[str]
        :param start: When paginating, skip this number of results.
        :type start: int
        :param limit: When paginating, limit the number of returned results to this many.
        :type limit: int
        :param filter: Expression to filter the result set. Read more about filtering results from LUSID here:              https://support.lusid.com/filtering-results-from-lusid.
        :type filter: str
        :param property_keys: A list of property keys from the \"Allocations\" domain to decorate onto each allocation.                  These take the format {domain}/{scope}/{code} e.g. \"Allocations/system/Name\".
        :type property_keys: list[str]
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (PagedResourceListOfAllocation, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'as_at',
            'page',
            'sort_by',
            'start',
            'limit',
            'filter',
            'property_keys'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_allocations" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and ('page' in local_var_params and  # noqa: E501
                                                        len(local_var_params['page']) > 500):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `page` when calling `list_allocations`, length must be less than or equal to `500`")  # noqa: E501
        if self.api_client.client_side_validation and ('page' in local_var_params and  # noqa: E501
                                                        len(local_var_params['page']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `page` when calling `list_allocations`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'page' in local_var_params and not re.search(r'^[a-zA-Z0-9\+\/]*={0,3}$', local_var_params['page']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `page` when calling `list_allocations`, must conform to the pattern `/^[a-zA-Z0-9\+\/]*={0,3}$/`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 5000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_allocations`, must be a value less than or equal to `5000`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `list_allocations`, must be a value greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and ('filter' in local_var_params and  # noqa: E501
                                                        len(local_var_params['filter']) > 16384):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `filter` when calling `list_allocations`, length must be less than or equal to `16384`")  # noqa: E501
        if self.api_client.client_side_validation and ('filter' in local_var_params and  # noqa: E501
                                                        len(local_var_params['filter']) < 0):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `filter` when calling `list_allocations`, length must be greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'filter' in local_var_params and not re.search(r'^[\s\S]*$', local_var_params['filter']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `filter` when calling `list_allocations`, must conform to the pattern `/^[\s\S]*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'as_at' in local_var_params and local_var_params['as_at'] is not None:  # noqa: E501
            query_params.append(('asAt', local_var_params['as_at']))  # noqa: E501
        if 'page' in local_var_params and local_var_params['page'] is not None:  # noqa: E501
            query_params.append(('page', local_var_params['page']))  # noqa: E501
        if 'sort_by' in local_var_params and local_var_params['sort_by'] is not None:  # noqa: E501
            query_params.append(('sortBy', local_var_params['sort_by']))  # noqa: E501
            collection_formats['sortBy'] = 'multi'  # noqa: E501
        if 'start' in local_var_params and local_var_params['start'] is not None:  # noqa: E501
            query_params.append(('start', local_var_params['start']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'filter' in local_var_params and local_var_params['filter'] is not None:  # noqa: E501
            query_params.append(('filter', local_var_params['filter']))  # noqa: E501
        if 'property_keys' in local_var_params and local_var_params['property_keys'] is not None:  # noqa: E501
            query_params.append(('propertyKeys', local_var_params['property_keys']))  # noqa: E501
            collection_formats['propertyKeys'] = 'multi'  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"


        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '0.11.5314'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "PagedResourceListOfAllocation",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/allocations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def upsert_allocations(self, **kwargs):  # noqa: E501
        """[EARLY ACCESS] UpsertAllocations: Upsert Allocations  # noqa: E501

        Upsert; update existing allocations with given ids, or create new allocations otherwise.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upsert_allocations(async_req=True)
        >>> result = thread.get()

        :param allocation_set_request: The collection of allocation requests.
        :type allocation_set_request: AllocationSetRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ResourceListOfAllocation
        """
        kwargs['_return_http_data_only'] = True
        return self.upsert_allocations_with_http_info(**kwargs)  # noqa: E501

    def upsert_allocations_with_http_info(self, **kwargs):  # noqa: E501
        """[EARLY ACCESS] UpsertAllocations: Upsert Allocations  # noqa: E501

        Upsert; update existing allocations with given ids, or create new allocations otherwise.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.upsert_allocations_with_http_info(async_req=True)
        >>> result = thread.get()

        :param allocation_set_request: The collection of allocation requests.
        :type allocation_set_request: AllocationSetRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object, the HTTP status code, and the headers.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: (ResourceListOfAllocation, int, HTTPHeaderDict)
        """

        local_var_params = locals()

        all_params = [
            'allocation_set_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method upsert_allocations" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        if 'allocation_set_request' in local_var_params:
            body_params = local_var_params['allocation_set_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        header_params['Accept-Encoding'] = "gzip, deflate, br"

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # set the LUSID header
        header_params['X-LUSID-SDK-Language'] = 'Python'
        header_params['X-LUSID-SDK-Version'] = '0.11.5314'

        # Authentication setting
        auth_settings = ['oauth2']  # noqa: E501

        response_types_map = {
            200: "ResourceListOfAllocation",
            400: "LusidValidationProblemDetails",
        }

        return self.api_client.call_api(
            '/api/allocations', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
