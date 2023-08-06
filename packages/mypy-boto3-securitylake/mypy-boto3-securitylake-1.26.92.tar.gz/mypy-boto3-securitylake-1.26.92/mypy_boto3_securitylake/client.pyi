"""
Type annotations for securitylake service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securitylake.client import SecurityLakeClient

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    AccessTypeType,
    DimensionType,
    HttpsMethodType,
    OcsfEventClassType,
    RegionType,
    SubscriptionProtocolTypeType,
)
from .paginator import (
    GetDatalakeStatusPaginator,
    ListDatalakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)
from .type_defs import (
    AutoEnableNewRegionConfigurationTypeDef,
    CreateAwsLogSourceResponseTypeDef,
    CreateCustomLogSourceResponseTypeDef,
    CreateSubscriberResponseTypeDef,
    CreateSubscriptionNotificationConfigurationResponseTypeDef,
    DeleteAwsLogSourceResponseTypeDef,
    DeleteCustomLogSourceResponseTypeDef,
    DeleteDatalakeExceptionsSubscriptionResponseTypeDef,
    GetDatalakeAutoEnableResponseTypeDef,
    GetDatalakeExceptionsExpiryResponseTypeDef,
    GetDatalakeExceptionsSubscriptionResponseTypeDef,
    GetDatalakeResponseTypeDef,
    GetDatalakeStatusResponseTypeDef,
    GetSubscriberResponseTypeDef,
    LakeConfigurationRequestTypeDef,
    ListDatalakeExceptionsResponseTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersResponseTypeDef,
    SourceTypeTypeDef,
    UpdateSubscriberResponseTypeDef,
    UpdateSubscriptionNotificationConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SecurityLakeClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AccountNotFoundException: Type[BotocoreClientError]
    BucketNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConflictSourceNamesException: Type[BotocoreClientError]
    ConflictSubscriptionException: Type[BotocoreClientError]
    EventBridgeException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    S3Exception: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SecurityLakeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#can_paginate)
        """
    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#close)
        """
    def create_aws_log_source(
        self,
        *,
        inputOrder: Sequence[DimensionType],
        enableAllDimensions: Mapping[str, Mapping[str, Sequence[str]]] = ...,
        enableSingleDimension: Sequence[str] = ...,
        enableTwoDimensions: Mapping[str, Sequence[str]] = ...
    ) -> CreateAwsLogSourceResponseTypeDef:
        """
        Adds a natively supported Amazon Web Service as an Amazon Security Lake source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_aws_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_aws_log_source)
        """
    def create_custom_log_source(
        self,
        *,
        customSourceName: str,
        eventClass: OcsfEventClassType,
        glueInvocationRoleArn: str,
        logProviderAccountId: str
    ) -> CreateCustomLogSourceResponseTypeDef:
        """
        Adds a third-party custom source in Amazon Security Lake, from the Amazon Web
        Services Region where you want to create a custom source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_custom_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_custom_log_source)
        """
    def create_datalake(
        self,
        *,
        configurations: Mapping[RegionType, LakeConfigurationRequestTypeDef] = ...,
        enableAll: bool = ...,
        metaStoreManagerRoleArn: str = ...,
        regions: Sequence[RegionType] = ...
    ) -> Dict[str, Any]:
        """
        Initializes an Amazon Security Lake instance with the provided (or default)
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_datalake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_datalake)
        """
    def create_datalake_auto_enable(
        self, *, configurationForNewAccounts: Sequence[AutoEnableNewRegionConfigurationTypeDef]
    ) -> Dict[str, Any]:
        """
        Automatically enables Amazon Security Lake for new member accounts in your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_datalake_auto_enable)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_datalake_auto_enable)
        """
    def create_datalake_delegated_admin(self, *, account: str) -> Dict[str, Any]:
        """
        Designates the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_datalake_delegated_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_datalake_delegated_admin)
        """
    def create_datalake_exceptions_subscription(
        self, *, notificationEndpoint: str, subscriptionProtocol: SubscriptionProtocolTypeType
    ) -> Dict[str, Any]:
        """
        Creates the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_datalake_exceptions_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_datalake_exceptions_subscription)
        """
    def create_subscriber(
        self,
        *,
        accountId: str,
        externalId: str,
        sourceTypes: Sequence[SourceTypeTypeDef],
        subscriberName: str,
        accessTypes: Sequence[AccessTypeType] = ...,
        subscriberDescription: str = ...
    ) -> CreateSubscriberResponseTypeDef:
        """
        Creates a subscription permission for accounts that are already enabled in
        Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_subscriber)
        """
    def create_subscription_notification_configuration(
        self,
        *,
        subscriptionId: str,
        createSqs: bool = ...,
        httpsApiKeyName: str = ...,
        httpsApiKeyValue: str = ...,
        httpsMethod: HttpsMethodType = ...,
        roleArn: str = ...,
        subscriptionEndpoint: str = ...
    ) -> CreateSubscriptionNotificationConfigurationResponseTypeDef:
        """
        Notifies the subscriber when new data is written to the data lake for the
        sources that the subscriber consumes in Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_subscription_notification_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_subscription_notification_configuration)
        """
    def delete_aws_log_source(
        self,
        *,
        inputOrder: Sequence[DimensionType],
        disableAllDimensions: Mapping[str, Mapping[str, Sequence[str]]] = ...,
        disableSingleDimension: Sequence[str] = ...,
        disableTwoDimensions: Mapping[str, Sequence[str]] = ...
    ) -> DeleteAwsLogSourceResponseTypeDef:
        """
        Removes a natively supported Amazon Web Service as an Amazon Security Lake
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_aws_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_aws_log_source)
        """
    def delete_custom_log_source(
        self, *, customSourceName: str
    ) -> DeleteCustomLogSourceResponseTypeDef:
        """
        Removes a custom log source from Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_custom_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_custom_log_source)
        """
    def delete_datalake(self) -> Dict[str, Any]:
        """
        When you delete Amazon Security Lake from your account, Security Lake is
        disabled in all Amazon Web Services Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_datalake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_datalake)
        """
    def delete_datalake_auto_enable(
        self,
        *,
        removeFromConfigurationForNewAccounts: Sequence[AutoEnableNewRegionConfigurationTypeDef]
    ) -> Dict[str, Any]:
        """
        `DeleteDatalakeAutoEnable` removes automatic enablement of configuration
        settings for new member accounts (but keeps settings for the delegated
        administrator) from Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_datalake_auto_enable)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_datalake_auto_enable)
        """
    def delete_datalake_delegated_admin(self, *, account: str) -> Dict[str, Any]:
        """
        Deletes the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_datalake_delegated_admin)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_datalake_delegated_admin)
        """
    def delete_datalake_exceptions_subscription(
        self,
    ) -> DeleteDatalakeExceptionsSubscriptionResponseTypeDef:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_datalake_exceptions_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_datalake_exceptions_subscription)
        """
    def delete_subscriber(self, *, id: str) -> Dict[str, Any]:
        """
        Deletes the subscription permission for accounts that are already enabled in
        Amazon Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_subscriber)
        """
    def delete_subscription_notification_configuration(
        self, *, subscriptionId: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_subscription_notification_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_subscription_notification_configuration)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#generate_presigned_url)
        """
    def get_datalake(self) -> GetDatalakeResponseTypeDef:
        """
        Retrieves the Amazon Security Lake configuration object for the specified Amazon
        Web Services account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_datalake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_datalake)
        """
    def get_datalake_auto_enable(self) -> GetDatalakeAutoEnableResponseTypeDef:
        """
        Retrieves the configuration that will be automatically set up for accounts added
        to the organization after the organization has onboarded to Amazon Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_datalake_auto_enable)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_datalake_auto_enable)
        """
    def get_datalake_exceptions_expiry(self) -> GetDatalakeExceptionsExpiryResponseTypeDef:
        """
        Retrieves the expiration period and time-to-live (TTL) for which the exception
        message will remain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_datalake_exceptions_expiry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_datalake_exceptions_expiry)
        """
    def get_datalake_exceptions_subscription(
        self,
    ) -> GetDatalakeExceptionsSubscriptionResponseTypeDef:
        """
        Retrieves the details of exception notifications for the account in Amazon
        Security Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_datalake_exceptions_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_datalake_exceptions_subscription)
        """
    def get_datalake_status(
        self, *, accountSet: Sequence[str] = ..., maxAccountResults: int = ..., nextToken: str = ...
    ) -> GetDatalakeStatusResponseTypeDef:
        """
        Retrieves a snapshot of the current Region, including whether Amazon Security
        Lake is enabled for those accounts and which sources Security Lake is collecting
        data from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_datalake_status)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_datalake_status)
        """
    def get_subscriber(self, *, id: str) -> GetSubscriberResponseTypeDef:
        """
        Retrieves the subscription information for the specified subscription ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_subscriber)
        """
    def list_datalake_exceptions(
        self, *, maxFailures: int = ..., nextToken: str = ..., regionSet: Sequence[RegionType] = ...
    ) -> ListDatalakeExceptionsResponseTypeDef:
        """
        Lists the Amazon Security Lake exceptions that you can use to find the source of
        problems and fix them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_datalake_exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_datalake_exceptions)
        """
    def list_log_sources(
        self,
        *,
        inputOrder: Sequence[DimensionType] = ...,
        listAllDimensions: Mapping[str, Mapping[str, Sequence[str]]] = ...,
        listSingleDimension: Sequence[str] = ...,
        listTwoDimensions: Mapping[str, Sequence[str]] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListLogSourcesResponseTypeDef:
        """
        Retrieves the log sources in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_log_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_log_sources)
        """
    def list_subscribers(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSubscribersResponseTypeDef:
        """
        List all subscribers for the specific Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_subscribers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_subscribers)
        """
    def update_datalake(
        self, *, configurations: Mapping[RegionType, LakeConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Specifies where to store your security data and for how long.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_datalake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_datalake)
        """
    def update_datalake_exceptions_expiry(self, *, exceptionMessageExpiry: int) -> Dict[str, Any]:
        """
        Update the expiration period for the exception message to your preferred time,
        and control the time-to-live (TTL) for the exception message to remain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_datalake_exceptions_expiry)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_datalake_exceptions_expiry)
        """
    def update_datalake_exceptions_subscription(
        self, *, notificationEndpoint: str, subscriptionProtocol: SubscriptionProtocolTypeType
    ) -> Dict[str, Any]:
        """
        Updates the specified notification subscription in Amazon Security Lake for the
        organization you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_datalake_exceptions_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_datalake_exceptions_subscription)
        """
    def update_subscriber(
        self,
        *,
        id: str,
        sourceTypes: Sequence[SourceTypeTypeDef],
        externalId: str = ...,
        subscriberDescription: str = ...,
        subscriberName: str = ...
    ) -> UpdateSubscriberResponseTypeDef:
        """
        Updates an existing subscription for the given Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_subscriber)
        """
    def update_subscription_notification_configuration(
        self,
        *,
        subscriptionId: str,
        createSqs: bool = ...,
        httpsApiKeyName: str = ...,
        httpsApiKeyValue: str = ...,
        httpsMethod: HttpsMethodType = ...,
        roleArn: str = ...,
        subscriptionEndpoint: str = ...
    ) -> UpdateSubscriptionNotificationConfigurationResponseTypeDef:
        """
        Updates an existing notification method for the subscription (SQS or HTTPs
        endpoint) or switches the notification subscription endpoint for a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_subscription_notification_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_subscription_notification_configuration)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_datalake_status"]
    ) -> GetDatalakeStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_datalake_exceptions"]
    ) -> ListDatalakeExceptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_log_sources"]) -> ListLogSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscribers"]
    ) -> ListSubscribersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """
