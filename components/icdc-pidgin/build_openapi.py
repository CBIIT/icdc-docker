import collections
from flasgger import Swagger, Flasgger
import yaml
from yaml.representer import Representer

from pidgin.app import app, app_info


def write_swagger():
    """
    Generate the Swagger documentation and store it in a file.
    """
    yaml.add_representer(collections.defaultdict, Representer.represent_dict)
    outfile = 'openapi/swagger.yml'
    with open(outfile, 'w') as f:
        data = Flasgger.get_apispecs(swagger)
        yaml.dump(data, f, default_flow_style=False)
        print('Generated docs')


if __name__ == '__main__':
    try:
        with app.app_context():
            swagger = Swagger(app, template=app_info)
            write_swagger()
    except Exception as e:
        print('Could not geberate docs: {}'.format(e))
