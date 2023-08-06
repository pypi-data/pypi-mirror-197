import os
import uuid
from pathlib import Path
from endoscopie import utils
from endoscopie.logarithm import Logarithm

logger = Logarithm(__name__)


def make(images):
    metadata = utils.get_metadata(Path(f"{os.path.dirname(os.path.abspath(__file__))}/metadata/endoscopie-meta.json"))

    metadata["openstack"]["region"] = os.getenv("OS_REGION_NAME")
    metadata["openstack"]["auth"]["type"] = os.getenv("OS_AUTH_TYPE")
    metadata["openstack"]["auth"]["url"] = os.getenv("OS_AUTH_URL")
    metadata["openstack"]["credential"]["id"] = os.getenv("OS_APPLICATION_CREDENTIAL_ID")
    metadata["openstack"]["credential"]["secret"] = os.getenv("OS_APPLICATION_CREDENTIAL_SECRET")

    # with open(yaml_file) as file:
    #     images = yaml.load(file, Loader=yaml.FullLoader)

    servers = []
    for i in range(len(images["images"])):
        server = {
            "name": f'{images["images"][i]["osType"]}',
            "keypair": {
                "name": images["instance"]["keypair"]["name"]
            },
            "flavors": images["images"][i]["flavors"],
            "vpc": {
                "id": images["instance"]["vpc"]["id"],
                "subnet": images["instance"]["vpc"]["subnet"],
                "security_groups": images["instance"]["vpc"]["securityGroups"]
            },
            "block_device": {
                "uuid": images["images"][i]["id"],
                "source_type": "image",
                "volume_size": images["images"][i]["volumeSize"]
            },
            "image_id": images["images"][i]["id"],
            "image_name": images["images"][i]["name"],
            "os_type": images['images'][i]['osType'],
            "os_version": images['images'][i]['osVersion'],
            "os_user": images['images'][i]['osUser'],
            "user_script": {
                "path": images['images'][i]["userScript"]['path']
            # },
            # "assertThat": {
            #     "processes": images['images'][i]['assertThat']['processes'],
            #     "ports": images['images'][i]['assertThat']['ports']
                # "logs": images['images'][i]['assertThat']['logs'],
                # "files": images['images'][i]['assertThat']['files'],
                # "endpoint": {
                #     "url": images['images'][i]['assertThat']['endpoint']['url'],
                #     "id": images['images'][i]['assertThat']['endpoint']['id'],
                #     "password": images['images'][i]['assertThat']['endpoint']['password']
                # }
            }
        }

        servers.append(server)

    metadata["servers"] = servers

    logger.debug(metadata)

    return metadata
