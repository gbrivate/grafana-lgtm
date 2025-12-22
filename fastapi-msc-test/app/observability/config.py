import logging
from pythonjsonlogger import jsonlogger
from opentelemetry.trace import get_current_span

class OTelJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_data, record, message_dict):
        super(OTelJsonFormatter, self).add_fields(log_data, record, message_dict)
        span = get_current_span()
        span_context = span.get_span_context()
        if span_context.is_valid:
            log_data['trace_id'] = format(span_context.trace_id, '032x')
            log_data['span_id'] = format(span_context.span_id, '016x')

def setup_logging():
    handler = logging.StreamHandler()
    formatter = OTelJsonFormatter(
        fmt='%(levelname)s %(name)s %(message)s %(asctime)s',
        reserved_attrs=['message', 'levelname', 'name', 'asctime']
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(handler)
    return logging.getLogger("app")