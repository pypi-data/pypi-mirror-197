# This is replaced during release process.
__version_suffix__ = '159'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.22.17"
KUBECTL_SHA512 = {
    "linux": "fe9fb234653435f75f2de968914b64a1096eceb5014c45d4d1a678b781f3c00aa40420a7421f156daee50350a2b6f91e55a913854bea08d0d0f2c9e3788fe325",
    "darwin": "d5362f67b1e3730b00ced11be8ac5415d6a0ca7ea4211422530f71e28a2d944fd7fc76949c3fbf0babb72dce4f13be8c383acb20b2b96f63cf3c4442e0b8ec44",
}
STERN_VERSION = "1.19.0"
STERN_SHA256 = {
    "linux": "fcd71d777b6e998c6a4e97ba7c9c9bb34a105db1eb51637371782a0a4de3f0cd",
    "darwin": "18a42e08c5f995ffabb6100f3a57fe3c2e2b074ec14356912667eeeca950e849",
}
KUBELOGIN_VERSION = "v1.26.0"
KUBELOGIN_SHA256 = {
    "linux": "d75d0d1006530f14a502038325836097b5cc3c79b637619cf08cd0b4df5b3177",
    "darwin": "1086814f19fb713278044f275c006d3d111d11ca6d92f2348af7f3eff78eecf1",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
