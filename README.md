## Local Install

pip install -e ../aischool_backend_framework --config-settings editable_mode=strict

## Global Install

pip install -e "git+https://github.com/IgorGrosu21/AISchool-shared-backend.git#egg=aischool_backend_framework"

## Local run

waitress-serve --listen=\*:<PORT> core.wsgi:application
