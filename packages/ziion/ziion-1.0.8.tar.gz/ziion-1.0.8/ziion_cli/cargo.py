import os
import sys
import shutil
import gzip
import urllib.request
import subprocess
import platform
from packaging import version
import ziion_cli.dispatcher
import ziion_cli.utils

from ziion_cli.constants import (
    CARGO_ARTIFACTS_DIR,
    CARGO_DIR,
    S3_BUCKET_URL,
    CARGO_AMD_FOLDER_S3,
    CARGO_ARM_FOLDER_S3
)


def installed_versions():
    output = subprocess.check_output(["cargo", "install", "--list"])
    return ziion_cli.utils.parse_str_to_dict(output.decode("utf-8"))


def list_packages_to_be_updated(s3_packages_list, local_packages_list):
    packages_to_update = []
    print("\n{:<30} {:<15} {:<15} {:<18}".format(
        'Package', 'Installed', 'Latest', 'Need update'))
    print("-"*75)
    for package in s3_packages_list:
        if package not in local_packages_list:
            print("{:<30} {:<15} {:<18} {:<15}".format(
                package, " No ", s3_packages_list[package], " No "))
            packages_to_update.append(package)
        elif (package in local_packages_list) and (version.parse(s3_packages_list[package]) == version.parse(local_packages_list[package])):
            print("{:<30} {:<15} {:<18} {:<15}".format(
                package, local_packages_list[package], s3_packages_list[package], " No "))
        elif version.parse(s3_packages_list[package]) > version.parse(local_packages_list[package]):
            print("{:<30} {:<15} {:<18} {:<15}".format(
                package, local_packages_list[package], s3_packages_list[package], " Yes "))
            packages_to_update.append(package)
    print("\n")
    return packages_to_update


def update_necessary_packages(s3_packages_list, local_packages_list):
    packages = list_packages_to_be_updated(
        s3_packages_list, local_packages_list)
    if platform.machine() == 'x86_64':
        s3_folder = CARGO_AMD_FOLDER_S3
    elif platform.machine() == 'aarch64':
        s3_folder = CARGO_ARM_FOLDER_S3
    for package in packages:
        url = S3_BUCKET_URL + s3_folder + package + ".gz"
        try:
            urllib.request.urlretrieve(url, "/tmp/" + package + ".gz")
        except urllib.error.HTTPError as e:
            print("ERROR:" + package +
                  " could not be updated correctly. " + e.reason)
            sys.exit()
        with gzip.open("/tmp/" + package + ".gz", "rb") as f_in, open(CARGO_ARTIFACTS_DIR.joinpath(package), "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove("/tmp/" + package + ".gz")
        os.chmod(CARGO_ARTIFACTS_DIR.joinpath(package), 0o755)
        print(package + " updated successfully.")
    if packages:
        print("Download .crates.toml")
        url = S3_BUCKET_URL + s3_folder + ".crates.toml"
        try:
            urllib.request.urlretrieve(url, str(CARGO_DIR) + "/.crates.toml")
        except urllib.error.HTTPError as e:
            print("ERROR: .crates.toml could not be updated correctly. " + e.reason)
            sys.exit()
    print("\n")
