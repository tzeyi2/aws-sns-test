def get_field_value(all_pantas_ef_objs, fields):
    """
    Get all the distinct value from all_pantas_ef_objs for each distinct_fields
    """

    fields_value = []

    for field in fields:
        fields_value.append(
            list(
                all_pantas_ef_objs.order_by(field)
                .values_list(field, flat=True)
                .distinct()
            )
        )

    return fields_value
