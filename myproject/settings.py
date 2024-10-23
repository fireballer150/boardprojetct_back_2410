INSTALLED_APPS = [
    # ... 기존 앱들 ...
    'django_filters',
]

REST_FRAMEWORK = {
    # ... 기존 설정 ...
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
