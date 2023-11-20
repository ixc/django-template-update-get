import re
from django import template
from django.http import QueryDict
from django.utils.encoding import force_str


register = template.Library()


@register.tag(name="update_GET")
def do_update_get(parser, token):
    try:
        args = token.split_contents()[1:]
        triples = list(_chunks(args, 3))
        if triples and len(triples[-1]) != 3:
            raise template.TemplateSyntaxError(
                "%r tag requires arguments in groups of three (op, attr, value)."
                % token.contents.split()[0]
            )
        ops = set([t[1] for t in triples])
        if not ops <= {"+=", "-=", "="}:
            raise template.TemplateSyntaxError(
                "The only allowed operators are '+=', '-=' and '='. You have used %s"
                % ", ".join(ops)
            )

    except ValueError:
        return UpdateGetNode()

    return UpdateGetNode(triples)


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


unencoded_ampersands_re = re.compile(r"&(?!(\w+|#\d+);)")


def fix_ampersands(value):
    """Returns given HTML with all unencoded ampersands encoded correctly."""
    return unencoded_ampersands_re.sub("&amp;", force_str(value))


class UpdateGetNode(template.Node):
    def __init__(self, triples=None):
        if triples is None:
            triples = []
        self.triples = [
            (template.Variable(attr), op, template.Variable(val))
            for attr, op, val in triples
        ]

    def render(self, context):
        try:
            params = context.get("request").GET.copy()
        except AttributeError:
            params = QueryDict("", mutable=True)

        for attr, op, val in self.triples:
            actual_attr = attr.resolve(context)

            try:
                actual_val = val.resolve(context)
            except:
                if val.var == "None":
                    actual_val = None
                else:
                    actual_val = val.var

            if actual_attr:
                if op == "=":
                    if actual_val is None or actual_val == []:
                        if actual_attr in params:
                            del params[actual_attr]
                    elif isinstance(actual_val, list):
                        params.setlist(actual_attr, actual_val)
                    else:
                        params[actual_attr] = str(actual_val)
                elif op == "+=":
                    if actual_val is None or actual_val == []:
                        if params.has_key(actual_attr):
                            del params[actual_attr]
                    elif isinstance(actual_val, list):
                        params.setlist(
                            actual_attr, params.getlist(actual_attr) + list(actual_val)
                        )
                    else:
                        params.appendlist(actual_attr, str(actual_val))
                elif op == "-=":
                    li = params.getlist(actual_attr)
                    if isinstance(actual_val, list):
                        for v in list(actual_val):
                            if v in li:
                                li.remove(v)
                        params.setlist(actual_attr, li)
                    else:
                        actual_val = str(actual_val)
                        if actual_val in li:
                            li.remove(actual_val)
                        params.setlist(actual_attr, li)

        return fix_ampersands(params.urlencode())
