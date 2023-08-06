"""
Main interface for securitylake service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securitylake import (
        Client,
        GetDatalakeStatusPaginator,
        ListDatalakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
        SecurityLakeClient,
    )

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")

    get_datalake_status_paginator: GetDatalakeStatusPaginator = client.get_paginator("get_datalake_status")
    list_datalake_exceptions_paginator: ListDatalakeExceptionsPaginator = client.get_paginator("list_datalake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""
from .client import SecurityLakeClient
from .paginator import (
    GetDatalakeStatusPaginator,
    ListDatalakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)

Client = SecurityLakeClient


__all__ = (
    "Client",
    "GetDatalakeStatusPaginator",
    "ListDatalakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
    "SecurityLakeClient",
)
