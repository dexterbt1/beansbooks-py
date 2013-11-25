
class Lookup(object):
    METHOD = 'POST'
    URL_PATH = '%(entity_url_path)s/Lookup'

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
        url_path_data = { 'entity_url_path': self.entity.Meta.entity_url_path }
        path = path % url_path_data
        url = prefix + path
        return url

    def handle_response_data(self, client, data):
        obj = None
        if self.entity.Meta.entity_lookup_data_key in data:
            # build entity from data
            ed = data.get(self.entity.Meta.entity_lookup_data_key)
            obj_id = ed['id']
            if int(obj_id) == int(self.obj_id):
                obj = self.entity.build_from_dict(ed) 
                self.entity.attach_refs(obj, data=ed, api_client=client, LookupClass=type(self))
                
        return obj




class Search(object):
    METHOD = 'POST'
    URL_PATH = '%(entity_url_path)s/Search'

    OLDEST = 'oldest'
    NEWEST = 'newest'


    class Page(object):

        def __init__(self, client, items, total_results=None, page=None, pages=None, next_page_search=None):
            self.client = client
            self.items = items
            self.total_results = total_results
            self.page = page
            self.pages = pages
            self.next_page_search = next_page_search

        def has_next_page(self):
            return (self.next_page_search is not None)

        def next_page(self):
            return self.client.execute(self.next_page_search)
        
    def __init__(self, entity, sort_by=NEWEST, page=0, page_size=50, **kwargs):
        self.entity = entity
        self.sort_by = sort_by
        self.page = page
        self.page_size = page_size
        self.params = kwargs

    @property
    def headers(self):
        return { 'Content-Type': 'application/json' }

    @property
    def content(self):
        d = { 
            'sort_by': self.sort_by,
            'page': self.page,
            'page_size': self.page_size,
            }
        d.update(self.params)
        return d

    def url_path(self, prefix=''):
        path = self.__class__.URL_PATH
        url_path_data = { 'entity_url_path': self.entity.Meta.entity_url_path }
        path = path % url_path_data
        url = prefix + path
        return url

    def handle_response_data(self, client, data):
        page = None
        if self.entity.Meta.entity_search_data_key in data:
            # build entity from data
            raw_entity_list = data.get(self.entity.Meta.entity_search_data_key)
            entity_list = [ ]
            for raw_e in raw_entity_list:
                rd = { self.entity.Meta.entity_lookup_data_key: raw_e }
                lookup = Lookup(self.entity, raw_e.get('id'))
                # simulate as if the entity came from a Lookup request
                e = lookup.handle_response_data(client, rd)
                entity_list.append(e)
            current_page = int(data.get('page'))
            current_pages = int(data.get('pages')) 
            next_page = None
            if current_page < (current_pages-1):
                next_page = current_page + 1
            params = self.params
            page = Search.Page(
                client,
                entity_list, 
                total_results=int(data.get('total_results')), 
                page=current_page,
                pages=current_pages,
                next_page_search=type(self)(self.entity, sort_by=self.sort_by, page=next_page, page_size=self.page_size, **params),
                )
        return page

