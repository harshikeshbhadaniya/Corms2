from enum import Enum


class Gerrit(Enum):
    android = "https://android-review.googlesource.com"
    chromium = "https://chromium-review.googlesource.com"
    cloudera = "https://gerrit.cloudera.org"
    eclipse = "https://git.eclipse.org/r"
    gerrithub = "https://review.gerrithub.io"
    go = "https://go-review.googlesource.com"
    libreoffice = "https://gerrit.libreoffice.org"
    opencord = "https://gerrit.opencord.org"
    openstack = "https://review.openstack.org"
    unlegacy = "https://gerrit.unlegacy-android.org"
    qt = "https://codereview.qt-project.org"
    openbmc = "https://gerrit.openbmc-project.xyz"
    opendaylight = "https://git.opendaylight.org/gerrit"
    onap = "https://gerrit.onap.org/r"
    softwarefactory	= "https://softwarefactory-project.io/r"
    LineageOS = "https://review.lineageos.org"
    pixel = "https://gerrit.pixelexperience.org"
    FDio = "https://gerrit.fd.io/r"
    oransc = "https://gerrit.o-ran-sc.org/r"
    mano = "https://osm.etsi.org/gerrit"
    gerrit = "https://gerrit-review.googlesource.com"

    def __str__(self):
        return f"{self.name}"

