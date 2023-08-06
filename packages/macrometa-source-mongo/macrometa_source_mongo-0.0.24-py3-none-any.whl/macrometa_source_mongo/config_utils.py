from pathlib import Path
from singer import get_logger
from typing import Dict
import uuid

from macrometa_source_mongo.errors import InvalidAwaitTimeError, InvalidUpdateBufferSizeError
from macrometa_source_mongo.sync_strategies import change_streams

logger = get_logger('macrometa_source_mongo')

def validate_config(config: Dict) -> None:
    """
    Goes through the config and validate it
    Currently, only few parameters are validated
    Args:
        config: Dictionary of config to validate

    Returns: None
    Raises: InvalidUpdateBufferSizeError or InvalidAwaitTimeError
    """
    if 'update_buffer_size' in config:
        update_buffer_size = config['update_buffer_size']

        if not isinstance(update_buffer_size, int):
            raise InvalidUpdateBufferSizeError(update_buffer_size, 'Not integer')

        if not (change_streams.MIN_UPDATE_BUFFER_LENGTH <=
                update_buffer_size <= change_streams.MAX_UPDATE_BUFFER_LENGTH):
            raise InvalidUpdateBufferSizeError(
                update_buffer_size,
                f'Not in the range [{change_streams.MIN_UPDATE_BUFFER_LENGTH}..'
                f'{change_streams.MAX_UPDATE_BUFFER_LENGTH}]')

    if 'await_time_ms' in config:
        await_time_ms = config['await_time_ms']

        if not isinstance(await_time_ms, int):
            raise InvalidAwaitTimeError(await_time_ms, 'Not integer')

        if await_time_ms <= 0:
            raise InvalidAwaitTimeError(
                await_time_ms, 'time must be > 0')

def create_certficate_files(config: Dict) -> Dict:
    path_uuid = uuid.uuid4().hex
    try:
        if config.get('tls_ca_file'):
            path = f"/opt/mongo/{path_uuid}/ca.pem"
            ca_cert = Path(path)
            ca_cert.parent.mkdir(exist_ok=True, parents=True)
            ca_cert.write_text(create_ssl_string(config['tls_ca_file']))
            config['tls_ca_file'] = path
            logger.info(f"CA certificate file created at: {path}")

        if config.get('tls_certificate_key_file'):
            path = f"/opt/mongo/{path_uuid}/client.pem"
            client_cert = Path(path)
            client_cert.parent.mkdir(exist_ok=True, parents=True)
            client_cert.write_text(create_ssl_string(config['tls_certificate_key_file']))
            config['tls_certificate_key_file'] = path
            logger.info(f"Client certificate file created at: {path}")
    except Exception as e:
        logger.warn(f"Failed to create certificate: /opt/mongo/{path_uuid}/. {e}")
    return config

def delete_certficate_files(config: Dict) -> None:
    try:
        cert = None
        if config.get('tls_ca_file'):
            path = config['tls_ca_file']
            cert = Path(path)
            config['tls_ca_file'] = cert.read_text()
            cert.unlink()
            logger.info(f"CA certificate file deleted from: {path}")

        if config.get('tls_certificate_key_file'):
            path = config['tls_certificate_key_file']
            cert = Path(path)
            config['tls_certificate_key_file'] = cert.read_text()
            cert.unlink()
            logger.info(f"Client certificate file deleted from: {path}")

        if cert is not None:
            cert.parent.rmdir()
    except Exception as e:
        logger.warn(f"Failed to delete certificate: {e}")

def create_ssl_string(ssl_string: str) -> str:
    tls_certificate_key_list = []
    split_string = ssl_string.split("-----")
    if len(split_string) < 4:
        raise Exception("Invalid PEM format for certificate.")
    for i in range(len(split_string)):
        if((i % 2) == 1):
            tls_certificate_key_list.append("-----")
            tls_certificate_key_list.append(split_string[i])
            tls_certificate_key_list.append("-----")
        else:
            tls_certificate_key_list.append(split_string[i].replace(' ', '\n'))
    
    tls_certificate_key_file = ''.join(tls_certificate_key_list)
    return tls_certificate_key_file
