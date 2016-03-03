#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

'''
TOSCA exception classes
'''
import logging
import sys
import traceback

from toscaparser.utils.gettextutils import _


log = logging.getLogger(__name__)


class TOSCAException(Exception):
    '''Base exception class for TOSCA

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property.

    '''

    _FATAL_EXCEPTION_FORMAT_ERRORS = False

    message = _('An unknown exception occurred.')

    def __init__(self, **kwargs):
        try:
            self.message = self.msg_fmt % kwargs
        except KeyError:
            exc_info = sys.exc_info()
            log.exception(_('Exception in string format operation: %s')
                          % exc_info[1])

            if TOSCAException._FATAL_EXCEPTION_FORMAT_ERRORS:
                raise exc_info[0]

    def __str__(self):
        return self.message

    @staticmethod
    def set_fatal_format_exception(flag):
        if isinstance(flag, bool):
            TOSCAException._FATAL_EXCEPTION_FORMAT_ERRORS = flag


class MissingRequiredFieldError(TOSCAException):
    msg_fmt = _('%(what)s is missing required field "%(required)s".')


class UnknownFieldError(TOSCAException):
    msg_fmt = _('%(what)s contains unknown field "%(field)s". Refer to the '
                'definition to verify valid values.')


class TypeMismatchError(TOSCAException):
    msg_fmt = _('%(what)s must be of type "%(type)s".')


class InvalidNodeTypeError(TOSCAException):
    msg_fmt = _('Node type "%(what)s" is not a valid type.')


class InvalidTypeError(TOSCAException):
    msg_fmt = _('Type "%(what)s" is not a valid type.')


class InvalidSchemaError(TOSCAException):
    msg_fmt = _('%(message)s')


class ValidationError(TOSCAException):
    msg_fmt = _('%(message)s')


class UnknownInputError(TOSCAException):
    msg_fmt = _('Unknown input "%(input_name)s".')


class InvalidPropertyValueError(TOSCAException):
    msg_fmt = _('Value of property "%(what)s" is invalid.')


class InvalidTemplateVersion(TOSCAException):
    msg_fmt = _('The template version "%(what)s" is invalid. '
                'Valid versions are "%(valid_versions)s".')


class InvalidTOSCAVersionPropertyException(TOSCAException):
    msg_fmt = _('Value of TOSCA version property "%(what)s" is invalid.')


class URLException(TOSCAException):
    msg_fmt = _('%(what)s')


class ToscaExtImportError(TOSCAException):
    msg_fmt = _('Unable to import extension "%(ext_name)s". '
                'Check to see that it exists and has no '
                'language definition errors.')


class ToscaExtAttributeError(TOSCAException):
    msg_fmt = _('Missing attribute in extension "%(ext_name)s". '
                'Check to see that it has required attributes '
                '"%(attrs)s" defined.')


class InvalidGroupTargetException(TOSCAException):
    msg_fmt = _('"%(message)s"')


class ExceptionCollector(object):

    exceptions = []
    collecting = False

    @staticmethod
    def clear():
        del ExceptionCollector.exceptions[:]

    @staticmethod
    def start():
        ExceptionCollector.clear()
        ExceptionCollector.collecting = True

    @staticmethod
    def stop():
        ExceptionCollector.collecting = False

    @staticmethod
    def contains(exception):
        for ex in ExceptionCollector.exceptions:
            if str(ex) == str(exception):
                return True
        return False

    @staticmethod
    def appendException(exception):
        if ExceptionCollector.collecting:
            if not ExceptionCollector.contains(exception):
                exception.trace = traceback.extract_stack()[:-1]
                ExceptionCollector.exceptions.append(exception)
        else:
            raise exception

    @staticmethod
    def exceptionsCaught():
        return len(ExceptionCollector.exceptions) > 0

    @staticmethod
    def getTraceString(traceList):
        traceString = ''
        for entry in traceList:
            f, l, m, c = entry[0], entry[1], entry[2], entry[3]
            traceString += (_('\t\tFile %(file)s, line %(line)s, in '
                              '%(method)s\n\t\t\t%(call)s\n')
                            % {'file': f, 'line': l, 'method': m, 'call': c})
        return traceString

    @staticmethod
    def getExceptionReportEntry(exception, full=True):
        entry = exception.__class__.__name__ + ': ' + str(exception)
        if full:
            entry += '\n' + ExceptionCollector.getTraceString(exception.trace)
        return entry

    @staticmethod
    def getExceptions():
        return ExceptionCollector.exceptions

    @staticmethod
    def getExceptionsReport(full=True):
        report = []
        for exception in ExceptionCollector.exceptions:
            report.append(
                ExceptionCollector.getExceptionReportEntry(exception, full))
        return report

    @staticmethod
    def assertExceptionMessage(exception, message):
        err_msg = exception.__name__ + ': ' + message
        report = ExceptionCollector.getExceptionsReport(False)
        assert err_msg in report, (_('Could not find "%(msg)s" in "%(rep)s".')
                                   % {'rep': report.__str__(), 'msg': err_msg})
