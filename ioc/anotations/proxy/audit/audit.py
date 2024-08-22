class Audit:
    def __call__(self, func):
        func._is_audit = True  # Добавляем метаинформацию
        return func
