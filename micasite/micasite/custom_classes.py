import datetime

class SerializerMixin(object):
  def __serialize__(self, exclude_list=list()):
    dictionary = {}
    for c in self._meta.get_fields():
      if c.name not in exclude_list:
        attr = getattr(self, c.name)
        if type(attr) is datetime.date:
          attr = attr.isoformat() 
        dictionary[c.name] = attr 
    return dictionary

