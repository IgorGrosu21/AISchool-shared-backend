## Local Install

pip install -e ../aischool_backend_framework --config-settings editable_mode=strict


## Local run

waitress-serve --listen=*:<PORT> core.wsgi:application