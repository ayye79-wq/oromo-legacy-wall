from rest_framework.throttling import AnonRateThrottle


class SubmitThrottle(AnonRateThrottle):
    scope = 'submit'


class TributeThrottle(AnonRateThrottle):
    scope = 'tribute'
