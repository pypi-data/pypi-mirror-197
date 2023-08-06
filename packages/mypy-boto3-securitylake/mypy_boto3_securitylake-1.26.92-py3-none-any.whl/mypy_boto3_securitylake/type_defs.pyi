"""
Type annotations for securitylake service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/type_defs/)

Usage::

    ```python
    from mypy_boto3_securitylake.type_defs import LogsStatusTypeDef

    data: LogsStatusTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AccessTypeType,
    AwsLogSourceTypeType,
    DimensionType,
    EndpointProtocolType,
    HttpsMethodType,
    OcsfEventClassType,
    RegionType,
    SourceStatusType,
    StorageClassType,
    SubscriptionProtocolTypeType,
    SubscriptionStatusType,
    settingsStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "LogsStatusTypeDef",
    "AutoEnableNewRegionConfigurationTypeDef",
    "CreateAwsLogSourceRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateCustomLogSourceRequestRequestTypeDef",
    "CreateDatalakeDelegatedAdminRequestRequestTypeDef",
    "CreateDatalakeExceptionsSubscriptionRequestRequestTypeDef",
    "SourceTypeTypeDef",
    "CreateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    "DeleteAwsLogSourceRequestRequestTypeDef",
    "DeleteCustomLogSourceRequestRequestTypeDef",
    "DeleteDatalakeDelegatedAdminRequestRequestTypeDef",
    "DeleteSubscriberRequestRequestTypeDef",
    "DeleteSubscriptionNotificationConfigurationRequestRequestTypeDef",
    "FailuresTypeDef",
    "ProtocolAndNotificationEndpointTypeDef",
    "PaginatorConfigTypeDef",
    "GetDatalakeStatusRequestRequestTypeDef",
    "GetSubscriberRequestRequestTypeDef",
    "RetentionSettingTypeDef",
    "LastUpdateFailureTypeDef",
    "ListDatalakeExceptionsRequestRequestTypeDef",
    "ListLogSourcesRequestRequestTypeDef",
    "ListSubscribersRequestRequestTypeDef",
    "UpdateDatalakeExceptionsExpiryRequestRequestTypeDef",
    "UpdateDatalakeExceptionsSubscriptionRequestRequestTypeDef",
    "UpdateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    "AccountSourcesTypeDef",
    "CreateDatalakeAutoEnableRequestRequestTypeDef",
    "DeleteDatalakeAutoEnableRequestRequestTypeDef",
    "CreateAwsLogSourceResponseTypeDef",
    "CreateCustomLogSourceResponseTypeDef",
    "CreateSubscriberResponseTypeDef",
    "CreateSubscriptionNotificationConfigurationResponseTypeDef",
    "DeleteAwsLogSourceResponseTypeDef",
    "DeleteCustomLogSourceResponseTypeDef",
    "DeleteDatalakeExceptionsSubscriptionResponseTypeDef",
    "GetDatalakeAutoEnableResponseTypeDef",
    "GetDatalakeExceptionsExpiryResponseTypeDef",
    "ListLogSourcesResponseTypeDef",
    "UpdateSubscriptionNotificationConfigurationResponseTypeDef",
    "CreateSubscriberRequestRequestTypeDef",
    "SubscriberResourceTypeDef",
    "UpdateSubscriberRequestRequestTypeDef",
    "FailuresResponseTypeDef",
    "GetDatalakeExceptionsSubscriptionResponseTypeDef",
    "GetDatalakeStatusRequestGetDatalakeStatusPaginateTypeDef",
    "ListDatalakeExceptionsRequestListDatalakeExceptionsPaginateTypeDef",
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    "LakeConfigurationRequestTypeDef",
    "UpdateStatusTypeDef",
    "GetDatalakeStatusResponseTypeDef",
    "GetSubscriberResponseTypeDef",
    "ListSubscribersResponseTypeDef",
    "UpdateSubscriberResponseTypeDef",
    "ListDatalakeExceptionsResponseTypeDef",
    "CreateDatalakeRequestRequestTypeDef",
    "UpdateDatalakeRequestRequestTypeDef",
    "LakeConfigurationResponseTypeDef",
    "GetDatalakeResponseTypeDef",
)

LogsStatusTypeDef = TypedDict(
    "LogsStatusTypeDef",
    {
        "healthStatus": SourceStatusType,
        "pathToLogs": str,
    },
)

AutoEnableNewRegionConfigurationTypeDef = TypedDict(
    "AutoEnableNewRegionConfigurationTypeDef",
    {
        "region": RegionType,
        "sources": Sequence[AwsLogSourceTypeType],
    },
)

_RequiredCreateAwsLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAwsLogSourceRequestRequestTypeDef",
    {
        "inputOrder": Sequence[DimensionType],
    },
)
_OptionalCreateAwsLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAwsLogSourceRequestRequestTypeDef",
    {
        "enableAllDimensions": Mapping[str, Mapping[str, Sequence[str]]],
        "enableSingleDimension": Sequence[str],
        "enableTwoDimensions": Mapping[str, Sequence[str]],
    },
    total=False,
)

class CreateAwsLogSourceRequestRequestTypeDef(
    _RequiredCreateAwsLogSourceRequestRequestTypeDef,
    _OptionalCreateAwsLogSourceRequestRequestTypeDef,
):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

CreateCustomLogSourceRequestRequestTypeDef = TypedDict(
    "CreateCustomLogSourceRequestRequestTypeDef",
    {
        "customSourceName": str,
        "eventClass": OcsfEventClassType,
        "glueInvocationRoleArn": str,
        "logProviderAccountId": str,
    },
)

CreateDatalakeDelegatedAdminRequestRequestTypeDef = TypedDict(
    "CreateDatalakeDelegatedAdminRequestRequestTypeDef",
    {
        "account": str,
    },
)

CreateDatalakeExceptionsSubscriptionRequestRequestTypeDef = TypedDict(
    "CreateDatalakeExceptionsSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": SubscriptionProtocolTypeType,
    },
)

SourceTypeTypeDef = TypedDict(
    "SourceTypeTypeDef",
    {
        "awsSourceType": AwsLogSourceTypeType,
        "customSourceType": str,
    },
    total=False,
)

_RequiredCreateSubscriptionNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    {
        "subscriptionId": str,
    },
)
_OptionalCreateSubscriptionNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    {
        "createSqs": bool,
        "httpsApiKeyName": str,
        "httpsApiKeyValue": str,
        "httpsMethod": HttpsMethodType,
        "roleArn": str,
        "subscriptionEndpoint": str,
    },
    total=False,
)

class CreateSubscriptionNotificationConfigurationRequestRequestTypeDef(
    _RequiredCreateSubscriptionNotificationConfigurationRequestRequestTypeDef,
    _OptionalCreateSubscriptionNotificationConfigurationRequestRequestTypeDef,
):
    pass

_RequiredDeleteAwsLogSourceRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAwsLogSourceRequestRequestTypeDef",
    {
        "inputOrder": Sequence[DimensionType],
    },
)
_OptionalDeleteAwsLogSourceRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAwsLogSourceRequestRequestTypeDef",
    {
        "disableAllDimensions": Mapping[str, Mapping[str, Sequence[str]]],
        "disableSingleDimension": Sequence[str],
        "disableTwoDimensions": Mapping[str, Sequence[str]],
    },
    total=False,
)

class DeleteAwsLogSourceRequestRequestTypeDef(
    _RequiredDeleteAwsLogSourceRequestRequestTypeDef,
    _OptionalDeleteAwsLogSourceRequestRequestTypeDef,
):
    pass

DeleteCustomLogSourceRequestRequestTypeDef = TypedDict(
    "DeleteCustomLogSourceRequestRequestTypeDef",
    {
        "customSourceName": str,
    },
)

DeleteDatalakeDelegatedAdminRequestRequestTypeDef = TypedDict(
    "DeleteDatalakeDelegatedAdminRequestRequestTypeDef",
    {
        "account": str,
    },
)

DeleteSubscriberRequestRequestTypeDef = TypedDict(
    "DeleteSubscriberRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteSubscriptionNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteSubscriptionNotificationConfigurationRequestRequestTypeDef",
    {
        "subscriptionId": str,
    },
)

FailuresTypeDef = TypedDict(
    "FailuresTypeDef",
    {
        "exceptionMessage": str,
        "remediation": str,
        "timestamp": datetime,
    },
)

ProtocolAndNotificationEndpointTypeDef = TypedDict(
    "ProtocolAndNotificationEndpointTypeDef",
    {
        "endpoint": str,
        "protocol": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

GetDatalakeStatusRequestRequestTypeDef = TypedDict(
    "GetDatalakeStatusRequestRequestTypeDef",
    {
        "accountSet": Sequence[str],
        "maxAccountResults": int,
        "nextToken": str,
    },
    total=False,
)

GetSubscriberRequestRequestTypeDef = TypedDict(
    "GetSubscriberRequestRequestTypeDef",
    {
        "id": str,
    },
)

RetentionSettingTypeDef = TypedDict(
    "RetentionSettingTypeDef",
    {
        "retentionPeriod": int,
        "storageClass": StorageClassType,
    },
    total=False,
)

LastUpdateFailureTypeDef = TypedDict(
    "LastUpdateFailureTypeDef",
    {
        "code": str,
        "reason": str,
    },
    total=False,
)

ListDatalakeExceptionsRequestRequestTypeDef = TypedDict(
    "ListDatalakeExceptionsRequestRequestTypeDef",
    {
        "maxFailures": int,
        "nextToken": str,
        "regionSet": Sequence[RegionType],
    },
    total=False,
)

ListLogSourcesRequestRequestTypeDef = TypedDict(
    "ListLogSourcesRequestRequestTypeDef",
    {
        "inputOrder": Sequence[DimensionType],
        "listAllDimensions": Mapping[str, Mapping[str, Sequence[str]]],
        "listSingleDimension": Sequence[str],
        "listTwoDimensions": Mapping[str, Sequence[str]],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSubscribersRequestRequestTypeDef = TypedDict(
    "ListSubscribersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

UpdateDatalakeExceptionsExpiryRequestRequestTypeDef = TypedDict(
    "UpdateDatalakeExceptionsExpiryRequestRequestTypeDef",
    {
        "exceptionMessageExpiry": int,
    },
)

UpdateDatalakeExceptionsSubscriptionRequestRequestTypeDef = TypedDict(
    "UpdateDatalakeExceptionsSubscriptionRequestRequestTypeDef",
    {
        "notificationEndpoint": str,
        "subscriptionProtocol": SubscriptionProtocolTypeType,
    },
)

_RequiredUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    {
        "subscriptionId": str,
    },
)
_OptionalUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef",
    {
        "createSqs": bool,
        "httpsApiKeyName": str,
        "httpsApiKeyValue": str,
        "httpsMethod": HttpsMethodType,
        "roleArn": str,
        "subscriptionEndpoint": str,
    },
    total=False,
)

class UpdateSubscriptionNotificationConfigurationRequestRequestTypeDef(
    _RequiredUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef,
    _OptionalUpdateSubscriptionNotificationConfigurationRequestRequestTypeDef,
):
    pass

_RequiredAccountSourcesTypeDef = TypedDict(
    "_RequiredAccountSourcesTypeDef",
    {
        "account": str,
        "sourceType": str,
    },
)
_OptionalAccountSourcesTypeDef = TypedDict(
    "_OptionalAccountSourcesTypeDef",
    {
        "eventClass": OcsfEventClassType,
        "logsStatus": List[LogsStatusTypeDef],
    },
    total=False,
)

class AccountSourcesTypeDef(_RequiredAccountSourcesTypeDef, _OptionalAccountSourcesTypeDef):
    pass

CreateDatalakeAutoEnableRequestRequestTypeDef = TypedDict(
    "CreateDatalakeAutoEnableRequestRequestTypeDef",
    {
        "configurationForNewAccounts": Sequence[AutoEnableNewRegionConfigurationTypeDef],
    },
)

DeleteDatalakeAutoEnableRequestRequestTypeDef = TypedDict(
    "DeleteDatalakeAutoEnableRequestRequestTypeDef",
    {
        "removeFromConfigurationForNewAccounts": Sequence[AutoEnableNewRegionConfigurationTypeDef],
    },
)

CreateAwsLogSourceResponseTypeDef = TypedDict(
    "CreateAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "processing": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCustomLogSourceResponseTypeDef = TypedDict(
    "CreateCustomLogSourceResponseTypeDef",
    {
        "customDataLocation": str,
        "glueCrawlerName": str,
        "glueDatabaseName": str,
        "glueTableName": str,
        "logProviderAccessRoleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriberResponseTypeDef = TypedDict(
    "CreateSubscriberResponseTypeDef",
    {
        "resourceShareArn": str,
        "resourceShareName": str,
        "roleArn": str,
        "s3BucketArn": str,
        "snsArn": str,
        "subscriptionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSubscriptionNotificationConfigurationResponseTypeDef = TypedDict(
    "CreateSubscriptionNotificationConfigurationResponseTypeDef",
    {
        "queueArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAwsLogSourceResponseTypeDef = TypedDict(
    "DeleteAwsLogSourceResponseTypeDef",
    {
        "failed": List[str],
        "processing": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCustomLogSourceResponseTypeDef = TypedDict(
    "DeleteCustomLogSourceResponseTypeDef",
    {
        "customDataLocation": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDatalakeExceptionsSubscriptionResponseTypeDef = TypedDict(
    "DeleteDatalakeExceptionsSubscriptionResponseTypeDef",
    {
        "status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDatalakeAutoEnableResponseTypeDef = TypedDict(
    "GetDatalakeAutoEnableResponseTypeDef",
    {
        "autoEnableNewAccounts": List[AutoEnableNewRegionConfigurationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDatalakeExceptionsExpiryResponseTypeDef = TypedDict(
    "GetDatalakeExceptionsExpiryResponseTypeDef",
    {
        "exceptionMessageExpiry": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLogSourcesResponseTypeDef = TypedDict(
    "ListLogSourcesResponseTypeDef",
    {
        "nextToken": str,
        "regionSourceTypesAccountsList": List[Dict[str, Dict[str, List[str]]]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubscriptionNotificationConfigurationResponseTypeDef = TypedDict(
    "UpdateSubscriptionNotificationConfigurationResponseTypeDef",
    {
        "queueArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSubscriberRequestRequestTypeDef",
    {
        "accountId": str,
        "externalId": str,
        "sourceTypes": Sequence[SourceTypeTypeDef],
        "subscriberName": str,
    },
)
_OptionalCreateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSubscriberRequestRequestTypeDef",
    {
        "accessTypes": Sequence[AccessTypeType],
        "subscriberDescription": str,
    },
    total=False,
)

class CreateSubscriberRequestRequestTypeDef(
    _RequiredCreateSubscriberRequestRequestTypeDef, _OptionalCreateSubscriberRequestRequestTypeDef
):
    pass

_RequiredSubscriberResourceTypeDef = TypedDict(
    "_RequiredSubscriberResourceTypeDef",
    {
        "accountId": str,
        "sourceTypes": List[SourceTypeTypeDef],
        "subscriptionId": str,
    },
)
_OptionalSubscriberResourceTypeDef = TypedDict(
    "_OptionalSubscriberResourceTypeDef",
    {
        "accessTypes": List[AccessTypeType],
        "createdAt": datetime,
        "externalId": str,
        "resourceShareArn": str,
        "resourceShareName": str,
        "roleArn": str,
        "s3BucketArn": str,
        "snsArn": str,
        "subscriberDescription": str,
        "subscriberName": str,
        "subscriptionEndpoint": str,
        "subscriptionProtocol": EndpointProtocolType,
        "subscriptionStatus": SubscriptionStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

class SubscriberResourceTypeDef(
    _RequiredSubscriberResourceTypeDef, _OptionalSubscriberResourceTypeDef
):
    pass

_RequiredUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSubscriberRequestRequestTypeDef",
    {
        "id": str,
        "sourceTypes": Sequence[SourceTypeTypeDef],
    },
)
_OptionalUpdateSubscriberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSubscriberRequestRequestTypeDef",
    {
        "externalId": str,
        "subscriberDescription": str,
        "subscriberName": str,
    },
    total=False,
)

class UpdateSubscriberRequestRequestTypeDef(
    _RequiredUpdateSubscriberRequestRequestTypeDef, _OptionalUpdateSubscriberRequestRequestTypeDef
):
    pass

FailuresResponseTypeDef = TypedDict(
    "FailuresResponseTypeDef",
    {
        "failures": List[FailuresTypeDef],
        "region": str,
    },
    total=False,
)

GetDatalakeExceptionsSubscriptionResponseTypeDef = TypedDict(
    "GetDatalakeExceptionsSubscriptionResponseTypeDef",
    {
        "protocolAndNotificationEndpoint": ProtocolAndNotificationEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDatalakeStatusRequestGetDatalakeStatusPaginateTypeDef = TypedDict(
    "GetDatalakeStatusRequestGetDatalakeStatusPaginateTypeDef",
    {
        "accountSet": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDatalakeExceptionsRequestListDatalakeExceptionsPaginateTypeDef = TypedDict(
    "ListDatalakeExceptionsRequestListDatalakeExceptionsPaginateTypeDef",
    {
        "regionSet": Sequence[RegionType],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListLogSourcesRequestListLogSourcesPaginateTypeDef = TypedDict(
    "ListLogSourcesRequestListLogSourcesPaginateTypeDef",
    {
        "inputOrder": Sequence[DimensionType],
        "listAllDimensions": Mapping[str, Mapping[str, Sequence[str]]],
        "listSingleDimension": Sequence[str],
        "listTwoDimensions": Mapping[str, Sequence[str]],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSubscribersRequestListSubscribersPaginateTypeDef = TypedDict(
    "ListSubscribersRequestListSubscribersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

LakeConfigurationRequestTypeDef = TypedDict(
    "LakeConfigurationRequestTypeDef",
    {
        "encryptionKey": str,
        "replicationDestinationRegions": Sequence[RegionType],
        "replicationRoleArn": str,
        "retentionSettings": Sequence[RetentionSettingTypeDef],
        "tagsMap": Mapping[str, str],
    },
    total=False,
)

UpdateStatusTypeDef = TypedDict(
    "UpdateStatusTypeDef",
    {
        "lastUpdateFailure": LastUpdateFailureTypeDef,
        "lastUpdateRequestId": str,
        "lastUpdateStatus": settingsStatusType,
    },
    total=False,
)

GetDatalakeStatusResponseTypeDef = TypedDict(
    "GetDatalakeStatusResponseTypeDef",
    {
        "accountSourcesList": List[AccountSourcesTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSubscriberResponseTypeDef = TypedDict(
    "GetSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSubscribersResponseTypeDef = TypedDict(
    "ListSubscribersResponseTypeDef",
    {
        "nextToken": str,
        "subscribers": List[SubscriberResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSubscriberResponseTypeDef = TypedDict(
    "UpdateSubscriberResponseTypeDef",
    {
        "subscriber": SubscriberResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatalakeExceptionsResponseTypeDef = TypedDict(
    "ListDatalakeExceptionsResponseTypeDef",
    {
        "nextToken": str,
        "nonRetryableFailures": List[FailuresResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDatalakeRequestRequestTypeDef = TypedDict(
    "CreateDatalakeRequestRequestTypeDef",
    {
        "configurations": Mapping[RegionType, LakeConfigurationRequestTypeDef],
        "enableAll": bool,
        "metaStoreManagerRoleArn": str,
        "regions": Sequence[RegionType],
    },
    total=False,
)

UpdateDatalakeRequestRequestTypeDef = TypedDict(
    "UpdateDatalakeRequestRequestTypeDef",
    {
        "configurations": Mapping[RegionType, LakeConfigurationRequestTypeDef],
    },
)

LakeConfigurationResponseTypeDef = TypedDict(
    "LakeConfigurationResponseTypeDef",
    {
        "encryptionKey": str,
        "replicationDestinationRegions": List[RegionType],
        "replicationRoleArn": str,
        "retentionSettings": List[RetentionSettingTypeDef],
        "s3BucketArn": str,
        "status": settingsStatusType,
        "tagsMap": Dict[str, str],
        "updateStatus": UpdateStatusTypeDef,
    },
    total=False,
)

GetDatalakeResponseTypeDef = TypedDict(
    "GetDatalakeResponseTypeDef",
    {
        "configurations": Dict[RegionType, LakeConfigurationResponseTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
