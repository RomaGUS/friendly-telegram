from werkzeug.datastructures import MultiDict, FileStorage
from collections import MutableSequence
from flask import current_app, request
from flask import abort as flask_abort
from werkzeug import exceptions
from hikka.errors import abort
from flask import Response
from copy import deepcopy
import decimal
import six

available_location = {
    u"json": u"the JSON body",
    u"form": u"the post body",
    u"args": u"the query string",
    u"values": u"the post body or the query string",
    u"headers": u"the HTTP headers",
    u"cookies": u"the request's cookies",
    u"files": u"an uploaded file",
}

class Namespace(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

class Argument(object):
    def __init__(self, name, default=None, dest=None, required=False,
                 ignore=False, type=lambda x: six.text_type(x), location=("json", "values"),
                 choices=(), action="store", help=None, operators=("="),
                 case_sensitive=True, store_missing=True, trim=False,
                 nullable=True):

        self.name = name
        self.default = default
        self.dest = dest
        self.required = required
        self.ignore = ignore
        self.location = location
        self.type = type
        self.choices = choices
        self.action = action
        self.help = help
        self.case_sensitive = case_sensitive
        self.operators = operators
        self.store_missing = store_missing
        self.trim = trim
        self.nullable = nullable

    def source(self, request):
        if isinstance(self.location, six.string_types):
            value = getattr(request, self.location, MultiDict())
            if callable(value):
                value = value()
            if value is not None:
                return value
        else:
            values = MultiDict()
            for l in self.location:
                value = getattr(request, l, None)
                if callable(value):
                    value = value()
                if value is not None:
                    values.update(value)
            return values

        return MultiDict()

    def convert(self, value, op):
        if value is None:
            if self.nullable:
                return None
            else:
                raise ValueError("Must not be null!")

        elif isinstance(value, FileStorage) and self.type == FileStorage:
            return value

        try:
            return self.type(value, self.name, op)
        except TypeError:
            try:
                if self.type is decimal.Decimal:
                    return self.type(str(value))
                else:
                    return self.type(value, self.name)
            except TypeError:
                return self.type(value)

    def handle_validation_error(self, error, bundle_errors):
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg

        response = abort("general", "missing-field")
        flask_abort(response)

    def parse(self, request, bundle_errors=False):
        source = self.source(request)

        results = []
        _not_found = False
        _found = True

        for operator in self.operators:
            name = self.name + operator.replace("=", "", 1)
            if name in source:
                if hasattr(source, "getlist"):
                    values = source.getlist(name)
                else:
                    values = source.get(name)
                    if not (isinstance(values, MutableSequence) and self.action == "append"):
                        values = [values]

                for value in values:
                    if hasattr(value, "strip") and self.trim:
                        value = value.strip()
                    if hasattr(value, "lower") and not self.case_sensitive:
                        value = value.lower()

                        if hasattr(self.choices, "__iter__"):
                            self.choices = [choice.lower()
                                            for choice in self.choices]

                    try:
                        value = self.convert(value, operator)
                    except Exception as error:
                        self.type(value)
                        if self.ignore:
                            continue
                        return self.handle_validation_error(error, bundle_errors)

                    if self.choices and value not in self.choices:
                        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                            return self.handle_validation_error(
                                ValueError(u"{0} is not a valid choice".format(
                                    value)), bundle_errors)
                        self.handle_validation_error(
                            ValueError(u"{0} is not a valid choice".format(
                                value)), bundle_errors)

                    if name in request.unparsed_arguments:
                        request.unparsed_arguments.pop(name)
                    results.append(value)

        if not results and self.required:
            if isinstance(self.location, six.string_types):
                error = available_location.get(self.location, self.location)
                error_msg = f"Missing required parameter in {error}"
            else:
                friendly_locations = [available_location.get(loc, loc)
                                      for loc in self.location]
                error = " or ".join(friendly_locations)
                error_msg = f"Missing required parameter in {error}"

            if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                return self.handle_validation_error(ValueError(error_msg), bundle_errors)
            self.handle_validation_error(ValueError(error_msg), bundle_errors)

        if not results:
            if callable(self.default):
                return self.default(), _not_found
            else:
                return self.default, _not_found

        if self.action == "append":
            return results, _found

        if self.action == "store" or len(results) == 1:
            return results[0], _found

        return results, _found


class RequestParser(object):
    def __init__(self, argument_class=Argument, namespace_class=Namespace,
                 trim=False, bundle_errors=False):
        self.args = []
        self.argument_class = argument_class
        self.namespace_class = namespace_class
        self.trim = trim
        self.bundle_errors = bundle_errors

    def argument(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], self.argument_class):
            self.args.append(args[0])
        else:
            self.args.append(self.argument_class(*args, **kwargs))

        if self.trim and self.argument_class is Argument:
            self.args[-1].trim = kwargs.get("trim", self.trim)

        return self

    def parse(self, req=None, strict=False, http_error_code=400):
        if req is None:
            req = request

        namespace = self.namespace_class()

        req.unparsed_arguments = dict(self.argument_class("").source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value

            if type(value) is Response:
                flask_abort(value)

        if errors:
            response = abort("general", "missing-field")
            flask_abort(response)

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest("Unknown arguments: %s"
                                        % ", ".join(req.unparsed_arguments.keys()))

        return namespace

    def copy(self):
        parser_copy = self.__class__(self.argument_class, self.namespace_class)
        parser_copy.args = deepcopy(self.args)
        parser_copy.trim = self.trim
        parser_copy.bundle_errors = self.bundle_errors
        return parser_copy

    def replace_argument(self, name, *args, **kwargs):
        new_arg = self.argument_class(name, *args, **kwargs)
        for index, arg in enumerate(self.args[:]):
            if new_arg.name == arg.name:
                del self.args[index]
                self.args.append(new_arg)
                break
        return self

    def remove_argument(self, name):
        for index, arg in enumerate(self.args[:]):
            if name == arg.name:
                del self.args[index]
                break
        return self
