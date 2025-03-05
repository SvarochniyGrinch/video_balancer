#!/bin/sh

sleep 1

NAME=$1

cd /libs/shared/database

alembic revision --autogenerate -m $NAME
