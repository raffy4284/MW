import datetime

class SerializerMixin(object):
  def __serialize__(self, exclude_list=list()):
    dictionary = {}
    for c in self._meta.get_fields_with_model():
      if c[0].name not in exclude_list:
        attr = getattr(self, c[0].name)
        if type(attr) is datetime.date:
          attr = attr.isoformat() 
        dictionary[c[0].name] = attr 
    return dictionary

