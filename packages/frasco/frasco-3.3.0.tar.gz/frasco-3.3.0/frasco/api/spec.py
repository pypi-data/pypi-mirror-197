from apispec import APISpec
from frasco.utils import join_url_rule, AttrDict
from frasco.request_params import RequestDataParam, get_marshmallow_schema, get_marshmallow_schema_instance
import re


try:
    from marshmallow import Schema as MarshmallowSchema
    from marshmallow.fields import Field as MarshmallowField
    from marshmallow.exceptions import ValidationError as MarshmallowValidationError
    from apispec.ext.marshmallow import MarshmallowPlugin, resolver as ma_schema_name_resolver
    from apispec.ext.marshmallow.field_converter import DEFAULT_FIELD_MAPPING
    marshmallow_available = True
except ImportError:
    marshmallow_available = False


def build_openapi_spec(api_version, with_security_scheme=False):
    plugins = []
    if marshmallow_available:
        plugins.append(MarshmallowPlugin())

    spec = APISpec(title="API %s" % api_version.version,
                    version=api_version.version,
                    openapi_version="3.0.2",
                    plugins=plugins)

    if with_security_scheme:
        spec.components.security_scheme("api_key_bearer_token", {"type": "http", "scheme": "bearer"})
        spec.components.security_scheme("api_key_header", {"type": "apiKey", "in": "header", "name": "X-Api-Key"})
        spec.components.response("InvalidUserInput", {"description": "InvalidUserInput"})
        spec.components.response("NotAuthenticatedError", {"description": "Authentification required"})
        spec.components.response("NotAuthorizedError", {"description": "Some permissions are missing to perform this request"})

    for service in api_version.iter_services():
        paths = {}
        tag = {"name": service.name}
        if service.description:
            tag["description"] = service.description
        spec.tag(tag)
        for rule, endpoint, func, options in service.iter_endpoints():
            rule = join_url_rule(api_version.url_prefix, join_url_rule(service.url_prefix, rule))
            path = paths.setdefault(convert_url_args(rule), {})
            for method in options.get('methods', ['GET']):
                op = build_spec_operation(spec, rule, service.name + '_' + endpoint, func, options, with_security_scheme)
                op['tags'] = [service.name]
                path[method.lower()] = op
        for path, operations in paths.items():
            spec.path(path=path, operations=operations)

    return spec


def build_spec_operation(spec, rule, endpoint, func, options, with_security_scheme=False):
    path_request_params = []
    query_request_params = []
    body_request_params = []
    file_request_params = []
    if hasattr(func, 'request_params'):
        url = convert_url_args(rule)
        method = options.get('methods', ['GET'])[0]
        for p in reversed(func.request_params):
            if isinstance(p, RequestDataParam):
                if not marshmallow_available or not get_marshmallow_schema(p.loader):
                    continue
                schema = get_marshmallow_schema(p.loader)
                for name, field in schema._declared_fields.items():
                    if not field.dump_only:
                        body_request_params.append((name, field.required, DEFAULT_FIELD_MAPPING.get(field.__class__, ('string', None))[0]))
                continue
            for pname in p.names:
                if p.location == 'files':
                    file_request_params.append((pname, p))
                elif ("{%s}" % pname) in url:
                    path_request_params.append((pname, p))
                elif method == 'GET':
                    query_request_params.append((pname, p))
                else:
                    body_request_params.append((pname, p.required, convert_type_to_spec(p.type)))

    params = [build_spec_param(n, p, "path") for (n, p) in path_request_params] \
           + [build_spec_param(n, p) for (n, p) in query_request_params]

    body_request_schema = None
    if body_request_params:
        body_request_schema = {
            "type": "object",
            "required": [n for (n, r, t) in body_request_params if r],
            "properties": {n: {"type": t} for (n, r, t) in body_request_params}
        }

    request_body = {}
    if body_request_schema:
        request_body["application/json"] = {"schema": body_request_schema}

    if file_request_params:
        file_properties = {}
        for pname, p in file_request_params:
            file_properties[pname] = {"type": "array", "items": {"type": "string", "format": "binary"}}
        request_body.setdefault("multipart/form-data", {}).setdefault("schema", {})\
            .setdefault("properties", {}).update(file_properties)

    responses = {
        "default": {"description": "Unexpected error"},
        "200": {"description": "Successful response"},
        "400": {"$ref": "#/components/responses/InvalidUserInput"}
    }
    if hasattr(func, 'marshalled_with') and marshmallow_available and get_marshmallow_schema(func.marshalled_with):
        schema = get_marshmallow_schema(func.marshalled_with)
        schema_name = ma_schema_name_resolver(schema)
        if schema_name not in spec.components.schemas:
            spec.components.schema(schema_name, schema=schema)
        if func.marshal_many:
            responses["200"]["content"] = {"application/json": {"schema": {"type": "array", "items": schema_name}}}
        else:
            responses["200"]["content"] = {"application/json": {"schema": schema_name}}

    if with_security_scheme:
        responses["401"] = {"$ref": "#/components/responses/NotAuthenticatedError"}
        responses["403"] = {"$ref": "#/components/responses/NotAuthorizedError"}

    o = {"operationId": endpoint,
         "parameters": params,
         "responses": responses}
    if func.__doc__:
        o['description'] = func.__doc__
    if request_body:
        o["requestBody"] = {"content": request_body}
    return o


def build_spec_param(name, request_param, loc="query"):
    o = {"name": name,
        "schema": {"type": convert_type_to_spec(request_param.type)},
        "required": loc == "path" or bool(request_param.required),
        "in": loc}
    if request_param.help:
        o['description'] = request_param.help
    return o


_url_arg_re = re.compile(r"<([a-z]+:)?([a-z0-9_]+)>")
def convert_url_args(url):
    return _url_arg_re.sub(r"{\2}", url)


def convert_type_to_spec(type):
    if type is int:
        return "integer"
    if type is float:
        return "number"
    if type is bool:
        return "boolean"
    return "string"
