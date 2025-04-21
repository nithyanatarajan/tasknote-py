# src/notes/settings.py
from pathlib import Path

from src.common.config_loader import load_config_for
from src.common.settings import BaseServiceSettings

env_file = Path(__file__).parent / '.env'
defaults = load_config_for('notes', env_file=env_file)

settings = BaseServiceSettings(**defaults)
