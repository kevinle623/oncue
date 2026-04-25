from twilio.request_validator import RequestValidator

from oncue.adapters.telephony import twilio as twilio_adapter


def test_validate_signature_accepts_valid_signature() -> None:
    token = "test-token-123"
    url = "https://example.test/voice/incoming"
    params = {"CallSid": "CA123", "From": "+1555", "To": "+1666"}
    signature = RequestValidator(token).compute_signature(url, params)

    assert twilio_adapter.validate_signature(url, params, signature, auth_token=token)


def test_validate_signature_rejects_tampered_params() -> None:
    token = "test-token-123"
    url = "https://example.test/voice/incoming"
    params = {"CallSid": "CA123", "From": "+1555", "To": "+1666"}
    signature = RequestValidator(token).compute_signature(url, params)
    tampered = {**params, "From": "+1999"}

    assert not twilio_adapter.validate_signature(
        url, tampered, signature, auth_token=token
    )


def test_build_voice_twiml_includes_stream_and_call_sid(
    monkeypatch: object,
) -> None:
    twiml = twilio_adapter.build_voice_twiml("CA999", greeting="Hello.")

    assert twiml.startswith("<?xml")
    assert "<Say>Hello.</Say>" in twiml
    assert "<Connect>" in twiml
    assert "<Stream" in twiml
    assert "/v1/voice/stream" in twiml
    assert 'name="call_sid"' in twiml
    assert 'value="CA999"' in twiml


def test_build_voice_twiml_uses_wss_scheme_when_https(
    monkeypatch: object,
) -> None:
    from oncue import settings as settings_mod

    original = settings_mod.settings.app_base_url
    try:
        settings_mod.settings.app_base_url = "https://oncue.example.com"
        twiml = twilio_adapter.build_voice_twiml("CA1")
        assert "wss://oncue.example.com/v1/voice/stream" in twiml
    finally:
        settings_mod.settings.app_base_url = original
