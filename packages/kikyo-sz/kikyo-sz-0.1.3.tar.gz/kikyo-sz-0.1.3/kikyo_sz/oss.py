import io
from typing import Any

from kikyo import Kikyo
from kikyo.oss import OSS, Bucket
from requests_toolbelt.sessions import BaseUrlSession


class FileSysBasedOSS(OSS):
    def __init__(self, client: Kikyo):
        settings = client.settings.deep('filesys-oss')

        if not settings:
            return

        self.client = client
        self.bucket_prefix = settings.get('bucket_prefix', default='')
        self.endpoint: str = settings['endpoint']
        if not self.endpoint.startswith('http//') and not self.endpoint.startswith('https://'):
            self.endpoint = f'http://{self.endpoint}'
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'
        self.session = BaseUrlSession(self.endpoint)
        client.add_component('filesys_oss', self)

    def bucket(self, name: str) -> Bucket:
        if name.startswith(self.bucket_prefix):
            bucket_name = name
        else:
            bucket_name = f'{self.bucket_prefix}{name}'

        return FileSysBucket(bucket_name, self)


class FileSysBucket(Bucket):
    def __init__(self, name: str, oss: FileSysBasedOSS):
        self._name = name
        self._file_sys_endpoint = oss.endpoint
        self._session = oss.session

    def get_object_link(self, key: str) -> str:
        return f'{self._file_sys_endpoint}{self._name}/{key}'

    def put_object(self, key: str, data: Any) -> str:
        _data = None
        _length = None
        if isinstance(data, bytes):
            _length = len(data)
            _data = io.BytesIO(data)
        else:
            raise RuntimeError(f'Unsupported data type: {type(data)}')

        resp = self._session.post(f'{self._name}/{key}', data=_data)
        resp.raise_for_status()

        return self.get_object_link(key)

    def get_object(self, key: str) -> Any:
        resp = self._session.get(f'{self._name}/{key}')
        resp.raise_for_status()
        return resp.content
