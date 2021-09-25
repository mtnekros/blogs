# Multi Language Site with Django
## 1. SETUP LOCALE SETTINGS
* [ ] make the directory to where .po and .mo files should go (this is the LOCALE_PATHS)
    * [ ] $BASE_DIR/locale/
* [ ] add LOCALE_PATHS variable to settings.py
   ```python
  LOCALE_PATHS = [
      os.path.join(BASE_DIR, 'locale')
  ]
   ```
* [ ] add the supported LANGUAGES in the settings.py
   ```python
  LANGUAGES = (
      ('en', _('English')),
      ('ne', _('Nepali')),
  )
   ```
* [ ] add "django.middleware.locale.LocaleMiddleware" after common middleware in settings.py
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.locale.LocaleMiddleware', # <- Add this
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]
   ```
* [ ] wrap the urls patterns in the projets urls.py with i18n_patterns from django.conf.urls.i18n
   ```python
   from django.conf.urls.i18n import i18n_patterns
   urlpatterns = i18n_patterns(
       path('users', include('users.urls')),
       # other urls
       url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
       url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
       *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   )
   ```
    * Adding the middleware and wrapping the url paths with i18n_patterns will
      set the translation urls to be automatically handled
      For example: all nepali language page paths will have ne/ prefixed to them.
      (en for english)

## 2. ACTUAL TRANSLATION PART
* [ ] Let django know which texts should be translated
    * [ ] html:
        * load i18n tags with `{% load i18n %}` 
        * wrap every text that should be translated like
            * `{% trans 'text_to_be_translated' %}` or
            * `{% blocktrans %}text_to_be_translated{% endblocktrans %}`
    * [ ] py:
        * import gettext with
          `from django.utils.translation import gettext as _`
        * wrap every text that should be translated like this
          `_(text_to_be_translated)`
* [ ] run the command: `python manage.py makemessages -t ne`
  
  _Note: for makemessages & compilemessages command to work, you need to install GNU gettext utilities 
  in your computer_
      * _For linux users, gettext will usually be installed by default. If it isn't, you
      can install using the package manager of your choice._
      * _For windows users, read more at this [link](https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#gettext-on-windows) or download & install getext [here](https://mlocati.github.io/articles/gettext-iconv-windows.html)_
* [ ] edit the .po files
* [ ] compile and regenerate .mo file
    * [ ] Use this command: `python manage.py compilemessages`
* [ ] translations should work now after restarting the server

## Working the variables inside translation string in django template
Note that trans doesn't work properly with variables as expected.
If you have to translate, `{{ count }} lemons` and wrap it inside trans tag like
`{% trans "{{ count }} lemons" %}`, django will treat `{{ count }}` as a string.

From django documentation,
> It's not possible to mix a template variable inside a string within {% trans
> %}. If your translations require strings with variables (placeholders), use
> {% blocktrans %} instead.

If you want to translate strings that contain variables as a whole, you need to use
blocktrans tag. Contrarily to the trans tag, the blocktrans tag allows you to mark complex
sentences consisting of literals and variable content for translation by making
use of placeholders:
```htmldjango
{% blocktrans %}This string will have {{ value }} inside.{% endblocktrans %}
```
To translate a template expression – say, accessing object attributes or using
template filters – you need to bind the expression to a local variable for use
within the translation block. Examples:

```htmldjango
{% blocktrans with amount=article.price myvar=value|filter %}
That will cost $ {{ amount }}.
This will have {{ myvar }} inside.
{% endblocktrans %}
```

## Contextual markers: Translation for words that have different meaning in different context
The same word can have multiple translations based on different contexts. For
example, the word "May" can refer to a month name and to a verb. To enable the
translators to translate this word in two contexts, you can use
django.utils.translation.pgettext() function or the
django.utils.translation.npgettext() function if the string needs
pluralization.
```python
from django.utils.translation import pgettext

month = pgettext("month name", "May")
verb = pgettext("verb", "May")
```
They take a context string as the first variable which will appear in the .po
file as show below and same text will appear twice in the .po file given that
the context strings for them are different.

```po
msgctxt "month name"
msgid "May"
msgstr ""

msgctxt "verb"
msgid "May"
msgstr ""
```

Providing context in django template can be done with translation tags as shown
below and context string will appear in the .po the same way as before.
```htmldjango
{% trans "May" context "verb"%}

{% blocktrans context "month name"%}May{% endblocktrans %}
```


## TIPS
1. To ignore newlines within a blocktrans tag with can use trimmed option.
    ```
    {% blocktrans trimmed %}
    This is a multiline text.
    But it will be treated as a single line text by the blocktrans
    tag because it has trimmed option given.
    {% endblocktrans %}
    ```
2. To reused same translated text in multiple place
    * set variable as translated text at one place
        * `{% trans "Repeated text" as var_name %}`
        * `{% blocktrans asvar var_name %}`
           Repeated text
          `{% endblocktrans %}`
    * reuse the `{{ var_name }}`
        * `{{ var_name }}`
3. Very useful extensions for VSCode
    * `gettext` extension by MrOrz for po file syntax highlighting
    * `gettext-duplicate-error` extension by ovcharik for detecting
    duplicate translation string

<!--## TODO List-->
<!--* [ ] Setup the simple project-->
<!--* [ ] Make app necromancer-->
<!--<!-1--->
<!--Tables aren't really required right now because we're just doing static-->
<!--translation it's not high priority-->
<!--* [ ] Add following tables--> 
<!--    * [ ] Spell-->
<!--        + id-->
<!--        + name-->
<!--        + description-->
<!--    * [ ] Necromancer-->
<!--        + id-->
<!--        + name-->
<!--        + gender-->
<!--        + age-->
<!--        + experience-->
<!--        + spells = ManyToManyField(Spell)-->
<!--    * [ ] Revived-->
<!--        + id-->
<!--        + name-->
<!--        + occupation-->
<!--        + revived_by (FK to Necromancer)-->
<!---1->-->
<!--* [ ] Add a simple view (Welcome to the site)-->
<!--* [ ] Translate it using necromancer.-->

<!--* [ ] Add a welcome page-->
<!--* [ ] Pass some context to the welcome page-->
<!--* [ ] Add some text in the welcome page-->
<!--* [ ] Translate both texts-->
<!--    1. [ ] passed as context-->
<!--    2. [ ] already present in the template-->
<!--* End of our tasks-->

<!--## What we're working with?-->
<!--* Only static translation-->

<!--## Setup django project-->
<!--## Create a view-->

