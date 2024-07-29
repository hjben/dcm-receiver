"""
This module provides a class for a dicom-receiving service.

Classes:
    - Receiver: Run a dicom file receiver service, which is wating for a dcm-sending event and processing it.
"""
import os

from datetime import datetime
from pydicom.uid import JPEGLosslessSV1, JPEG2000Lossless
from pynetdicom import AE, StoragePresentationContexts, evt, DEFAULT_TRANSFER_SYNTAXES

from dcm_receiver_config import get_receiver_cfg

class Receiver:
    """
    Run a dicom file receiver service, which is wating for a dcm-send event and processing it.

    Public attributes:
        - receiver_cfg: configurations read from dcm_receiver_config.py
    """
    def __init__(self):
        self.receiver_cfg = get_receiver_cfg()

    def handle_store(self, event):
        """
            Process the dcm-send event if it occurs. 

            Parameters
            ----------
            event: Object
                A dcm-send event

            Returns
            -------
            Hexadecimal
                Dummy number
        """
        ds = event.dataset
        ds.file_meta = event.file_meta

        if ds.SOPInstanceUID!=self.receiver_cfg['TEST_DCM_SOP_ID']:
            root_save_dir = os.path.join(self.receiver_cfg['PRJ_ABS_PATH'], 'received', datetime.now().strftime('%Y%m%d'))
            os.makedirs(root_save_dir, exist_ok=True)
            filename = os.path.join(root_save_dir, f"received_{ds.SOPInstanceUID}.dcm")
            print(f"Received DICOM file: {filename}")
            ds.save_as(filename)
        else:
            print("Test data received. Receiver health is OK.")

        return 0x0000
    
    def on_c_echo(self, event):
        return 0x0000
    
    def on_c_store(self, event):
        return 0x0000
    
    def receive_dicom_files_periodically(self):
        """
            Start a service waiting for dcm-send event.

            Parameters
            ----------
            None

            Returns
            -------
            None
        """
        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        ae = AE(self.receiver_cfg['AE_TITLE'])

        for context in StoragePresentationContexts:
            ae.add_supported_context(context.abstract_syntax, DEFAULT_TRANSFER_SYNTAXES + [JPEGLosslessSV1, JPEG2000Lossless])

        ae.on_c_echo = self.on_c_echo
        ae.on_c_store = self.on_c_store

        local_host = self.receiver_cfg['HOST']
        local_port = self.receiver_cfg['PORT']

        print("[*] host is.. {}".format(local_host))
        print("[*] port is.. {}".format(local_port))
        print("[*] Waiting.. ")

        ae.start_server((local_host, local_port), block=True, evt_handlers=handlers)

if __name__=="__main__":
    print("[*] Receiver started..")
    print(f"[*] Datetime: {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}")

    receiver = Receiver()
    receiver.receive_dicom_files_periodically()