from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""

    # Spotify
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    spotify_redirect_uri: str = "http://localhost:8000/spotify/callback"

    # Deepgram / ElevenLabs / Anthropic
    deepgram_api_key: str = ""
    elevenlabs_api_key: str = ""
    anthropic_api_key: str = ""

    # Infra
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql+asyncpg://oncue:oncue@localhost:5432/oncue"

settings = Settings()