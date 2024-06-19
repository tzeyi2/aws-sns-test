from django.urls import path

from . import views

urlpatterns = [
    # verb comes after the noun
    # also, companies should not be prefixed with account preferably
    # add has to come before the url with regular expression for show and edit
    path(
        "emission-factors/", views.list_emission_factors, name="list_emission_factors"
    ),
    path(
        "emission-factors/<uuid:external_id>/",
        views.show_emission_factor,
        name="show_emission_factor",
    ),
    path(
        "emission-factors/ajax/",
        views.EmessionFactorsList.as_view(),
        name="ajax_show_emission_factor",
    ),
]
