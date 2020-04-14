from collections import MutableSequence
from flask import abort as flask_abort
from flask_restful import reqparse
from werkzeug import exceptions
from flask import current_app
from flask import Response
from flask import request
import flask_restful
import six

class Argument(reqparse.Argument):
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
                error_msg = u"Missing required parameter in {0}".format(
                    reqparse._friendly_location.get(self.location, self.location)
                )
            else:
                friendly_locations = [reqparse._friendly_location.get(loc, loc)
                                      for loc in self.location]
                error_msg = u"Missing required parameter in {0}".format(
                    " or ".join(friendly_locations)
                )
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

class RequestParser(reqparse.RequestParser):
    def __init__(self, argument_class=Argument, namespace_class=reqparse.Namespace,
                 trim=False, bundle_errors=False):
        self.args = []
        self.argument_class = argument_class
        self.namespace_class = namespace_class
        self.trim = trim
        self.bundle_errors = bundle_errors

    def parse_args(self, req=None, strict=False, http_error_code=400):
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
            flask_restful.abort(http_error_code, message=errors)

        if strict and req.unparsed_arguments:
            raise exceptions.BadRequest("Unknown arguments: %s"
                                        % ", ".join(req.unparsed_arguments.keys()))

        return namespace
