import json
from dataclasses import fields
from distutils.version import StrictVersion

import pkg_resources
import requests

from mstuff.http import http_get


def warn_if_old(mod_name):

    resp = http_get(f"https://pypi.org/project/{mod_name}", status_checker=None)
    if resp.status_code == 404:
        print(f"package {mod_name} does not yet exist?")
        return

    try:
        this_version = pkg_resources.get_distribution(mod_name).version
    except pkg_resources.DistributionNotFound:
        this_version = None


    # https://stackoverflow.com/a/27239645/6596010
    def versions(package_name):
        url = "https://pypi.org/pypi/%s/json" % (package_name,)
        data = json.loads(requests.get(url).text)
        versions = list(data["releases"].keys())
        versions.sort(key=StrictVersion)
        return versions


    online_versions = versions(mod_name)
    latest_version = online_versions[len(online_versions) - 1]
    if this_version != latest_version:
        print(
            f"WARNING: You are using {mod_name} {this_version} but the latest version is {latest_version}. In the terminal use `python -m pip install {mod_name} --upgrade` to update."
        )




# https://stackoverflow.com/questions/68417319/initialize-python-dataclass-from-dictionary
def class_from_args(cls, d):
    field_set = {f.name for f in fields(cls) if f.init}
    filtered_arg_dict = {k: v for k, v in d.items() if k in field_set}
    return cls(**filtered_arg_dict)
