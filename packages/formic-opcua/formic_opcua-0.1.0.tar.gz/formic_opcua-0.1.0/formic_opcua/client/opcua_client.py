# Copyright Formic Technologies 2023
import logging
import posixpath
import time
import warnings
from typing import Any, Dict, List

from asyncua.sync import Client, ThreadLoopNotRunning
from asyncua.ua.uatypes import VariantType

from formic_opcua.core import convert_type, parse_settings

logger = logging.getLogger(__name__)
warnings.simplefilter('error')


class OpcuaClient:
    def __init__(self, server_config_file: str) -> None:
        logger.debug('Configuring client.')
        self._server_config_file = server_config_file
        self.config = parse_settings(self._server_config_file)
        self._client_map: Dict[str, tuple] = dict()
        self._url = self.config['server_settings']['url']
        self._uri = self.config['server_settings']['uri']
        self._idx = -1
        self._node_path_list: List[str] = []
        self._client = Client(url=self._url)
        self._has_connected = False
        logger.info(f'Client created with url: {self._url}, and uri: {self._uri}')

    def __enter__(self):
        self._connect()
        self._establish_server_structure()
        return self

    def __exit__(self, *args) -> None:
        self._disconnect()

    def _connect(self):
        try:
            if self._test_server_connection():
                logger.info('_connect called but there is a connection to the server.')
                self._has_connected = True
                return
            if self._disconnect():
                self._client = Client(url=self._url)
            logger.info('Connecting...')
            self._client.connect()
            logger.info('Connected...')
            self._has_connected = True
        except (ConnectionRefusedError, ConnectionError, RuntimeError, RuntimeWarning):
            logger.error(
                f'Unable to connect to server. Client expects server to have url: {self._url} and uri: {self._uri}. '
                f'Server is not running or the configs are not matched with client.'
            )
            self._has_connected = False

    def _disconnect(self) -> bool:
        logger.info('Cleaning up client.')
        try:
            self._client.disconnect()
            return True
        except (RuntimeError, ConnectionError, ThreadLoopNotRunning):
            logger.warning('Tried to disconnect but there is no connection.')
            return False

    def _establish_server_structure(self) -> None:
        try:
            self._idx = self._client.get_namespace_index(self._uri)
            logger.info(f'Namespace index = {self._idx}')
            logger.info(f'Mapping namespace using {self._server_config_file}')
            for child_name, root in self.config['opcua_nodes'].items():
                self._map_client(parent_path=child_name, root=root)
            self._node_path_list = list(self._client_map.keys())
            logger.info(f'All nodes successfully mapped: {self._node_path_list}')
        except (AttributeError, ConnectionError, RuntimeWarning, ThreadLoopNotRunning):
            logger.error(f'Unable to map opcua nodes from {self._server_config_file}')

    def _map_client(self, parent_path: str, root: dict) -> None:
        if self._is_leaf(root):
            identifier = self._identifier_from_string(parent_path)
            var = self._client.nodes.root.get_child(identifier)
            self._client_map[parent_path] = (var, getattr(VariantType, root['type']))
            return None

        original_parent_path_length = len(parent_path)

        for child_root_name, child_root in root.items():
            parent_path = posixpath.join(parent_path, child_root_name)
            if original_parent_path_length == 0:
                parent_path = parent_path[1:]

            self._map_client(parent_path, child_root)
            parent_path = parent_path[:original_parent_path_length]

    @staticmethod
    def _is_leaf(root: dict) -> bool:
        if 'initial_value' in root:
            return True
        return False

    def _identifier_from_string(self, path: str) -> List[str]:
        identifier = [f'{self._idx}:{path_part}' for path_part in path.split('/')]
        return ['0:Objects'] + identifier

    def _test_server_connection(self) -> bool:
        try:
            self._client.get_namespace_index(self._uri)
            return True
        except Exception as e:
            logger.warning(e)
            logger.warning('Failed server connectivity test.')
            return False

    def _write_helper(self, path: str, value: Any) -> bool:
        if self._has_connected:
            try:
                var, var_type = self._client_map[path]
            except KeyError:
                logger.warning(f'Unable to find {path} in client map {self._client_map}')
                return False
            try:
                value = convert_type(value=value, var_type=var_type)
            except (KeyError, TypeError):
                logger.warning(f'Unable to convert value {value} to variant type {var_type}')
                return False
            try:
                var.write_value(value, var_type)
                logger.info(f'Wrote value {value} of type {var_type} to {path}')
                return True
            except (ConnectionError, ThreadLoopNotRunning) as e:
                logger.warning(f'{e}')
                logger.warning(f'Unable to write value {value} of type {var_type} to {path}')
        else:
            logger.warning(f'No connection has been made to server. Cannot write value {value} to path {path}')
        return False

    def write(self, path: str, value: Any, reconnect_attempts: int = 0, reconnect_delay: float = 0) -> bool:
        total_write_attempts = reconnect_attempts + 1
        logger.info(f'Attempting to write value {value} to path {path}.')
        for write_attempt in range(total_write_attempts):
            logger.info(f'Starting {write_attempt + 1} / {total_write_attempts} write attempts.')
            if not self._has_connected:  # Write attempt has failed or client never connected.
                logger.info('Client has not connected to server. Attempting to connect.')
                self.__enter__()
            if self._write_helper(path=path, value=value):
                logger.info(f'Write attempt succeeded on {write_attempt + 1} / {total_write_attempts}.')
                return True
            else:
                logger.warning(f'Write attempt {write_attempt + 1} / {total_write_attempts} unsuccessful')
                self._has_connected = False

            if write_attempt < reconnect_attempts:
                logger.info(f'Waiting {reconnect_delay}s.')
                time.sleep(reconnect_delay)
        return False

    def _read_helper(self, path: str) -> Any:
        if self._has_connected:
            try:
                node = self._client_map[path][0]
            except (KeyError, IndexError):
                logger.warning(f'Unable to get node {path} from client map {self._client_map}')
                return None
            try:
                value = node.read_value()
                logger.info(f'Read value {value} from path {path}')
                return value
            except (ConnectionError, ThreadLoopNotRunning) as e:
                logger.warning(f'{e}')
                logger.warning(f'Unable to read node at {path}')
        else:
            logger.warning(f'No connection has been made to server. Cannot read node at path {path}')
        return None

    def read(self, path: str, reconnect_attempts: int = 0, reconnect_delay: float = 0) -> Any:
        total_read_attempts = reconnect_attempts + 1
        logger.info(f'Attempting to read path {path}.')
        for read_attempt in range(total_read_attempts):
            logger.info(f'Starting {read_attempt + 1} / {total_read_attempts} read attempts.')
            if not self._has_connected:  # Read attempt has failed or client never connected.
                logger.info('Client has not connected to server. Attempting to connect.')
                self.__enter__()
            value = self._read_helper(path=path)
            if value is not None:
                logger.info(f'Read attempt succeeded on {read_attempt + 1} / {total_read_attempts}.')
                logger.info(f'Value: {value}')
                return value
            else:
                logger.warning(f'Read attempt {read_attempt + 1} / {total_read_attempts} unsuccessful')
                self._has_connected = False

            if read_attempt < reconnect_attempts:
                logger.info(f'Waiting {reconnect_delay}s.')
                time.sleep(reconnect_delay)
        return None

    def read_all(self, reconnect_attempts: int = 0, reconnect_delay: float = 0) -> Dict[str, Any]:
        logger.info(f'Attempting to read all variables on server at uri: {self._uri} and url: {self._url}.')
        results = {}
        total_read_attempts = reconnect_attempts + 1
        for read_attempt in range(total_read_attempts):
            logger.info(f'Starting {read_attempt + 1}/{total_read_attempts} read attempts.')
            if not self._has_connected:  # Client has never successfully connected to the server
                logger.info('Client may not be connected to server. Attempting to connect.')
                self.__enter__()  # Creates a new client object and adjusts self._has_connected() appropriately
            if self._has_connected:  # In case self.__enter__() changed value to true by establishing a connection
                for path in self._node_path_list:
                    if path not in results:
                        value = self._read_helper(path)
                        if value is not None:
                            logger.info(
                                (
                                    f'Successfully read value: {value} for path: {path} on attempt {read_attempt + 1}/'
                                    + f'{total_read_attempts}.'
                                )
                            )
                            results[path] = value
                        else:
                            logger.warning(
                                (
                                    f'Unsuccessful read attempt for path {path} of read attempt {read_attempt + 1}/'
                                    + f'{total_read_attempts}.'
                                )
                            )
                            self._has_connected = False
            # Case where no connection was made at any point during reading all nodes.
            if len(self._node_path_list) == 0 or len(results) != len(self._node_path_list):
                # Either there was never a connection or there was a disconnect
                # while reading and only some results were read
                self._has_connected = False
            # Case where a non None vale has been read for all nodes.
            elif len(results) == len(self._node_path_list) and len(self._node_path_list) > 0:
                break
            if read_attempt < reconnect_attempts:
                logger.warning(
                    (
                        f'Unsuccessful connection attempt to server on read attempt {read_attempt + 1}/'
                        + f'{total_read_attempts}'
                    )
                )
                logger.info(f'Waiting {reconnect_delay}s.')
                time.sleep(reconnect_delay)
        logger.info(f'{results}')
        return results
