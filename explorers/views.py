import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django_datatables_view.base_datatable_view import BaseDatatableView

from accounts.decorators import otp_required
from accounts.mixins import OTPRequiredMixin
from explorers.constants import TABLE_COLUMN_MAP
from explorers.models import PantasEmissionFactor
from explorers.utils import get_field_value


@login_required
@otp_required
def show_emission_factor(request, external_id):
    emission_factor = get_object_or_404(
        PantasEmissionFactor, external_id=external_id)

    # TODO: This is a temporary solution (as discussed) to prevent non staff to be able to see
    # the following two lines in the description of the EF, if they exist.
    if not request.user.is_staff:
        sentences_to_hide = [
            "NOTE: This dataset has been deprecated by the source and will be replaced soon.",
            "NOTE: This dataset has been deprecated by the source and will be removed soon."
        ]

        for sentence in sentences_to_hide:
            emission_factor.description = emission_factor.description.replace(
                sentence,
                ""
            )

    return render(
        request,
        "show-emission-factor.html",
        {
            "emission_factor": emission_factor,
        },
    )


@login_required
@otp_required
def list_emission_factors(request):
    if not request.user.is_staff:
        raise Http404

    return render(
        request,
        "list_emission_factors.html",
    )


class EmessionFactorsList(LoginRequiredMixin, OTPRequiredMixin, BaseDatatableView):
    # Define maximum display length
    max_display_length = 100
    # Define column names
    columns = [
        "description",
        "name",
        "source",
        "year_released",
        "region",
        "sector",
        "category",
        "unit_type",
        "emission_factor_value",
        "external_source_emission_factor.external_source_version",
    ]
    # Define order columns
    # Default order set to 'name' due to the first column being 'description'
    # (which is hidden as a child of the table row)
    order_columns = [
        "name",  # Default order
        "name",
        "source",
        "year_released",
        "region",
        "sector",
        "category",
        "unit_type",
        "",     # use empty value like '' for non-sortable columns
        "external_source_emission_factor.external_source_version",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filtered_queryset = None

    def get_initial_queryset(self):
        # Query the db to get related info
        self.filtered_queryset = PantasEmissionFactor.objects.get_all_latest_ef()
        return self.filtered_queryset

    def filter_queryset(self, qs):
        # Extract query parameters
        desc = self.request.POST.get("search[value]")

        # Define filter parameters based on query parameters
        filter_kwargs = {"description__icontains": desc} if desc else {}

        # columns with search filter (1 to 7) in the table header
        for idx in range(1, 8):
            col_search_value = self.request.POST.get(
                f"columns[{idx}][search][value]", ""
            )

            # case-insensitive search (icontains) for text search bar in col == 1
            if idx in [1]:
                filter_kwargs[f"{TABLE_COLUMN_MAP[str(idx)]}__icontains"] = (
                    col_search_value
                )
            # Exact match filter for dropdown filter
            elif (
                col_search_value
                and col_search_value != "All"
                and col_search_value != "-"
            ):
                filter_kwargs[f"{TABLE_COLUMN_MAP[str(idx)]}"] = (
                    col_search_value
                )
            elif col_search_value == "-":
                filter_kwargs[f"{TABLE_COLUMN_MAP[str(idx)]}"] = "-"

        # Perform filter on the query set"
        if filter_kwargs:
            self.filtered_queryset = qs.filter(**filter_kwargs)
            return self.filtered_queryset
        return qs

    def render_column(self, row, column):
        # "Replace __ to . for `external_source_emission_factor.external_source_version`
        column = column.replace("__", ".")
        value = super().render_column(row, column)

        # Format the output for ef_value
        if column == "emission_factor_value":
            emission_factor_value = row.emission_factor_value
            emission_value = [
                str(values) + row.unit
                for values in emission_factor_value.values()
                if values is not None
            ]

            emission_value = "\n".join(emission_value)
            return emission_value
        return value

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        original_data = response.content.decode("utf-8")
        original_json = json.loads(original_data)

        # Get all the distinct value for dropdown filter columns
        distinct_fields = get_field_value(
            all_pantas_ef_objs=self.filtered_queryset,
            fields=[
                "source",
                "year_released",
                "region",
                "sector",
                "category",
                "unit_type",
            ],
        )
        modified_data = {
            "columnFilters": distinct_fields,
            "data": original_json["data"],
            "draw": original_json["draw"],
            "recordsFiltered": original_json["recordsFiltered"],
            "recordsTotal": original_json["recordsTotal"],
        }
        return JsonResponse(modified_data)
