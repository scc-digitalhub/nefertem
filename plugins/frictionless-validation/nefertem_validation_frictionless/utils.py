from __future__ import annotations

from frictionless import Schema
from nefertem_validation_frictionless.constraints import ConstraintFrictionless


def frictionless_schema_converter(schema: Schema | dict, resource_name: str) -> list[ConstraintFrictionless]:
    """
    Convert a frictionless schema in a list of ConstraintFrictionless.

    Parameters
    ----------
    schema : Union[dict, Schema]
        A valid frictionless Resource table schema.
    resource_name : str
        Name of the resource.

    Returns
    -------
    list[ConstraintFrictionless]
        A list of ConstraintFrictionless.
    """
    constraints = []
    for field in schema.get("fields", []):
        cnt = 0

        type_ = field.get("type")
        if type_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintFrictionless(
                type="frictionless",
                name=name,
                resources=[resource_name],
                title=name,
                field=field.get("name"),
                field_type=type_,
                constraint="type",
                value=type_,
                weight=5,
            )
            constraints.append(c)
            cnt += 1

        format_ = field.get("format")
        if format_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintFrictionless(
                type="frictionless",
                name=name,
                resources=[resource_name],
                title=name,
                field=field.get("name"),
                field_type=type_,
                constraint="format",
                value=format_,
                weight=5,
            )
            constraints.append(c)
            cnt += 1

        const = field.get("constraints", {})
        if const:
            for k, v in const.items():
                name = f'{field.get("name", "")}_{str(cnt)}'
                c = ConstraintFrictionless(
                    type="frictionless",
                    name=name,
                    resources=[resource_name],
                    title=name,
                    field=field.get("name"),
                    field_type=type_,
                    constraint=k,
                    value=v,
                    weight=5,
                )
                constraints.append(c)
                cnt += 1

    return constraints
