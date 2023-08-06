"""
Type annotations for securitylake service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_securitylake.client import SecurityLakeClient
    from mypy_boto3_securitylake.paginator import (
        GetDatalakeStatusPaginator,
        ListDatalakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
    )

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")

    get_datalake_status_paginator: GetDatalakeStatusPaginator = client.get_paginator("get_datalake_status")
    list_datalake_exceptions_paginator: ListDatalakeExceptionsPaginator = client.get_paginator("list_datalake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import DimensionType, RegionType
from .type_defs import (
    GetDatalakeStatusResponseTypeDef,
    ListDatalakeExceptionsResponseTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetDatalakeStatusPaginator",
    "ListDatalakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetDatalakeStatusPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.GetDatalakeStatus)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#getdatalakestatuspaginator)
    """

    def paginate(
        self, *, accountSet: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetDatalakeStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.GetDatalakeStatus.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#getdatalakestatuspaginator)
        """


class ListDatalakeExceptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListDatalakeExceptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listdatalakeexceptionspaginator)
    """

    def paginate(
        self,
        *,
        regionSet: Sequence[RegionType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDatalakeExceptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListDatalakeExceptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listdatalakeexceptionspaginator)
        """


class ListLogSourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListLogSources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listlogsourcespaginator)
    """

    def paginate(
        self,
        *,
        inputOrder: Sequence[DimensionType] = ...,
        listAllDimensions: Mapping[str, Mapping[str, Sequence[str]]] = ...,
        listSingleDimension: Sequence[str] = ...,
        listTwoDimensions: Mapping[str, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLogSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListLogSources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listlogsourcespaginator)
        """


class ListSubscribersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListSubscribers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listsubscriberspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListSubscribers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/paginators/#listsubscriberspaginator)
        """
