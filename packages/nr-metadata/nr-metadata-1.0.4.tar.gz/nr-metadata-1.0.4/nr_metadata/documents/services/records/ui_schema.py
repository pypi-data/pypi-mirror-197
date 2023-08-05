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
from oarepo_vocabularies.services.ui_schemas import HierarchyUISchema

from nr_metadata.common.services.records.ui_schema import (
    AdditionalTitlesUISchema,
    NRAccessRightsVocabularyUISchema,
    NRAffiliationVocabularyUISchema,
    NRAuthorityIdentifierUISchema,
    NRAuthorityUIUISchema,
    NRAuthorityVocabularyUISchema,
    NRCountryVocabularyUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFunderVocabularyUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationPointUISchema,
    NRGeoLocationUISchema,
    NRItemRelationTypeVocabularyUISchema,
    NRLanguageVocabularyUISchema,
    NRLocationUISchema,
    NRObjectPIDUISchema,
    NRRelatedItemUISchema,
    NRResourceTypeVocabularyUISchema,
    NRSeriesUISchema,
    NRSubjectCategoryVocabularyUISchema,
    NRSubjectUISchema,
    NRSystemIdentifierUISchema,
)


class NRDegreeGrantorUISchema(ma.Schema):
    """NRDegreeGrantorUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRThesisUISchema(ma.Schema):
    """NRThesisUISchema schema."""

    dateDefended = l10n.LocalizedDate()
    defended = ma_fields.Boolean()
    degreeGrantor = ma_fields.Nested(lambda: NRDegreeGrantorUISchema())
    studyFields = ma_fields.List(ma_fields.String())


class NRDocumentMetadataUISchema(ma.Schema):
    """NRDocumentMetadataUISchema schema."""

    thesis = ma_fields.Nested(lambda: NRThesisUISchema())
    collection = ma_fields.String()
    title = ma_fields.String()
    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesUISchema())
    )
    creators = ma_fields.List(ma_fields.Nested(lambda: NRAuthorityUIUISchema()))
    contributors = ma_fields.List(ma_fields.Nested(lambda: NRAuthorityUIUISchema()))
    resourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularyUISchema())
    dateAvailable = l10n.LocalizedEDTF()
    dateModified = l10n.LocalizedEDTF()
    subjects = ma_fields.List(ma_fields.Nested(lambda: NRSubjectUISchema()))
    publishers = ma_fields.List(ma_fields.String())
    subjectCategories = ma_fields.List(
        ma_fields.Nested(lambda: NRSubjectCategoryVocabularyUISchema())
    )
    languages = ma_fields.List(ma_fields.Nested(lambda: NRLanguageVocabularyUISchema()))
    notes = ma_fields.List(ma_fields.String())
    abstract = ma_fields.String()
    methods = ma_fields.String()
    technicalInfo = ma_fields.String()
    rights = ma_fields.List(
        ma_fields.Nested(lambda: NRAccessRightsVocabularyUISchema())
    )
    accessRights = ma_fields.Nested(lambda: NRAccessRightsVocabularyUISchema())
    relatedItems = ma_fields.List(ma_fields.Nested(lambda: NRRelatedItemUISchema()))
    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: NRFundingReferenceUISchema())
    )
    version = ma_fields.String()
    geoLocations = ma_fields.List(ma_fields.Nested(lambda: NRGeoLocationUISchema()))
    accessibility = ma_fields.String()
    series = ma_fields.List(ma_fields.Nested(lambda: NRSeriesUISchema()))
    externalLocation = ma_fields.Nested(lambda: NRExternalLocationUISchema())
    originalRecord = ma_fields.String()
    objectIdentifiers = ma_fields.List(ma_fields.Nested(lambda: NRObjectPIDUISchema()))
    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRSystemIdentifierUISchema())
    )
    events = ma_fields.List(ma_fields.Nested(lambda: NREventUISchema()))


class NRDocumentRecordUISchema(ma.Schema):
    """NRDocumentRecordUISchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")
