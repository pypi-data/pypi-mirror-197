import json

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    db_auto_upgrade: bool = False
    admin_mode: bool = False
    enable_cache: bool = False
    cache_impl: str = "flaggery.cache.MemoryCache"
    cache_params: str = json.dumps({'expiry_sec': 60, 'cleanup_sec': 5 * 60})

    class Config:
        env_prefix = "flaggery_"
