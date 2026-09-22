{%- macro resolution_hours(from_column, to_column) %}
    {{ return("DATEDIFF('hour', " ~ from_column ~ ", " ~ to_column ~ ")") }}
{%- endmacro %}
