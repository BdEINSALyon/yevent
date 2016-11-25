import json

from Crypto.Cipher import XOR
import base64

from django.conf import settings


def _cipher():
    return XOR.new(settings.SECRET_KEY[:16])


def encrypt(data):
    return base64.b64encode(_cipher().encrypt(json.dumps(data))).decode("utf-8")


def decrypt(data):
    return json.loads(_cipher().decrypt(base64.b64decode(data)).decode('utf-8'))