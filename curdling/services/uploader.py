from __future__ import absolute_import, print_function, unicode_literals
from .base import Service
from ..util import get_auth_info_from_url

import io
import os
import urllib3
import urlparse


class Uploader(Service):

    def __init__(self, *args, **kwargs):
        super(Uploader, self).__init__(*args, **kwargs)
        self.opener = urllib3.PoolManager()

    def handle(self, requester, requirement, sender_data):
        # Preparing the url to PUT the file
        path = sender_data.pop('path')
        server = sender_data.pop('server')
        package_name = os.path.basename(path)
        url = urlparse.urljoin(server, 'p/{0}'.format(package_name))

        # Sending the file to the server. Both `method` and `url` parameters
        # for calling `request_encode_body()` must be `str()` instances, not
        # unicode.
        contents = io.open(path, 'rb').read()
        self.opener.request_encode_body(
            b'PUT', bytes(url), {package_name: (package_name, contents)},
            headers=get_auth_info_from_url(url))
        return {'url': url}
