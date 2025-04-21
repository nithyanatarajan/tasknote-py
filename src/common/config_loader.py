# src/common/config_loader.py

import os

from pathlib import Path

import structlog
import yaml

from dotenv import load_dotenv


def load_config_for(service_name: str, env_file: Path) -> dict:
    logger = structlog.get_logger(__name__)
    load_dotenv(env_file)  # load per-service .env

    config_filename = os.getenv('CONFIG_FILEPATH', 'config/services.yaml')
    logger.info(f'Loading config from `{config_filename}`')

    config_file = Path(config_filename)

    if not config_file.exists():
        logger.warning(f'Config file not found: {config_file}. Proceeding with environment variables only.')
        return {}

    try:
        config = yaml.safe_load(config_file.read_text())
        logger.debug('Loaded config', content=config)
    except Exception as e:
        logger.error('Failed to parse YAML config', error=str(e))
        return {}

    service_config = config.get(service_name)
    if not service_config:
        logger.warning(
            f'No config block found for service: {service_name}. Proceeding with environment variables only.'
        )
        return {}

    envs = service_config.get('envs', {})
    logger.debug('Resolved service config', service=service_name, envs=envs)

    return envs
