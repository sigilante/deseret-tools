# Tools for Working with the Deseret Alphabet

1. Deseret translation library `deseret`.
2. Deseret translator server applet built with Flask.

```
cd deseret-tools/app
gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app
```
