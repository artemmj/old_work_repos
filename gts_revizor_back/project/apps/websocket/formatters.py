class ErrorFormatter:
    @classmethod
    def format(cls, errors, status_code):
        return {
            'errors': errors,
            'status_code': status_code,
            'is_error': True,
        }
