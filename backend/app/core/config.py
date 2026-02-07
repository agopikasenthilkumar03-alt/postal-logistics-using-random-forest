from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Weather-Based Post Delay Prediction and SMS Notification System"
    database_url: str = "mysql+pymysql://postal_user:postal_pass@localhost:3306/postal_logistics"
    sms_provider: str = "twilio"
    sms_sender_number: str = "+910000000000"
    weather_api_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_api_key: str = ""
    model_path: str = "backend/data/random_forest_model.json"

    class Config:
        env_file = ".env"


settings = Settings()
