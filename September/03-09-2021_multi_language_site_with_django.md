# Multi Language Site with Django

This is going to be a run through of how one can get around setting up a
multi-language site in django. We are going to go through following steps to
set it all up.
* Setup the locale settings
* Mark the strings for translation and make the .po files
* Add the translation in .po files and generate .mo files
* Switch language in template
* Tips
  * Working the variables inside translation string in django template
  * Contextual markers: translation for words that have different meaning in different context
  * Trimmed blocktrans
  * Resuing translated text as variable in django template
  * Useful extensions for VSCode

## 1. Setup the locale settings
* [ ] make the directory to where .po and .mo files should go (this is the LOCALE_PATHS)
    * [ ] $BASE_DIR/locale/
* [ ] add LOCALE_PATHS variable to settings.py file.
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
    _Adding the middleware and wrapping the url paths with i18n_patterns will
      set the translation urls to be automatically handled
      For example: all nepali language page paths will have ne/ prefixed to them.
      (en for english)_

## 2. Mark the strings for translation and make the .po files
1. [ ] Let django know which texts should be translated
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
2. [ ] run the command: `python manage.py makemessages -l ne`

  _Note: for makemessages & compilemessages command to work, you need to install GNU gettext utilities 
  in your computer_
      * _For linux users, gettext will usually be installed by default. If it isn't, you
      can install using the package manager of your choice._
      * _For windows users, read more at this [link](https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#gettext-on-windows) or download & install getext [here](https://mlocati.github.io/articles/gettext-iconv-windows.html)_

## 3. Add the translation in .po files and generate .mo files
* [ ] edit the .po files
    ```po
    #: emergencyApp/models.py:159 genericAbsenteeApp/views.py:191
    #: genericBusinessApp/views.py:194 genericIndividualApp/views.py:426
    #: municipality/views.py:706 template/backend/base/include/leftsidemenu.html:68
    #: template/backend/data/catalogue/index.html:47
    #: template/backend/data/update/include/sidebar.html:11
    #: template/backend/data/update/include/sidebar.html:22
    #: template/backend/data/update/include/verification-sidebar.html:13
    #: template/backend/demography/base/include/leftsidemenu.html:68
    #: template/frontend/data/catalogue/index.html:41
    msgid "House"
    msgstr "घर"

    #: emergencyApp/models.py:160
    msgid "Number of infected"
    msgstr "संक्रमितको संख्या"

    #: emergencyApp/models.py:161
    msgid "Number of active"
    msgstr "सक्रिय संख्या"

    #: emergencyApp/models.py:162
    msgid "Number of recovered"
    msgstr "निको भएको संख्या"
    ```
    ```po
    #: template/backend/data/catalogue/index.html:84
    msgid ""
    "Translation , paraphrase , version refer to a rewording of something. A "
    "translation is a rendering of the same ideas in a different language from the "
    "original: a translation from Greek into English. A paraphrase is a free "
    "rendering of the sense of a passage in other words, usually in the same "
    "language: a paraphrase of a poem. A version is a translation, especially of the "
    "Bible, or else an account of something illustrating a particular point of view: "
    "the Douay Version. "
    msgstr ""
    "अनुवाद, p संस्करण केहि को एक rewording को सन्दर्भ। एक अनुवाद मूल बाट फरक भाषा मा एउटै "
    "विचारहरु को एक प्रतिपादन हो: ग्रीक बाट अंग्रेजी मा अनुवाद। एक पाराफ्रेज अन्य शब्दहरु मा एक पारित को भावना को एक "
    "मुक्त प्रतिपादन हो, सामान्यतया एउटै भाषा मा: एक कविता को एक व्याख्या। एक संस्करण एक अनुवाद हो, विशेष गरी "
    "बाइबल को, वा अन्यथा केहि एक खाता को एक विशेष दृष्टिकोण को दृष्टान्त को एक खाता: Douay संस्करण।" "
    ```
* [ ] compile and regenerate .mo file with the following command. This .mo file
  is the file that is going to be used by django to read the translated texts.
    * [ ] Use this command: `python manage.py compilemessages`
* [ ] translations should work now after restarting the server

## 4. Switch language in template
* If you only have two languages to switch between you can just do it the following way.
    ```htmldjango
    <ol>
      <li class="">
        <a class="nav-link nav-user mr-0 waves-eff" href="/en{{ request.get_full_path|slice:'3:' }}" role="button">
          <span class="pro-user-name ml-1">
            {% trans "English" %}
          </span>
        </a>
      </li>
      <li>
        <a class="nav-link nav-user mr-0 waves-eff" href="/ne{{ request.get_full_path|slice:'3:' }}" role="button">
          <span class="pro-user-name ml-1">
            {% trans "Nepali" %}
          </span>
        </a>
       </li>
    </ol>
    ```

* If you want to have multiple languages, you might want to try the following way.
    1. We've already added the supported languages in settings.py as below
       when setting up locale settings
       ```python
          LANGUAGES = (
              ('en', _('English')),
              ('ne', _('Nepali')),
          )
       ```
    2. Next, we have to include the django translation urlpatterns as shown
        below to use the set_language url pattern.
        ```python
        urlpatterns += [path('i18n/', include('django.conf.urls.i18n')),]
        ```
    3. Setup the translation tags as shown below.
        ```htmldjango
        {% load i18n %}
        <div>
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
            <form action="{% url 'set_language' %}" method="POST">
              {% csrf_token %}
              <input name="next" type="hidden" value="{{ redirect_to }}">
              <select name="language" onchange="this.form.submit()">
                {% for language in languages %}
                <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                {{ language.name_local }} ({{ language.code }})
                </option>
                {% endfor %}
              </select>
            </form>
        </div>
        ```
        And that is all we need to do to add language switching in our site.

## TIPS
1. Contextual markers: Translation for words that have different meaning in different context
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
    msgstr "मे"
    
    msgctxt "verb"
    msgid "May"
    msgstr "सायद"
    ```

    Providing context in django template can be done with translation tags as shown
    below and context string will appear in the .po the same way as before.
    ```htmldjango
    {% trans "May" context "verb"%}
    
    {% blocktrans context "month name"%}May{% endblocktrans %}
    ```
2. Working the variables inside translation string in django template
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
3. To ignore newlines within a blocktrans tag with can use trimmed option.
    ```
    {% blocktrans trimmed %}
    This is a multiline text.
    But it will be treated as a single line text by the blocktrans
    tag because it has trimmed option given.
    {% endblocktrans %}
    ```
4. To reused same translated text in multiple place
    * set variable as translated text at one place
        * `{% trans "Repeated text" as var_name %}`
        * `{% blocktrans asvar var_name %}`
           Repeated text
          `{% endblocktrans %}`
    * reuse the `{{ var_name }}`
        * `{{ var_name }}`
5. Very useful extensions for VSCode
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

