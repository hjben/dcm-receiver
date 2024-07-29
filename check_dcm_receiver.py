"""
With this module, you could manage a dicom-receiving service which contains checking, killing, and re-running.

Functions:
    - check_receiver_health: Check the receiver process is alive.
    - kill_receiver_health: Find the receiver processes and kill them.
    - run_receiver: Run the receiver process in background.
"""
import os
import subprocess

from dcm_receiver_config import get_receiver_cfg

receiver_cfg = get_receiver_cfg()

def check_receiver_health():
    """
        Check the dcm_receiver.py process is alive.

        Parameters
        ----------
        None

        Returns
        -------
        Boolean
            True if the dcm_receiver.py process is alive, False otherwise.
    """
    result = subprocess.run(f"python -m pynetdicom storescu {receiver_cfg['IP']} {receiver_cfg['PORT']} '{os.path.join(receiver_cfg['PRJ_ABS_PATH'], 'test_' + receiver_cfg['TEST_DCM_SOP_ID'] + '.dcm')}' -v -cx", capture_output=True, text=True, shell=True)

    if (result.stdout + '\n' + result.stderr).find('Success') < 0: # if test send failed
        return False
    
    return True

def kill_receiver_process():
    """
        Find precesses with dcm_receiver.py file and kill them.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    for process in [line.split(' ')[1] for line in subprocess.run("ps -ef | grep dcm_receiver.py", capture_output=True, text=True, shell=True).stdout.split('\n') if not line.find(os.path.join(receiver_cfg['PRJ_ABS_PATH'], 'receive_dcm', 'dcm_receiver.py')) < 0]:
        subprocess.run(f"kill -9 {process}", shell=True)

def run_receiver():
    """
        Run dcm_receiver.py in background.

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    subprocess.run(f"nohup python -u {os.path.join(receiver_cfg['PRJ_ABS_PATH'], 'dcm_receiver.py')} >> {os.path.join(receiver_cfg['PRJ_ABS_PATH'], receiver_cfg['LOG_FILE_NAME'] + '.out')} &", shell=True)

if __name__=="__main__":
    if not check_receiver_health():
        print("Receiver is not healthy, Re-running receiver process..")
        kill_receiver_process()
        run_receiver()
    else:
        print("Receiver is running and healthy.")
