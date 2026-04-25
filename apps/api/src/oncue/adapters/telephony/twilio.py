from twilio.request_validator import RequestValidator
from twilio.twiml.voice_response import Connect, VoiceResponse

from oncue.settings import settings


def validate_signature(
    url: str, params: dict[str, str], signature: str, *, auth_token: str | None = None
) -> bool:
    token = auth_token or settings.twilio_auth_token
    validator = RequestValidator(token)
    return bool(validator.validate(url, params, signature))


def _ws_url(path: str) -> str:
    base = settings.app_base_url.rstrip("/")
    if base.startswith("https://"):
        base = "wss://" + base[len("https://") :]
    elif base.startswith("http://"):
        base = "ws://" + base[len("http://") :]
    return f"{base}{path}"


def build_voice_twiml(call_sid: str, *, greeting: str | None = None) -> str:
    response = VoiceResponse()
    if greeting:
        response.say(greeting)
    connect = Connect()
    stream = connect.stream(url=_ws_url("/voice/stream"))
    stream.parameter(name="call_sid", value=call_sid)
    response.append(connect)
    return str(response)
