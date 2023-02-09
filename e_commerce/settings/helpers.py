import re
from uuid import uuid4


DEFAULT_TYPE_FORMATTER = {
    "datetime": lambda val: val.strftime("%Y-%m-%d %H:%M:%S") if val else val,
    "Decimal": lambda val: float(val)
}


email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def check_email(email):
    if(re.search(email_regex, email)):
        #print("Valid Email")
        return True
    else:
        #print("Invalid Email")
        return False


class BaseSerializer(object):
    fields = None
    fields_format = {}
    fields_by_type = DEFAULT_TYPE_FORMATTER

    def serialize(self):
        if not self.fields:
            raise NotImplementedError("Please add a fields attr to your class")
        data = {}
        for f in self.fields:
            value = getattr(self, f)
            type_str = type(value).__name__
            type_formatter = self.fields_by_type.get(type_str, None)
            field_formatter = self.fields_format.get(f, None)
            if type_formatter:
                formatter = type_formatter
            elif field_formatter:
                formatter = field_formatter
            else:
                def formatter(x): return x
            data[f] = formatter(value) if formatter else value
        return data



def remove_empty_from_dict(d):
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d


def create_filename(curr_filename):
    ext = curr_filename.rsplit(".", 1)[1].lower()
    return "%s.%s" % (str(uuid4()), ext)
