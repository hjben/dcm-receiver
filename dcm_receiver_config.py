"""
In this module, a configuration of dicom-receiving service could be defined.

Functions:
    - get_receiver_cfg: provide receiver_cfg object.
"""
import os

_receiver_cfg = dict(
    PRJ_ABS_PATH = os.path.dirname(os.path.abspath(__file__)),
    AE_TITLE = 'dcm_receiver',

    HOST = '0.0.0.0', # target host to open
    IP = '127.0.0.1', # external IP for receiver (to be changed)
    PORT = 11112,

    LOG_FILE_NAME = 'receiver_log',
    TEST_DCM_SOP_ID = '1.2.826.0.1.3680043.8.1055.1.20111103112244831.30826609.78057758' # SOP_INSTANCE_ID of health-check dcm
)

def get_receiver_cfg():
    """
        Returns _receiver_cfg defined above.

        Parameters
        ----------
        None

        Returns
        -------
        Dictionary
            A dictionary object with receiver_cfg.
    """
    return _receiver_cfg

if __name__=="__main__":
    print(get_receiver_cfg())