import decimal

# TODO: FIXME: Needs a lots of test cases

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
    
    def from_remote(self, parent, v, api_client=None, LookupClass=None):
        return type(self).builtin(v)

    def to_remote(self, v):
        return v


class StringField(BuiltinTypeField):
    builtin = unicode

class IntegerField(BuiltinTypeField):
    builtin = int

class DecimalField(BuiltinTypeField):
    builtin = decimal.Decimal


# -----------------------------------------



class ReferenceField(BeansBaseField):
    def __init__(self, to=None, via_key=None, **kwargs):
        self.ref_to = to 
        self.via_key = via_key
        return super(ReferenceField, self).__init__(**kwargs)

    def get_obj_id(self, v):
        obj_id = None
        if isinstance(v, dict):
            obj_id_str = v.get('id')
            if obj_id_str is not None:
                obj_id = int(obj_id_str)
        elif isinstance(v, int):
            obj_id = v
        elif isinstance(v, basestring):
            obj_id = int(v)
        return obj_id

    def from_remote(self, parent, v, api_client=None, LookupClass=None):
        if not v:
            return None
        ref_fn = None
        to_obj_id = self.get_obj_id(v)
        ref_to = self.ref_to
        if self.ref_to == "self":
            ref_to = parent
        ref_fn = lambda: api_client.execute(LookupClass(ref_to, to_obj_id))
        return ref_fn

    def to_remote(self, v):
        return v
        


class ArrayField(BuiltinTypeField):
    def __init__(self, entity, **kwargs):
        self.entity = entity
        return super(ArrayField, self).__init__(**kwargs)
    
    def from_remote(self, parent, v, api_client=None, LookupClass=None):
        if not v:
            return
        nv = [ ]
        for ed in v:
            e = self.entity.build_from_dict(ed, api_client=api_client, LookupClass=LookupClass)
            nv.append(e)
        return nv

    def to_remote(self, v):
        return v
        



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

    def _set_id(self, new_id):
        self._beans_obj_id = new_id

    @property
    def id(self):
        return self._beans_obj_id

    @classmethod
    def build_from_dict(cls, data, api_client=None, LookupClass=None):
        obj_id = data['id']
        ck = { } # constructor kwargs

        ref_getters = { }
        for f in cls._beans_fields:
            dvk = f.name
            if hasattr(f, 'via_key'): # TODO: this is tied to the ReferenceField
                dvk = f.via_key
            if dvk in data:
                fv = f.from_remote(cls, data[dvk], api_client=api_client, LookupClass=LookupClass)
                if hasattr(fv, '__call__'): 
                    ref_getters[f.name] = fv
                else:
                    # non-ref
                    ck[f.name] = fv

        # instantiate first
        obj = cls(obj_id, **ck)  

        # attach refs
        for k in ref_getters.keys():
            obj._beans_ref_getter[k] = ref_getters.get(k)

        return obj

    @classmethod
    def fields_as_dict(cls, obj):
        data = { }
        for fk in cls._beans_fields_by_name.keys():
            f = cls._beans_fields_by_name[fk]
            if f.required:
                data[fk] = getattr(obj, fk, None)
            else:
                v = getattr(obj, fk, None) 
                if v is not None: 
                    data[fk] 
        return data


