# -*- coding: utf-8 -*-
import copy
from datetime import datetime

import pytest

from brewtils.models import Parameter, Command, Instance, System, Request, PatchOperation, \
    LoggingConfig, Event, Queue, Job


@pytest.fixture
def ts_epoch():
    """Timestamp as epoch timestamp."""
    return 1451606400000


@pytest.fixture
def ts_dt():
    """Timestamp as a datetime."""
    return datetime(2016, 1, 1)


@pytest.fixture
def nested_parameter_dict():
    """Nested Parameter as a dictionary."""
    return {
        'key': 'nested',
        'type': None,
        'multi': None,
        'display_name': None,
        'optional': None,
        'default': None,
        'description': None,
        'choices': None,
        'parameters': [],
        'nullable': None,
        'maximum': None,
        'minimum': None,
        'regex': None,
        'form_input_type': None,
    }


@pytest.fixture
def parameter_dict(nested_parameter_dict):
    """Non-nested parameter as a dictionary."""
    return {
        'key': 'key',
        'type': 'Any',
        'multi': False,
        'display_name': 'display',
        'optional': True,
        'default': 'default',
        'description': 'desc',
        'choices': {
            'display': 'select',
            'strict': True,
            'type': 'static',
            'value': ['choiceA', 'choiceB'],
            'details': {}
        },
        'parameters': [nested_parameter_dict],
        'nullable': False,
        'maximum': 10,
        'minimum': 1,
        'regex': '.*',
        'form_input_type': None
    }


@pytest.fixture
def bg_parameter(parameter_dict):
    """Parameter based on the parameter_dict"""
    dict_copy = copy.deepcopy(parameter_dict)
    dict_copy['parameters'] = [Parameter(**dict_copy['parameters'][0])]
    return Parameter(**dict_copy)


@pytest.fixture
def _command_dict(parameter_dict):
    """Use the command_dict fixture instead."""
    return {
        'name': 'name',
        'description': 'desc',
        'id': '123f11af55a38e64799f1234',
        'parameters': [parameter_dict],
        'command_type': 'ACTION',
        'output_type': 'STRING',
        'schema': {},
        'form': {},
        'template': '<html></html>',
        'icon_name': 'icon!',
        'system': None  # TODO: Set this up
    }


@pytest.fixture
def _bg_command(_command_dict, bg_parameter):
    """Use the bg_command fixture instead."""
    dict_copy = copy.deepcopy(_command_dict)
    dict_copy['parameters'] = [bg_parameter]
    return Command(**dict_copy)


@pytest.fixture
def instance_dict(ts_epoch):
    """An instance represented as a dictionary."""
    return {
        'id': '584f11af55a38e64799fd1d4',
        'name': 'default',
        'description': 'desc',
        'status': 'RUNNING',
        'icon_name': 'icon!',
        'queue_type': 'rabbitmq',
        'queue_info': {
            'queue': 'abc[default]-0.0.1',
            'url': 'amqp://guest:guest@localhost:5672'
        },
        'status_info': {'heartbeat': ts_epoch},
        'metadata': {}
    }


@pytest.fixture
def bg_instance(instance_dict, ts_dt):
    """An instance as a model."""
    dict_copy = copy.deepcopy(instance_dict)
    dict_copy['status_info']['heartbeat'] = ts_dt
    return Instance(**dict_copy)


@pytest.fixture
def system_dict(instance_dict, _command_dict):
    """A system represented as a dictionary."""
    return {
        'name': 'name',
        'description': 'desc',
        'version': '1.0.0',
        'id': '584f11af55a38e64799f1234',
        'max_instances': 1,
        'instances': [instance_dict],
        'commands': [_command_dict],
        'icon_name': 'fa-beer',
        'display_name': 'non-offensive',
        'metadata': {'some': 'stuff'}
    }


@pytest.fixture
def bg_system(system_dict, bg_instance, _bg_command):
    """A system as a model."""
    dict_copy = copy.deepcopy(system_dict)
    dict_copy['instances'] = [bg_instance]
    dict_copy['commands'] = [_bg_command]
    return System(**dict_copy)


@pytest.fixture
def child_request_dict(ts_epoch):
    """A child request represented as a dictionary."""
    return {
        'system': 'child_system',
        'system_version': '1.0.0',
        'instance_name': 'default',
        'command': 'say',
        'id': '58542eb571afd47ead90d25f',
        'parameters': {},
        'comment': 'bye!',
        'output': 'nested output',
        'output_type': 'STRING',
        'status': 'CREATED',
        'command_type': 'ACTION',
        'created_at': ts_epoch,
        'updated_at': ts_epoch,
        'error_class': None,
        'metadata': {'child': 'stuff'},
        'has_parent': True,
    }


@pytest.fixture
def _child_request(child_request_dict, ts_dt):
    """Use child_request instead."""
    dict_copy = copy.deepcopy(child_request_dict)
    dict_copy['created_at'] = ts_dt
    dict_copy['updated_at'] = ts_dt
    return Request(**dict_copy)


@pytest.fixture
def parent_request_dict(ts_epoch):
    """A parent request represented as a dictionary."""
    return {
        'system': 'parent_system',
        'system_version': '1.0.0',
        'instance_name': 'default',
        'command': 'say',
        'id': '58542eb571afd47ead90d25f',
        'parent': None,
        'parameters': {},
        'comment': 'bye!',
        'output': 'nested output',
        'output_type': 'STRING',
        'status': 'CREATED',
        'command_type': 'ACTION',
        'created_at': ts_epoch,
        'updated_at': ts_epoch,
        'error_class': None,
        'metadata': {'parent': 'stuff'},
        'has_parent': False,
    }


@pytest.fixture
def _parent_request(parent_request_dict, ts_dt):
    """Use parent_request instead."""
    dict_copy = copy.deepcopy(parent_request_dict)
    dict_copy['created_at'] = ts_dt
    dict_copy['updated_at'] = ts_dt
    return Request(**dict_copy)


@pytest.fixture
def request_template_dict():
    return {
        'system': 'system',
        'system_version': '1.0.0',
        'instance_name': 'default',
        'command': 'speak',
        'parameters': {'message': 'hey!'},
        'comment': 'hi!',
        'metadata': {'request': 'stuff'},
    }


@pytest.fixture
def request_dict(parent_request_dict, child_request_dict, ts_epoch):
    """A request represented as a dictionary."""
    return {
        'system': 'system',
        'system_version': '1.0.0',
        'instance_name': 'default',
        'command': 'speak',
        'id': '58542eb571afd47ead90d25e',
        'parent': parent_request_dict,
        'children': [child_request_dict],
        'parameters': {'message': 'hey!'},
        'comment': 'hi!',
        'output': 'output',
        'output_type': 'STRING',
        'status': 'CREATED',
        'command_type': 'ACTION',
        'created_at': ts_epoch,
        'updated_at': ts_epoch,
        'error_class': 'ValueError',
        'metadata': {'request': 'stuff'},
        'has_parent': True,
    }


@pytest.fixture
def bg_request(request_dict, _parent_request, _child_request, ts_dt):
    """A request as a model."""
    dict_copy = copy.deepcopy(request_dict)
    dict_copy['parent'] = _parent_request
    dict_copy['children'] = [_child_request]
    dict_copy['created_at'] = ts_dt
    dict_copy['updated_at'] = ts_dt
    return Request(**dict_copy)


@pytest.fixture
def patch_dict():
    """A patch represented as a dictionary."""
    return {
        'operations': [
            {
                'operation': 'replace',
                'path': '/status',
                'value': 'RUNNING'
            }
        ]
    }


@pytest.fixture
def patch_many_dict():
    """Multiple patches represented as a dictionary."""
    return {
        'operations': [
            {'operation': 'replace', 'path': '/status', 'value': 'RUNNING'},
            {'operation': 'replace2', 'path': '/status2', 'value': 'RUNNING2'}
        ]
    }


@pytest.fixture
def patch_no_envelop_dict():
    """A patch without an envelope represented as a dictionary."""
    return {
        'operation': 'replace',
        'path': '/status',
        'value': 'RUNNING'
    }


@pytest.fixture
def bg_patch1(patch_many_dict):
    """A patch as a model."""
    return PatchOperation(**patch_many_dict['operations'][0])


@pytest.fixture
def bg_patch2(patch_many_dict):
    """A patch as a model."""
    return PatchOperation(**patch_many_dict['operations'][1])


@pytest.fixture
def logging_config_dict():
    """A logging config represented as a dictionary."""
    return {
        'level': 'INFO',
        'handlers': {
            'stdout': {
                'foo': 'bar'
            }
        },
        'formatters': {'default': {'format': LoggingConfig.DEFAULT_FORMAT}}
    }


@pytest.fixture
def bg_logging_config(logging_config_dict):
    """A logging config as a model."""
    return LoggingConfig(**logging_config_dict)


@pytest.fixture
def event_dict(ts_epoch):
    """An event represented as a dictionary."""
    return {
        'name': 'REQUEST_CREATED',
        'error': False,
        'payload': {'id': '58542eb571afd47ead90d25e'},
        'metadata': {'extra': 'info'},
        'timestamp': ts_epoch
    }


@pytest.fixture
def bg_event(event_dict, ts_dt):
    """An event as a model."""
    dict_copy = copy.deepcopy(event_dict)
    dict_copy['timestamp'] = ts_dt
    return Event(**dict_copy)


@pytest.fixture
def queue_dict():
    """A queue represented as a dictionary."""
    return {
        'name': 'echo.1-0-0.default',
        'system': 'echo',
        'version': '1.0.0',
        'instance': 'default',
        'system_id': '1234',
        'display': 'foo.1-0-0.default',
        'size': 3,
    }


@pytest.fixture
def bg_queue(queue_dict):
    """A queue as a model."""
    return Queue(**queue_dict)


@pytest.fixture
def job_dict(ts_epoch, request_template_dict):
    """A job represented as a dictionary."""
    return {
        'name': 'job_name',
        'id': 'job_id',
        'trigger_type': 'cron',
        'trigger_args': {'minutes': '*/5'},
        'request_template': request_template_dict,
        'misfire_grace_time': 3,
        'coalesce': True,
        'max_instances': 2,
        'next_run_time': ts_epoch,
    }


@pytest.fixture
def bg_job(job_dict, ts_dt):
    """A job as a model."""
    dict_copy = copy.deepcopy(job_dict)
    dict_copy['next_run_time'] = ts_dt
    return Job(**dict_copy)


@pytest.fixture
def bg_command(_bg_command, bg_system):
    """A comand as a model."""
    _bg_command.system = bg_system
    return _bg_command


@pytest.fixture
def command_dict(_command_dict, bg_system):
    """A command represented as a dictionary."""
    dict_copy = copy.deepcopy(_command_dict)
    dict_copy['system'] = {'id': bg_system.id}
    return dict_copy


@pytest.fixture
def child_request(_child_request, bg_request):
    """A child request as a model."""
    _child_request.parent = bg_request
    return _child_request


@pytest.fixture
def parent_request(_parent_request, bg_request):
    """A parent request as a model."""
    _parent_request.children = [bg_request]
    return _parent_request
