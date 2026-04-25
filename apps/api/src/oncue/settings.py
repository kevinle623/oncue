from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Twilio
    twilio_account_sid: str
    twilio_auth_token: str

    # Spotify
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://localhost:8000/v1/spotify/callback"

    # Deepgram / ElevenLabs / Anthropic
    deepgram_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    anthropic_api_key: str

    # Infra
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+asyncpg://oncue:oncue@localhost:5432/oncue"

    # Public app URL (used to build Twilio webhook + Media Stream URLs)
    app_base_url: str = "http://localhost:8000"
    # Disable in tests / local dev without ngrok
    twilio_validate_signature: bool = True


settings = Settings()
