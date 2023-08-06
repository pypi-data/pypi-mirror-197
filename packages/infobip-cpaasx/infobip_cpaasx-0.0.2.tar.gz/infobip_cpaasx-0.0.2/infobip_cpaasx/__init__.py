# coding: utf-8

# flake8: noqa

"""
    This class is auto generated from the Infobip OpenAPI specification
    through the OpenAPI Specification Client API libraries (Re)Generator (OSCAR),
    powered by the OpenAPI Generator (https://openapi-generator.tech).
"""


from __future__ import absolute_import

__version__ = "0.0.2"

# import apis into sdk package
from infobip_cpaasx.api.application_api import ApplicationApi
from infobip_cpaasx.api.entity_api import EntityApi
from infobip_cpaasx.api.mms_api import MmsApi
from infobip_cpaasx.api.number_registration_api import NumberRegistrationApi
from infobip_cpaasx.api.numbers_api import NumbersApi
from infobip_cpaasx.api.resource_association_api import ResourceAssociationApi
from infobip_cpaasx.api.sms_api import SmsApi

# import ApiClient
from infobip_cpaasx.api_client import ApiClient
from infobip_cpaasx.configuration import Configuration
from infobip_cpaasx.exceptions import OpenApiException
from infobip_cpaasx.exceptions import ApiTypeError
from infobip_cpaasx.exceptions import ApiValueError
from infobip_cpaasx.exceptions import ApiKeyError
from infobip_cpaasx.exceptions import ApiAttributeError
from infobip_cpaasx.exceptions import ApiException

# import models into sdk package
from infobip_cpaasx.models.application import Application
from infobip_cpaasx.models.channel import Channel
from infobip_cpaasx.models.entity import Entity
from infobip_cpaasx.models.message_error import MessageError
from infobip_cpaasx.models.message_price import MessagePrice
from infobip_cpaasx.models.message_status import MessageStatus
from infobip_cpaasx.models.mms_advanced_message import MmsAdvancedMessage
from infobip_cpaasx.models.mms_advanced_message_segment import MmsAdvancedMessageSegment
from infobip_cpaasx.models.mms_advanced_message_segment_binary import (
    MmsAdvancedMessageSegmentBinary,
)
from infobip_cpaasx.models.mms_advanced_message_segment_link import (
    MmsAdvancedMessageSegmentLink,
)
from infobip_cpaasx.models.mms_advanced_message_segment_smil import (
    MmsAdvancedMessageSegmentSmil,
)
from infobip_cpaasx.models.mms_advanced_message_segment_text import (
    MmsAdvancedMessageSegmentText,
)
from infobip_cpaasx.models.mms_advanced_message_segment_upload_reference import (
    MmsAdvancedMessageSegmentUploadReference,
)
from infobip_cpaasx.models.mms_advanced_request import MmsAdvancedRequest
from infobip_cpaasx.models.mms_delivery_day import MmsDeliveryDay
from infobip_cpaasx.models.mms_delivery_time import MmsDeliveryTime
from infobip_cpaasx.models.mms_delivery_time_window import MmsDeliveryTimeWindow
from infobip_cpaasx.models.mms_destination import MmsDestination
from infobip_cpaasx.models.mms_error import MmsError
from infobip_cpaasx.models.mms_inbound_report import MmsInboundReport
from infobip_cpaasx.models.mms_inbound_report_response import MmsInboundReportResponse
from infobip_cpaasx.models.mms_message_result import MmsMessageResult
from infobip_cpaasx.models.mms_price import MmsPrice
from infobip_cpaasx.models.mms_report import MmsReport
from infobip_cpaasx.models.mms_report_response import MmsReportResponse
from infobip_cpaasx.models.mms_send_result import MmsSendResult
from infobip_cpaasx.models.mms_status import MmsStatus
from infobip_cpaasx.models.mms_upload_binary_result import MmsUploadBinaryResult
from infobip_cpaasx.models.mms_webhook_inbound_message_segment import (
    MmsWebhookInboundMessageSegment,
)
from infobip_cpaasx.models.mms_webhook_inbound_message_segment_link import (
    MmsWebhookInboundMessageSegmentLink,
)
from infobip_cpaasx.models.mms_webhook_inbound_message_segment_text import (
    MmsWebhookInboundMessageSegmentText,
)
from infobip_cpaasx.models.mms_webhook_inbound_report import MmsWebhookInboundReport
from infobip_cpaasx.models.mms_webhook_inbound_report_response import (
    MmsWebhookInboundReportResponse,
)
from infobip_cpaasx.models.mms_webhook_outbound_report import MmsWebhookOutboundReport
from infobip_cpaasx.models.mms_webhook_outbound_report_response import (
    MmsWebhookOutboundReportResponse,
)
from infobip_cpaasx.models.modify_application import ModifyApplication
from infobip_cpaasx.models.modify_entity import ModifyEntity
from infobip_cpaasx.models.number_price import NumberPrice
from infobip_cpaasx.models.number_registration_address import NumberRegistrationAddress
from infobip_cpaasx.models.number_registration_brand import NumberRegistrationBrand
from infobip_cpaasx.models.number_registration_brand_preview import (
    NumberRegistrationBrandPreview,
)
from infobip_cpaasx.models.number_registration_brand_status import (
    NumberRegistrationBrandStatus,
)
from infobip_cpaasx.models.number_registration_brand_vet import (
    NumberRegistrationBrandVet,
)
from infobip_cpaasx.models.number_registration_business_identifier import (
    NumberRegistrationBusinessIdentifier,
)
from infobip_cpaasx.models.number_registration_campaign import (
    NumberRegistrationCampaign,
)
from infobip_cpaasx.models.number_registration_data_universal_numbering_system_number import (
    NumberRegistrationDataUniversalNumberingSystemNumber,
)
from infobip_cpaasx.models.number_registration_document_metadata import (
    NumberRegistrationDocumentMetadata,
)
from infobip_cpaasx.models.number_registration_external_ten_dlc_campaign import (
    NumberRegistrationExternalTenDlcCampaign,
)
from infobip_cpaasx.models.number_registration_global_intermediary_identification_number import (
    NumberRegistrationGlobalIntermediaryIdentificationNumber,
)
from infobip_cpaasx.models.number_registration_government_brand import (
    NumberRegistrationGovernmentBrand,
)
from infobip_cpaasx.models.number_registration_interactive_voice_response_opt_in import (
    NumberRegistrationInteractiveVoiceResponseOptIn,
)
from infobip_cpaasx.models.number_registration_keyword_opt_in import (
    NumberRegistrationKeywordOptIn,
)
from infobip_cpaasx.models.number_registration_legal_entity_identifier import (
    NumberRegistrationLegalEntityIdentifier,
)
from infobip_cpaasx.models.number_registration_network_status import (
    NumberRegistrationNetworkStatus,
)
from infobip_cpaasx.models.number_registration_non_profit_brand import (
    NumberRegistrationNonProfitBrand,
)
from infobip_cpaasx.models.number_registration_number_preview import (
    NumberRegistrationNumberPreview,
)
from infobip_cpaasx.models.number_registration_opt_ins import NumberRegistrationOptIns
from infobip_cpaasx.models.number_registration_page_info import (
    NumberRegistrationPageInfo,
)
from infobip_cpaasx.models.number_registration_page_response_brand import (
    NumberRegistrationPageResponseBrand,
)
from infobip_cpaasx.models.number_registration_page_response_brand_vet import (
    NumberRegistrationPageResponseBrandVet,
)
from infobip_cpaasx.models.number_registration_page_response_campaign import (
    NumberRegistrationPageResponseCampaign,
)
from infobip_cpaasx.models.number_registration_private_company_brand import (
    NumberRegistrationPrivateCompanyBrand,
)
from infobip_cpaasx.models.number_registration_public_company_brand import (
    NumberRegistrationPublicCompanyBrand,
)
from infobip_cpaasx.models.number_registration_ten_dlc_campaign import (
    NumberRegistrationTenDlcCampaign,
)
from infobip_cpaasx.models.number_registration_update_brand_request import (
    NumberRegistrationUpdateBrandRequest,
)
from infobip_cpaasx.models.number_registration_update_campaign_request import (
    NumberRegistrationUpdateCampaignRequest,
)
from infobip_cpaasx.models.number_registration_verbal_opt_in import (
    NumberRegistrationVerbalOptIn,
)
from infobip_cpaasx.models.number_registration_web_opt_in import (
    NumberRegistrationWebOptIn,
)
from infobip_cpaasx.models.number_response import NumberResponse
from infobip_cpaasx.models.numbers_auto_response_action import NumbersAutoResponseAction
from infobip_cpaasx.models.numbers_block_action import NumbersBlockAction
from infobip_cpaasx.models.numbers_delivery_time_window import NumbersDeliveryTimeWindow
from infobip_cpaasx.models.numbers_edit_permissions import NumbersEditPermissions
from infobip_cpaasx.models.numbers_forward_to_ivr_action_details import (
    NumbersForwardToIvrActionDetails,
)
from infobip_cpaasx.models.numbers_forward_to_subscription_details import (
    NumbersForwardToSubscriptionDetails,
)
from infobip_cpaasx.models.numbers_http_forward_action import NumbersHttpForwardAction
from infobip_cpaasx.models.numbers_mail_forward_action import NumbersMailForwardAction
from infobip_cpaasx.models.numbers_mo_action import NumbersMoAction
from infobip_cpaasx.models.numbers_mo_configuration import NumbersMoConfiguration
from infobip_cpaasx.models.numbers_mo_configurations import NumbersMoConfigurations
from infobip_cpaasx.models.numbers_mo_non_forward_action import (
    NumbersMoNonForwardAction,
)
from infobip_cpaasx.models.numbers_no_action import NumbersNoAction
from infobip_cpaasx.models.numbers_pull_action import NumbersPullAction
from infobip_cpaasx.models.numbers_purchase_number_request import (
    NumbersPurchaseNumberRequest,
)
from infobip_cpaasx.models.numbers_response import NumbersResponse
from infobip_cpaasx.models.numbers_smpp_forward_action import NumbersSmppForwardAction
from infobip_cpaasx.models.numbers_stored_mo_configuration import (
    NumbersStoredMoConfiguration,
)
from infobip_cpaasx.models.numbers_use_conversation import NumbersUseConversation
from infobip_cpaasx.models.numbers_voice_action_details import NumbersVoiceActionDetails
from infobip_cpaasx.models.numbers_voice_call_forward_to_application_details import (
    NumbersVoiceCallForwardToApplicationDetails,
)
from infobip_cpaasx.models.numbers_voice_number_masking_action_details import (
    NumbersVoiceNumberMaskingActionDetails,
)
from infobip_cpaasx.models.numbers_voice_setup import NumbersVoiceSetup
from infobip_cpaasx.models.page_application import PageApplication
from infobip_cpaasx.models.page_entity import PageEntity
from infobip_cpaasx.models.page_info import PageInfo
from infobip_cpaasx.models.page_resource_association import PageResourceAssociation
from infobip_cpaasx.models.resource_association_request import (
    ResourceAssociationRequest,
)
from infobip_cpaasx.models.resource_association_response import (
    ResourceAssociationResponse,
)
from infobip_cpaasx.models.resource_type import ResourceType
from infobip_cpaasx.models.sms_advanced_binary_request import SmsAdvancedBinaryRequest
from infobip_cpaasx.models.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_cpaasx.models.sms_binary_content import SmsBinaryContent
from infobip_cpaasx.models.sms_binary_message import SmsBinaryMessage
from infobip_cpaasx.models.sms_bulk_request import SmsBulkRequest
from infobip_cpaasx.models.sms_bulk_response import SmsBulkResponse
from infobip_cpaasx.models.sms_bulk_status import SmsBulkStatus
from infobip_cpaasx.models.sms_bulk_status_response import SmsBulkStatusResponse
from infobip_cpaasx.models.sms_delivery_day import SmsDeliveryDay
from infobip_cpaasx.models.sms_delivery_result import SmsDeliveryResult
from infobip_cpaasx.models.sms_delivery_time_from import SmsDeliveryTimeFrom
from infobip_cpaasx.models.sms_delivery_time_to import SmsDeliveryTimeTo
from infobip_cpaasx.models.sms_delivery_time_window import SmsDeliveryTimeWindow
from infobip_cpaasx.models.sms_destination import SmsDestination
from infobip_cpaasx.models.sms_error import SmsError
from infobip_cpaasx.models.sms_inbound_message import SmsInboundMessage
from infobip_cpaasx.models.sms_inbound_message_result import SmsInboundMessageResult
from infobip_cpaasx.models.sms_india_dlt_options import SmsIndiaDltOptions
from infobip_cpaasx.models.sms_language import SmsLanguage
from infobip_cpaasx.models.sms_language_configuration import SmsLanguageConfiguration
from infobip_cpaasx.models.sms_log import SmsLog
from infobip_cpaasx.models.sms_logs_response import SmsLogsResponse
from infobip_cpaasx.models.sms_preview import SmsPreview
from infobip_cpaasx.models.sms_preview_request import SmsPreviewRequest
from infobip_cpaasx.models.sms_preview_response import SmsPreviewResponse
from infobip_cpaasx.models.sms_price import SmsPrice
from infobip_cpaasx.models.sms_regional_options import SmsRegionalOptions
from infobip_cpaasx.models.sms_report import SmsReport
from infobip_cpaasx.models.sms_response import SmsResponse
from infobip_cpaasx.models.sms_response_details import SmsResponseDetails
from infobip_cpaasx.models.sms_sending_speed_limit import SmsSendingSpeedLimit
from infobip_cpaasx.models.sms_speed_limit_time_unit import SmsSpeedLimitTimeUnit
from infobip_cpaasx.models.sms_status import SmsStatus
from infobip_cpaasx.models.sms_textual_message import SmsTextualMessage
from infobip_cpaasx.models.sms_tracking import SmsTracking
from infobip_cpaasx.models.sms_turkey_iys_options import SmsTurkeyIysOptions
from infobip_cpaasx.models.sms_update_status_request import SmsUpdateStatusRequest
from infobip_cpaasx.models.sms_url_options import SmsUrlOptions
from infobip_cpaasx.models.sms_webhook_inbound_report import SmsWebhookInboundReport
from infobip_cpaasx.models.sms_webhook_inbound_report_response import (
    SmsWebhookInboundReportResponse,
)
from infobip_cpaasx.models.sms_webhook_outbound_report import SmsWebhookOutboundReport
from infobip_cpaasx.models.sms_webhook_outbound_report_response import (
    SmsWebhookOutboundReportResponse,
)
from infobip_cpaasx.models.webhook_message_count import WebhookMessageCount
