# Pidgin

A core metadata service

## Concept

Pidgin is a lightweight API on top of [Peregrine](https://github.com/uc-cdis/peregrine). It takes a file's GUID as input, queries Peregrine for information about this file and returns an abstract of the file to the user.

Pidgin powers the "Download file" page, accessible from the "Files" page of the [Windmill data portal](https://github.com/uc-cdis/data-portal).

## Usage

Pidgin has a single endpoint: `/<GUID of a file>`. By default, this endpoint returns the core metadata as a JSON document. However, bibliography and JSON-LD schema.org formats are also supported. The user can specify the format of the output using the `Accept` header as follows:

```bash
Accept: application/json # for JSON format
Accept: x-bibtex # for bibliography format
Accept: application/vnd.schemaorg.ld+json # for JSON-LD format
```

## API documentation

[OpenAPI documentation available here.](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/uc-cdis/pidgin/master/openapi/swagger.yml)

The YAML file comtaining the OpenAPI documentation can be found in the `openapi` folder; see the README in that folder for more details.
