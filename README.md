# django-template-update-get

Adds an `update_GET` template tag that allows you to substitute parameters into the current
request's GET parameters. This is often useful when updating params for search filters and
pagination without losing the current set.

## Installation

```bash
pip install django-template-update-get
```

## Usage

Add `'template_update_get'` to `INSTALLED_APPS`.

Use the template tag with

```html
{% load template_update_get_tags %}

<a href="?{% update_GET attr1 += value1 attr2 -= value2 attr3 = value3 %}">foo</a>
```

This:

- adds value1 to (the list of values in) attr1,
- removes value2 from (the list of values in) attr2,
- sets attr3 to value3.

and then returns a urlencoded GET string.

Allowed values are:

- vars that resolve to strings
- strings, in quotes
- lists of strings
- None (without quotes)

If an attribute is set to None or an empty list, the GET parameter is removed.
