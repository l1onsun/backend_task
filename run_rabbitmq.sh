#!/bin/sh
docker run -d -p 5672:5672 --name rabbit rabbitmq || docker start rabbit