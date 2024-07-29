"""
This module has a dicom sender to test a receiver.

Functions:
    - dcm_send: send a dcm file to the target receiver.
"""
import os, glob
import subprocess

from dcm_receiver_config import get_receiver_cfg

receiver_cfg = get_receiver_cfg()
tmp_receiver_ip = '127.0.0.1' # external IP of receiver

def dcm_send(dcm_path: str):
    """
        Send a dcm file to the target receiver and print the send result.

        Parameters
        ----------
        dcm_path: String
            dcm file path to send (required)

        Returns
        -------
        None
    """
    print(f"Try sending DCM file: {dcm_path}")
    result = subprocess.run(f"python -m pynetdicom storescu {tmp_receiver_ip} {receiver_cfg['PORT']} '{dcm_path}' -v -cx", capture_output=True, text=True, shell=True)

    if (result.stdout + '\n' + result.stderr).find('Success') < 0:
        print('DCM send failed')
        print(result.stdout)
        print(result.stderr)
    else:
        print('DCM send successed')

if __name__=="__main__":
    dcm_send("./dummy_dcm/send_sample.dcm")