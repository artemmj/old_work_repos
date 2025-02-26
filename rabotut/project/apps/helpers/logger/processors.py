import os


def add_environment(_, __, event_dict):
    """Добавляет окружение в логи."""
    event_dict['build'] = os.getenv('BUILD')
    return event_dict


def gunicorn_log_parser(_, __, event_dict):
    """Разбирает лог gunicorn'а."""
    if event_dict.get('logger') != 'gunicorn.access':
        return event_dict
    message = event_dict['event']
    request_id = message.split()[0]
    event_dict['request_id'] = request_id if request_id != '-' else None
    return event_dict
