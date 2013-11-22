import json
import requests as pyrequests


class AuthAccess(object):

    def __init__(self, uid=None, key=None, expiration=None):
        self.uid = uid
        self.key = key
        self.expiration = expiration

    @property
    def request_dict(self):
        return {
            'auth_uid': self.uid,
            'auth_key': self.key,
            'auth_expiration': self.expiration,
            }



class Client(object):

    # TODO: FIXME: determine yet where to best place these exception classes
    class TransportError(Exception): pass
    class AuthError(Exception): pass
    class ConfigError(Exception): pass
    class RequestError(Exception): pass

    def __init__(self, endpoint, auth=None):
        self.endpoint = endpoint
        self.auth = auth

    def execute(self, req):
        content = req.content
        if self.auth:
            content.update(self.auth.request_dict)
        full_url = req.url_path(prefix=self.endpoint)
        req_body = json.dumps(content)
        pyreq = pyrequests.Request(
            req.METHOD, 
            full_url,
            data=req_body,
            headers=req.headers,
            )
        print "Request: %s %s: %s" % (req.METHOD, full_url, req_body)
        pyreq_prepped = pyreq.prepare()
        s = pyrequests.Session()

        response = s.send(pyreq_prepped)

        print "Response: code=%s: body: %s" % (response.status_code, response.content)

        if response.status_code != pyrequests.codes.ok:
            raise Client.TransportError, "Status %s" % response.status_code 

        rd = json.loads(response.content)
        if not rd['success']:
            if len(rd['auth_error']) > 0: raise Client.AuthError, rd['auth_error']
            if len(rd['config_error']) > 0: raise Client.ConfigError, rd['config_error']
            raise Client.RequestError, rd['error']

        return req.handle_response_data(self, rd['data'])
        
