from matter_exceptions.detailed_exception import DetailedException


class AuthenticationFailedError(DetailedException):
    TOPIC = "Authentication Failed Error"
