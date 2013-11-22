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


class String(BuiltinTypeField):
    builtin = unicode

class Integer(BuiltinTypeField):
    builtin = int

class Decimal(BuiltinTypeField):
    builtin = decimal.Decimal




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
                    field.name = k
                    dct['_beans_fields'].append(field)
                    dct['_beans_fields_by_name'][k] = field
        return super(BeansEntityMeta, cls).__new__(cls, type_name, parents, dct)


class Entity(object):
    __metaclass__ = BeansEntityMeta

    def __init__(self, obj_id=None, **kwargs):
        self._beans_obj_id = obj_id

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

    @property
    def id(self):
        return self._beans_obj_id

    @classmethod
    def build_from_dict(cls, data):
        obj_id = data['id']
        ck = { } # constructor kwargs
        for f in cls._beans_fields:
            if f.name in data:
                ck[f.name] = f.build(data[f.name])

        return cls(obj_id, **ck)
        





