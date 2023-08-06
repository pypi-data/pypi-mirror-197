import os


def get_ecc204_ta010_xsd_path():
    return os.path.join(os.path.dirname(__file__), "data", "cryptoauth", "ECC204_TA010_Config_1.0.xsd")


__all__ = ['get_ecc204_ta010_xsd_path']
