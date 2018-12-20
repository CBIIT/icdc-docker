# OpenAPI spec

This is the [OpenAPI](https://github.com/OAI/OpenAPI-Specification)/[Swagger](https://swagger.io/) specification of Pidgin's REST API, which can be visualized [here](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/uc-cdis/pidgin/master/openapi/swagger.yml).

# Swagger Tool

The specification in `swagger.yml` is generated using [Flasgger](https://github.com/rochacbruno/flasgger).

To update the documentation:
* update the docstring of the endpoints impacted by the changes;
* run `python build_openapi.py`;
* validate the updated `swagger.yml` using the [Swagger editor](http://editor.swagger.io);
* git push `swagger.yml`.
