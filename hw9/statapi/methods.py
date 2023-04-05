import functools
import json
import logging
from enum import Enum

import psutil as ps
import toml
import yaml

# (!) Note: depends on PIP packages: psultil toml pyyaml


__all__ = ('methods')


def _parse_spec(spec):
    """Convert library-internal data structures.

    Conversion is done into general Python types.
    """

    if hasattr(spec, '_asdict'):
        # assume namedtuple
        spec = spec._asdict()

    if isinstance(spec, dict):
        return {k: _parse_spec(v) for k, v in spec.items()}
    if isinstance(spec, list):
        return [_parse_spec(itm) for itm in spec]
    if isinstance(spec, Enum):
        return spec.name
    return spec


# Dict of a form:
# formatter_name: (mimetype, format_function)
# ...
formatters = {
    'json': ('application/json', functools.partial(json.dumps, indent=2)),
    'toml': ('text', functools.partial(toml.dumps)),
    'yaml': ('text', functools.partial(yaml.dump, sort_keys=False, indent=2)),
    'repr': ('text', repr)
}


def method_api(method, format='json', **args):
    """Call method, parse result and format it accordingly."""

    spec = method(**args)
    parsed = _parse_spec(spec)  # convert to Python native structures

    # in case we got a list, not a dict, for it to be parsed correctly, we form a dict out ot it first
    if isinstance(parsed, list):
        data = []
        for item in parsed:
            if isinstance(item, dict):
                data.append(item)
            else:
                data.append({'value': item})
        parsed = {'data': data}
    # check if it is a single value, like an integer and output it in the correct format
    elif not isinstance(parsed, dict):
        parsed = {'value': parsed}

    mime, func = formatters.get(format, (None, None))
    if func is None:
        raise ValueError(400, f'Format {format} not supported')

    res = func(parsed)

    return res, mime;


# dict of methods wrapped for api calls of a form:
# method_name: method_callable

# start building
methods = dict.fromkeys([
    'boot_time', 'cpu_count', 'cpu_freq', 'cpu_percent', 'cpu_stats',
    'cpu_times', 'cpu_times_percent', 'disk_io_counters', 'disk_partitions',
    'getloadavg', 'net_if_stats', 'net_io_counters', 'sensors_battery',
    'sensors_fans', 'sensors_temperatures', 'swap_memory', 'virtual_memory',
    'wait_procs'
])
# get original methods by name
methods = {name: getattr(ps, name) for name in methods}
# patch one as it requires argument
methods['disk_usage'] = functools.partial(ps.disk_usage, '/')
# now wrap methods
methods = {
    name: functools.partial(method_api, func)
    for name, func in methods.items()
}

if __name__ == '__main__':
    spec = ps.cpu_freq()
    res = _parse_spec(spec)
    logging.log(logging.INFO, spec)
    mtd = methods['cpu_freq']
    res, mime = mtd(format='yaml')
    print(f'Yaml res:\n{res}')
    res, mime = mtd(format='json')
    print(f'Json res:\n{res}')
    res, mime = mtd(format='toml')
    print(f'Toml res:\n{res}')
