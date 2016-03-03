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

from toscaparser.common.exception import ExceptionCollector
from toscaparser.common.exception import InvalidSchemaError
from toscaparser.utils.gettextutils import _


class PropertyDef(object):
    '''TOSCA built-in Property type.'''

    VALID_REQUIRED_VALUES = ['true', 'false']

    def __init__(self, name, value=None, schema=None):
        self.name = name
        self.value = value
        self.schema = schema

        try:
            self.schema['type']
        except KeyError:
            msg = (_('Schema definition of "%(pname)s" must have a "type" '
                     'attribute.') % dict(pname=self.name))
            ExceptionCollector.appendException(
                InvalidSchemaError(message=msg))

        if 'required' in self.schema:
            required = self.schema['required']
            if not isinstance(required, bool):
                if required.lower() not in self.VALID_REQUIRED_VALUES:
                    valid_values = ', '.join(self.VALID_REQUIRED_VALUES)
                    msg = (_('Schema definition of "%(propname)s" has '
                             '"required" attribute with invalid value '
                             '"%(value1)s". The value must be one of '
                             '"%(value2)s".') % {"propname": self.name,
                                                 "value1": required,
                                                 "value2": valid_values})
                    ExceptionCollector.appendException(
                        InvalidSchemaError(message=msg))

    @property
    def required(self):
        if self.schema:
            for prop_key, prop_value in self.schema.items():
                if prop_key == 'required' and prop_value:
                    return True
        return False

    @property
    def default(self):
        if self.schema:
            for prop_key, prop_value in self.schema.items():
                if prop_key == 'default':
                    return prop_value
        return None
