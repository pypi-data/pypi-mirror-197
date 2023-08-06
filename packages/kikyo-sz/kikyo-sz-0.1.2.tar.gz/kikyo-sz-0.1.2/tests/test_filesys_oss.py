from kikyo import configure_by_consul

from kikyo_sz.oss import FileSysBasedOSS


def test_upload():
    kikyo_client = configure_by_consul('http://consul.app.kdsec.org/v1/kv/kikyo-sz')
    bucket = kikyo_client.component(cls=FileSysBasedOSS).bucket('test')
    bucket.put_object('test.txt', b'123456')


def test_download():
    kikyo_client = configure_by_consul('http://consul.app.kdsec.org/v1/kv/kikyo-sz')
    bucket = kikyo_client.component(cls=FileSysBasedOSS).bucket('test')
    assert bucket.get_object('test.txt') == b'123456'

