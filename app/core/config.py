from pydantic_settings  import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "fastapi_db"
    SECRET_KEY: str = "0da9a70396e92ce272852e75721bc8c227dea4a89cf8cbd5cebf4decb7c051a5"   
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # TEST_DB:str="mongodb://localhost:27017/"      
    # TEST_DB_NAME:str="test_api"
    class Config:
        env_file = ".env"

settings = Settings()

