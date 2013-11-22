import decimal

class BeansFieldMeta(type):
    pass


class BeansBaseField(object):
    __metaclass__ = BeansFieldMeta

    def __init__(self, name=None, required=False, read_only=False):
        self.name = name
        self.required = required
        self.read_only = read_only


class BuiltinTypeField(BeansBaseField): # abstract
    builtin = None 
    
    def build(self, v):
        return type(self).builtin(v)


class StringField(BuiltinTypeField):
    builtin = unicode

class IntegerField(BuiltinTypeField):
    builtin = int

class DecimalField(BuiltinTypeField):
    builtin = decimal.Decimal


# -----------------------------------------



class ReferenceField(BeansBaseField):
    def __init__(self, to, via_key=None, **kwargs):
        self.ref_to = to # TODO: check if real entity
        self.via_key = via_key
        return super(ReferenceField, self).__init__(**kwargs)
        
    def get_obj_id(self, v):
        obj_id = None
        if isinstance(v, dict):
            obj_id = int(v.get('id'))
        elif isinstance(v, int):
            obj_id = v
        elif isinstance(v, basestring):
            obj_id = int(v)
        return obj_id



# -----------------------------------------

class BeansEntityMeta(type):
    def __new__(cls, type_name, parents, dct):
        #print "cls=%s, name=%s, parents=%s, dct=%s\n" % (cls, name, parents, dct)
        dct['_beans_fields'] = [ ]
        dct['_beans_fields_by_name'] = { }
        for k in dct.keys():
            t = type(dct[k])
            if getattr(t, '__metaclass__', None) == BeansFieldMeta:
                if k not in dct['_beans_fields_by_name']:
                    field = dct[k]
                    del dct[k]
                    field.name = k
                    dct['_beans_fields'].append(field)
                    dct['_beans_fields_by_name'][k] = field
        return super(BeansEntityMeta, cls).__new__(cls, type_name, parents, dct)


class Entity(object):
    __metaclass__ = BeansEntityMeta

    def __init__(self, obj_id=None, **kwargs):
        self._beans_obj_id = obj_id
        self._beans_ref_getter = { }

        # setting the obj_id means sync from remote
        if not obj_id:
            # only apply required and read_only fields to objects instantiated by the users

            # handle required fields
            for f in type(self)._beans_fields:
                if f.required and (f.name not in kwargs):
                    raise ValueError, "Missing required field %s" % f.name

            # handle read_only fields
            for f in type(self)._beans_fields:
                if f.read_only and (f.name in kwargs):
                    raise ValueError, "Attempt to set read_only field %s" % f.name
        
        # do assignment
        for f in type(self)._beans_fields:
            if f.name in kwargs:
                setattr(self, f.name, kwargs[f.name])

    def __getattr__(self, name):
        if name in self._beans_ref_getter:
            g = self._beans_ref_getter.get(name)
            return g()    

    @property
    def id(self):
        return self._beans_obj_id

    @classmethod
    def build_from_dict(cls, data):
        obj_id = data['id']
        ck = { } # constructor kwargs

        # init non-ref
        for f in cls._beans_fields:
            if isinstance(f, BuiltinTypeField):
                if f.name in data:
                    ck[f.name] = f.build(data[f.name])

        # instantiate first
        obj = cls(obj_id, **ck)  
        return obj


    @classmethod
    def attach_refs(cls, obj, data={}, api_client=None, LookupClass=None):
        if not LookupClass:
            return
        if not api_client:
            return
        for f in cls._beans_fields:
            if isinstance(f, ReferenceField):
                if f.via_key in data:
                    v = data[f.via_key]
                    to_obj_id = f.get_obj_id(v)
                    ref_to = f.ref_to
                    ref_fn = lambda: api_client.execute(LookupClass(ref_to, to_obj_id))
                    obj._beans_ref_getter[f.name] = ref_fn

