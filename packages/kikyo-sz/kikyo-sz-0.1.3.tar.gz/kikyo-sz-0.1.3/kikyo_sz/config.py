from kikyo import Kikyo

from kikyo_sz.oss import FileSysBasedOSS


def configure_kikyo(client: Kikyo):
    FileSysBasedOSS(client)
