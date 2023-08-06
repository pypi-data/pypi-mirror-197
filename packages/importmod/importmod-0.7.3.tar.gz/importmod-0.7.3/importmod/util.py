import filecmp
import os
import shlex
import shutil
import subprocess
from shutil import rmtree, which

from portmod.globals import env
from portmodlib._deprecated.vfs import find_file
from portmodlib.masters import get_masters


def tr_patcher(filename: str):
    """Updates Plugins that target old versions of Tamriel Rebuilt"""
    tr_patcher_location = which("tr-patcher")
    if not tr_patcher_location:
        raise FileNotFoundError(
            "Cannot find executable tr-patcher. Please ensure it is in your PATH"
        )
    subprocess.check_call(shlex.split('{} "{}"'.format(tr_patcher_location, filename)))


def clean_plugin(file: str) -> bool:
    """
    Cleans dirty GMSTs and other issues in the given Plugin File

    The plugin's master files must have been installed prior to calling this function
    @param filename path to the plugin to be cleaned
    @return True if the plugin needed cleaning, False if there was no change
    """
    tes3cmd_location = which("tes3cmd")
    if not tes3cmd_location:
        raise FileNotFoundError(
            "Cannot find executable tes3cmd. Please ensure it is in your PATH"
        )

    tmp = os.path.join(env.TMP_DIR, "cleaning")
    os.makedirs(tmp, exist_ok=True)
    filename = os.path.basename(file)

    # Copy file to temp dir
    shutil.copy(file, tmp)

    for master in get_masters(file):
        # Note that tes3cmd requires that the name is exactly the same (including case)
        try:
            shutil.copy(find_file(master), os.path.join(tmp, master))
        except FileNotFoundError as error:
            found = False
            for localfile in os.listdir("."):
                if os.path.basename(localfile).lower() == master.lower():
                    found = True
                    shutil.copy(localfile, os.path.join(tmp, master))
            for localfile in os.listdir(os.path.dirname(file)):
                if os.path.basename(localfile).lower() == master.lower():
                    found = True
                    shutil.copy(
                        os.path.join(os.path.dirname(file), localfile),
                        os.path.join(tmp, master),
                    )

            if not found:
                raise error

    olddir = os.getcwd()
    os.chdir(tmp)
    subprocess.check_call(
        shlex.split('{} clean "{}"'.format(tes3cmd_location, filename))
    )
    os.chdir(olddir)

    original = os.path.join(tmp, filename)
    new = os.path.join(tmp, "Clean_" + filename)

    if not os.path.exists(new) or filecmp.cmp(original, new):
        rmtree(tmp)
        return False

    print("Replacing original with cleaned file...")
    shutil.copy(new, file)
    rmtree(tmp)
    return True
