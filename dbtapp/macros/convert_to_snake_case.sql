{% macro convert_to_snake_case(relation) %}
    {# Fetch columns using dbt's built-in adapter #}
    {% set columns = adapter.get_columns_in_relation(relation) %}
    {% set re = modules.re %}
    {% set rename_dict = {} %}

    {% for column in columns %}
        {# Regex looks for camelCase or mixed spacing boundaries and injects underscores #}
        {% do rename_dict.update({column.column: re.sub("(?<!^)([A-Z][a-z]|(?<=[a-z])[^a-z_]|(?<=[A-Z])[0-9])", "_\\g<1>", column.column).lower()}) %}
    {% endfor %}

    {{ return(rename_dict) }}
{% endmacro %}