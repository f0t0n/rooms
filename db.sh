#!/usr/bin/env sh

# usage ./db.sh <action> <arguments>

CONFIG="./alembic.ini"

case $1 in
  upgrade )
    alembic --config "$CONFIG" upgrade "${2:-head}"
    ;;
  downgrade )
    alembic --config "$CONFIG" downgrade "$2"
    ;;
  migrate )
    alembic --config "$CONFIG" revision --autogenerate -m "$2"
    ;;
  * )
    printf "Unknown action: '%s'\n" "${1:-<none>}"
    exit 1
    ;;
esac

