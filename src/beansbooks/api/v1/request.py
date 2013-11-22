from beansbooks.entities import *

class Lookup(object):
    METHOD = 'POST'
    URL_PATH = '/%(entity_name)s/Lookup'

    def __init__(self, entity, obj_id):
        self.entity = entity
        self.obj_id = obj_id

    @property
    def headers(self):
        return { 'Content-Type': 'application/json' }

    @property
    def content(self):
        d = { 'id': self.obj_id }
        return d

    def url_path(self, prefix=''):
        path = self.__class__.URL_PATH
        url_path_data = { 'entity_name': self.entity.Meta.entity_name }
        path = path % url_path_data
        url = prefix + path
        return url

    def handle_response_data(self, data):
        obj = None
        if self.entity.Meta.entity_response_data_key in data:
            # build entity from data
            ed = data.get(self.entity.Meta.entity_response_data_key)
            obj_id = ed['id']
            if int(obj_id) == int(self.obj_id):
                obj = self.entity.build_from_dict(ed) 
        return obj

