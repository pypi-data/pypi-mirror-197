import marshmallow as ma
from edtf import Date as EDTFDate
from edtf import Interval as EDTFInterval
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from marshmallow_utils.fields import edtfdatestring as mu_fields_edtf
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_date


class AdditionalTitlesSchema(ma.Schema):
    """AdditionalTitlesSchema schema."""

    title = ma_fields.String()
    titleType = ma_fields.String()


class NRAffiliationVocabularySchema(ma.Schema):
    """NRAffiliationVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRAuthorityIdentifierSchema(ma.Schema):
    """NRAuthorityIdentifierSchema schema."""

    identifier = ma_fields.String()
    scheme = ma_fields.String()


class NRAuthoritySchema(ma.Schema):
    """NRAuthoritySchema schema."""

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularySchema())
    )
    nameType = ma_fields.String()
    fullName = ma_fields.String()
    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierSchema())
    )


class NRAuthorityVocabularySchema(ma.Schema):
    """NRAuthorityVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRResourceTypeVocabularySchema(ma.Schema):
    """NRResourceTypeVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRSubjectSchema(ma.Schema):
    """NRSubjectSchema schema."""

    subjectScheme = ma_fields.String()
    subject = ma_fields.String()
    valueURI = ma_fields.String()
    classificationCode = ma_fields.String()


class NRSubjectCategoryVocabularySchema(ma.Schema):
    """NRSubjectCategoryVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRLanguageVocabularySchema(ma.Schema):
    """NRLanguageVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRAccessRightsVocabularySchema(ma.Schema):
    """NRAccessRightsVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRObjectPIDSchema(ma.Schema):
    """NRObjectPIDSchema schema."""

    identifier = ma_fields.String()
    scheme = ma_fields.String()


class NRItemRelationTypeVocabularySchema(ma.Schema):
    """NRItemRelationTypeVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRRelatedItemSchema(ma.Schema):
    """NRRelatedItemSchema schema."""

    itemTitle = ma_fields.String()
    itemCreators = ma_fields.List(ma_fields.Nested(lambda: NRAuthoritySchema()))
    itemContributors = ma_fields.List(ma_fields.Nested(lambda: NRAuthoritySchema()))
    itemPIDs = ma_fields.List(ma_fields.Nested(lambda: NRObjectPIDSchema()))
    itemURL = ma_fields.String()
    itemYear = ma_fields.Integer()
    itemVolume = ma_fields.String()
    itemIssue = ma_fields.String()
    itemStartPage = ma_fields.String()
    itemEndPage = ma_fields.String()
    itemPublisher = ma_fields.String()
    itemRelationType = ma_fields.Nested(lambda: NRItemRelationTypeVocabularySchema())
    itemResourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularySchema())


class NRFunderVocabularySchema(ma.Schema):
    """NRFunderVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRFundingReferenceSchema(ma.Schema):
    """NRFundingReferenceSchema schema."""

    projectID = ma_fields.String()
    projectName = ma_fields.String()
    fundingProgram = ma_fields.String()
    funder = ma_fields.Nested(lambda: NRFunderVocabularySchema())


class NRGeoLocationPointSchema(ma.Schema):
    """NRGeoLocationPointSchema schema."""

    pointLongitude = ma_fields.Float(
        validate=[ma_validate.Range(min_inclusive=-180.0, max_inclusive=180.0)]
    )
    pointLatitude = ma_fields.Float(
        validate=[ma_validate.Range(min_inclusive=-90.0, max_inclusive=90.0)]
    )


class NRGeoLocationSchema(ma.Schema):
    """NRGeoLocationSchema schema."""

    geoLocationPlace = ma_fields.String()
    geoLocationPoint = ma_fields.Nested(lambda: NRGeoLocationPointSchema())


class NRSeriesSchema(ma.Schema):
    """NRSeriesSchema schema."""

    seriesTitle = ma_fields.String()
    seriesVolume = ma_fields.String()


class NRExternalLocationSchema(ma.Schema):
    """NRExternalLocationSchema schema."""

    externalLocationURL = ma_fields.String()
    externalLocationNote = ma_fields.String()


class NRSystemIdentifierSchema(ma.Schema):
    """NRSystemIdentifierSchema schema."""

    identifier = ma_fields.String()
    scheme = ma_fields.String()


class NRCountryVocabularySchema(ma.Schema):
    """NRCountryVocabularySchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRLocationSchema(ma.Schema):
    """NRLocationSchema schema."""

    place = ma_fields.String()
    country = ma_fields.Nested(lambda: NRCountryVocabularySchema())


class NREventSchema(ma.Schema):
    """NREventSchema schema."""

    eventNameOriginal = ma_fields.String()
    eventNameAlternate = ma_fields.List(ma_fields.String())
    eventDate = ma_fields.String(
        validate=[mu_fields_edtf.EDTFValidator(types=(EDTFInterval,))]
    )
    eventLocation = ma_fields.Nested(lambda: NRLocationSchema())


class NRCommonMetadataSchema(ma.Schema):
    """NRCommonMetadataSchema schema."""

    title = ma_fields.String()
    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesSchema())
    )
    creators = ma_fields.List(ma_fields.Nested(lambda: NRAuthoritySchema()))
    contributors = ma_fields.List(ma_fields.Nested(lambda: NRAuthoritySchema()))
    resourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularySchema())
    dateAvailable = ma_fields.String(
        validate=[mu_fields_edtf.EDTFValidator(types=(EDTFDate,))]
    )
    dateModified = ma_fields.String(
        validate=[mu_fields_edtf.EDTFValidator(types=(EDTFDate,))]
    )
    subjects = ma_fields.List(ma_fields.Nested(lambda: NRSubjectSchema()))
    publishers = ma_fields.List(ma_fields.String())
    subjectCategories = ma_fields.List(
        ma_fields.Nested(lambda: NRSubjectCategoryVocabularySchema())
    )
    languages = ma_fields.List(ma_fields.Nested(lambda: NRLanguageVocabularySchema()))
    notes = ma_fields.List(ma_fields.String())
    abstract = ma_fields.String()
    methods = ma_fields.String()
    technicalInfo = ma_fields.String()
    rights = ma_fields.List(ma_fields.Nested(lambda: NRAccessRightsVocabularySchema()))
    accessRights = ma_fields.Nested(lambda: NRAccessRightsVocabularySchema())
    relatedItems = ma_fields.List(ma_fields.Nested(lambda: NRRelatedItemSchema()))
    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: NRFundingReferenceSchema())
    )
    version = ma_fields.String()
    geoLocations = ma_fields.List(ma_fields.Nested(lambda: NRGeoLocationSchema()))
    accessibility = ma_fields.String()
    series = ma_fields.List(ma_fields.Nested(lambda: NRSeriesSchema()))
    externalLocation = ma_fields.Nested(lambda: NRExternalLocationSchema())
    originalRecord = ma_fields.String()
    objectIdentifiers = ma_fields.List(ma_fields.Nested(lambda: NRObjectPIDSchema()))
    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRSystemIdentifierSchema())
    )
    events = ma_fields.List(ma_fields.Nested(lambda: NREventSchema()))


class NRCommonRecordSchema(InvenioBaseRecordSchema):
    """NRCommonRecordSchema schema."""

    metadata = ma_fields.Nested(lambda: NRCommonMetadataSchema())
    created = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
    updated = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
