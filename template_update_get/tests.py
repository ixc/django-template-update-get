try:  # Python 2
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser
from django.test import TestCase
from django.test.client import RequestFactory
from django.template import Template, Context


def render(content, url, context):
    request = RequestFactory().get(url)
    if not context:
        context = {}
    context['request'] = request
    t = Template('{% load template_update_get_tags %}' + content)
    c = Context(context)
    rendered = t.render(c)
    return HTMLParser().unescape(rendered)


class TemplateUpdateGetTests(TestCase):
    def test_can_assign_a_value(self):
        self.assertEqual(
            render(
                content='{% update_GET foo = "blah" %}',
                url='/',
                context={'foo': 'bar'}
            ),
            'bar=blah',
        )

    def test_can_assign_a_value_and_update_the_url(self):
        self.assertEqual(
            render(
                content='{% update_GET foo = "blah" %}',
                url='/?woz=zum',
                context={'foo': 'bar'}
            ),
            'woz=zum&bar=blah',
        )

    def test_can_add_values_to_url(self):
        self.assertEqual(
            render(
                content='{% update_GET foo += "blah" %}',
                url='/?bar=grub',
                context={'foo': 'bar'}
            ),
            'bar=grub&bar=blah',
        )

    def test_can_remove_values_from_url(self):
        self.assertEqual(
            render(
                content='{% update_GET foo -= "blah" %}',
                url='/?bar=grub&bar=blah',
                context={'foo': 'bar'}
            ),
            'bar=grub',
        )

    def test_can_remove_all_values_from_url(self):
        self.assertEqual(
            render(
                content='{% update_GET foo = None %}',
                url='/?bar=grub&bar=blah',
                context={'foo': 'bar'}
            ),
            '',
        )
