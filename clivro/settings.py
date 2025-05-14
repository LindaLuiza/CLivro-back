import os


class Settings:
    def __init__(self, env_file: str = '.env'):
        self._load_env(env_file)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = self._str_to_int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def _load_env(self, file_path):
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found. Environment variables not loaded.")

    def _str_to_int(self, value: str) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0


settings = Settings()
