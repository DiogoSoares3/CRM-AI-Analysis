{% macro call_create_won_stage_data(endpoint_url) %}
    {% set command = "curl -X POST " ~ endpoint_url %}
    {% do run_query(command) %}
    {% do log("Endpoint chamado: " ~ endpoint_url, info=True) %}
{% endmacro %}