import datetime
import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.db.models.expressions import Case, When
from django.db.models.functions import Lower
from django.urls import reverse
from simple_history.models import HistoricalRecords
from pgvector.django import VectorField

from accounts.models import User
from green.models import CustomModel
from green.utils import DecimalDecoder


def max_current_year(value):
    current_year = datetime.date.today().year
    return MaxValueValidator(current_year)(value)


class ExternalSourceEmissionFactorManager(models.Manager):
    def get_by_natural_key(self, external_source_id, external_source_name):
        return self.get(external_source_id=external_source_id,
                        external_source_name=external_source_name)


class ExternalSourceEmissionFactor(CustomModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_source_page_link = models.URLField(
        blank=True, null=True, max_length=2048, help_text="URL of the data that we scraped from.")
    external_source_id = models.CharField(
        max_length=256, help_text="ID of the data that we scraped from.")
    activity_id = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    source = models.CharField(
        max_length=128, help_text="Original source of the information, e.g. GHG Protocol, EPA, etc.")
    source_link = models.URLField(
        max_length=2048, help_text="URL of original source.")
    year_released = models.IntegerField(
        validators=[MinValueValidator(1970), max_current_year])
    region = models.CharField(max_length=128)
    region_code = models.CharField(max_length=64)
    sector = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    unit_type = models.CharField(max_length=64)
    lca_activity = models.CharField(max_length=128)
    method_applied = models.CharField(max_length=64)
    method_supported = models.CharField(max_length=64)
    origin = models.CharField(max_length=64)
    unit = models.CharField(max_length=64)
    # e.g. {'CO2e': 120.179, 'CO2': 118.17, 'CH4': 0.032, 'N2O': 0.0042}
    emission_factor_value = models.JSONField(
        default=dict, encoder=DjangoJSONEncoder, decoder=DecimalDecoder)
    # ex: climatiq.io
    external_source_name = models.CharField(max_length=32)
    external_source_version = models.CharField(
        max_length=32, blank=True, null=True)

    raw_data = models.JSONField(default=dict)

    history = HistoricalRecords()
    objects = ExternalSourceEmissionFactorManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['external_source_id', 'external_source_name'], name='externalsourceemissionfactor_unique_constraint')
        ]

    def __str__(self):
        return f'{self.id} version={self.external_source_version} external_id={self.external_source_id}'


class UpdateExternalSourceEmissionFactor(CustomModel):
    external_source_emission_factor = models.OneToOneField(
        ExternalSourceEmissionFactor, unique=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    external_source_page_link = models.URLField(
        blank=True, null=True, max_length=2048)
    external_source_id = models.CharField(
        max_length=256, blank=True, null=True)
    activity_id = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=128, blank=True, null=True)
    source_link = models.URLField(max_length=2048, blank=True, null=True)
    year_released = models.IntegerField(
        validators=[MinValueValidator(1970), max_current_year], blank=True, null=True)
    region = models.CharField(max_length=128, blank=True, null=True)
    region_code = models.CharField(max_length=64, blank=True, null=True)
    sector = models.CharField(max_length=64, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    unit_type = models.CharField(max_length=64, blank=True, null=True)
    lca_activity = models.CharField(max_length=128, blank=True, null=True)
    method_applied = models.CharField(max_length=64, blank=True, null=True)
    method_supported = models.CharField(max_length=64, blank=True, null=True)
    origin = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=64, blank=True, null=True)
    emission_factor_value = models.JSONField(
        default=dict, blank=True, null=True, encoder=DjangoJSONEncoder, decoder=DecimalDecoder)
    external_source_name = models.CharField(
        max_length=32, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['external_source_id', 'external_source_name'], name='updateexternalsourceemissionfactor_unique_constraint')
        ]


class PantasEmissionFactorManager(models.Manager):
    def regions(self):
        return self.exclude(
            region__in=["Malaysia", "Singapore, SG"]
        ).order_by(
            Case(When(region__contains="Malaysia", then=0), default=1),
            'region'
        ).values_list('region', flat=True).distinct()

    def get_all_latest_ef(self):
        """
        It will get
        * climatiq EF that with latest version
        * all EF that not from climatiq source
        * climatiq EF that not exist in the latest version
        """
        all_objs = self.select_related(
            'external_source_emission_factor',
        ).all().annotate(
            name_lower=Lower("name"))

        if ClimatiqVersion.objects.exists():
            climatiq_source_name = "climatiq.io"
            latest_climatiq_version = ClimatiqVersion.objects.latest(
                "updated_at").latest
            filter_query = Q(
                external_source_name=climatiq_source_name,
                external_source_emission_factor__external_source_version=latest_climatiq_version,
            ) | ~Q(external_source_name=climatiq_source_name)
            pantas_ef_objs = all_objs.filter(filter_query)

            # need to exclude TGO from this name list
            # else there might be chance of missing actual EFs as it was filtered out based on TGO results
            # as TGO is for Thai only
            name_list = pantas_ef_objs.exclude(
                external_source_name__in=["TGO", "KBank_Research"]
            ).values_list("name_lower", flat=True)

            # Climatiq EFs not in the latest version are included if absent there.
            old_climatiq_ef_objs = all_objs.filter(
                Q(external_source_name=climatiq_source_name),
                (
                    Q(external_source_emission_factor__external_source_version__isnull=True)
                    | ~Q(
                        external_source_emission_factor__external_source_version=latest_climatiq_version
                    )
                ),
            ).exclude(name_lower__in=name_list)

            all_objs = pantas_ef_objs | old_climatiq_ef_objs
        return all_objs


class PantasEmissionFactor(CustomModel):
    """
    Pantas "golden" (output) table. This table is derived from
    `ExternalSourceEmissionFactor` and `UpdateExternalSourceEmissionFactor`.
    Should not modify this table directly.
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    external_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    external_source_emission_factor = models.OneToOneField(
        ExternalSourceEmissionFactor, unique=True, on_delete=models.CASCADE, editable=False)
    activity_id = models.CharField(
        max_length=512, blank=True, null=True)
    name = models.CharField(max_length=256, editable=False)
    description = models.TextField(editable=False)
    source = models.CharField(max_length=128, editable=False)
    source_link = models.URLField(max_length=2048, editable=False)
    year_released = models.IntegerField(
        validators=[MinValueValidator(1970), max_current_year], editable=False)
    region = models.CharField(max_length=128, editable=False)
    region_code = models.CharField(max_length=64, editable=False)
    sector = models.CharField(max_length=64, editable=False)
    category = models.CharField(max_length=64, editable=False)
    unit_type = models.CharField(max_length=64, editable=False)
    lca_activity = models.CharField(max_length=128, editable=False)
    method_applied = models.CharField(max_length=64, editable=False)
    method_supported = models.CharField(max_length=64, editable=False)
    origin = models.CharField(max_length=64, editable=False)
    unit = models.CharField(max_length=64, editable=False)
    emission_factor_value = models.JSONField(
        default=dict, editable=False, encoder=DjangoJSONEncoder, decoder=DecimalDecoder)
    external_source_name = models.CharField(max_length=32, editable=False)

    name_embedding = VectorField(dimensions=1024, blank=True, null=True)

    history = HistoricalRecords()
    objects = PantasEmissionFactorManager()

    def get_absolute_url(self):
        return reverse('show_emission_factor', kwargs={
            'external_id': self.external_id,
        })

    def __str__(self):
        return f'{self.external_id} | {self.name}'


class RegionConfiguration(CustomModel):
    climatiq_region = models.CharField(
        max_length=256, help_text="Region directly from Climatiq emission factors.")
    blocklist = ArrayField(
        models.CharField(max_length=256), blank=True, help_text="Activity data locations to directly exclude for this Climatiq region. **For non-country names, best to specify with country code. Separated by '|'")
    allowlist = ArrayField(
        models.CharField(max_length=256), help_text="Region(s) representing the Climatiq region. Must be available in the 'Region Geocode' table. **For non-country names, best to specify with country code. Separated by '|'")
    remark = models.TextField(
        blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['climatiq_region', 'blocklist', 'allowlist'], name='unique_climatiq_region_configuration'
            )
        ]


class RegionGeocode(CustomModel):
    region = models.CharField(
        max_length=256, help_text="Regions used in 'Region Configuration' table allowlist.")
    country = models.CharField(
        max_length=256, help_text="Country of the region. May be the same as region.", blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['region', 'latitude', 'longitude'], name='unique_region_geocode'
            )
        ]


class ClimatiqVersion(CustomModel):
    # data version for API
    latest = models.CharField(max_length=32, editable=False)
    # include EF additions, modification
    latest_minor = models.PositiveIntegerField(editable=False)
    # include EF additions and modificationss and remove older versions of EF
    latest_major = models.PositiveIntegerField(editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)
