=======
History
=======

0.1.9 (2016-08-08)
------------------

* Added 'I hover over "{container_selector}"'
* Added 'I follow the "{text}" link in "{container_selector}"'

Thanks to Chris Adams for help with these.

0.1.8 (2016-07-26)
------------------

* Added '"{selector}" is not checked'
* Added '"{selector}" has the following text with all whitespace removed'

0.1.7 (2016-07-26)
------------------

* Added 'the browser is at the formatted URL /{path}'
* Added 'I capture the value of "{regex}" in the URL to the "{name}" variable'

0.1.6 (2106-07-25)
------------------

* Added 'I choose "{choice}" from "{selector}"'
* Support whole number of seconds when waiting

0.1.5 (2016-07-18)
------------------

* Added 'type "" into a selector'
* Added '"{selector}" is checked'
* Added 'I capture the value of "{regex}" in the message to the "{name}" variable'
* Added `browserstep/debug.py`
* Added `browserstep/popup.py`
* Added `browserstep/timetravel.py`

0.1.4 (2016-06-20)
------------------

* Fields are cleared before text is sent to them
* Fixed an ordering issue with 'the browser is still at /'
* 'I follow the "{text}" link' also works with image alt text
* Added 'I click the "{text}" label' to allow clicking on labels in forms
* Added 'the value of "{selector}" is "{value}"' for input values

0.1.3 (2016-06-10)
------------------

* Added ability to capture values from fields and apply them to URLs to
  naviagate to or checks inside email bodies
* Added "I switch to the {name} browser" as an alias for "I'm using the
  {name} browser"

0.1.2 (2016-06-10)
------------------

* Improved support for input buttons
* Ability to switch browsers (if present set up in `environment.py`)

0.1.1 (2016-06-09)
------------------

* Added steps for interacting with `lathermail` to inspect email messages sent
  via SMTP (you need to install `requests` separately if you want to use them)

0.1.0 (2016-06-07)
------------------

* First release on PyPI.
