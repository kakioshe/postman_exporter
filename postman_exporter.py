import argparse
import json
import os


def main(file):
    with open(file) as f:
        data = json.load(f)
        name = ''
        for item in data['item']:
            recursive_read(item, name)


def recursive_read(data, name):
    if 'item' in data.keys():
        for entry in data['item']:
            recursive_read(entry, '{}/{}'.format(name, data['name']))
    else:
        create_markdown(data, name)


def create_markdown(data, name):
    path = 'output/{}'.format(name[1:])

    filename = data['name']
    filename = filename.replace('/', ' or ')
    filename = filename.replace('  ', ' ')

    if not os.path.exists(path):
        os.makedirs(path)

    print('WRITING {}'.format(filename))

    request = data['request']
    response = data['response']

    with open('{}/{}.md'.format(path, filename), 'w') as f:
        f.write('Endpoint for {}\n'.format(name))
        f.write('\n')

        f.write('_url: {}_\n'.format(request['url']['raw']))
        f.write('Method: {}\n'.format(request['method']))
        f.write('\n')

        # HEADER
        f.write('# Header\n')
        f.write('```\n')
        f.write('{\n')
        if 'header' in request.keys():
            for header in request['header']:
                f.write('    {}: {} # {}\n'.format(
                    header['key'], header['value'], header['type']))
        f.write('}\n')
        f.write('```\n')
        f.write('\n')

        # BODY
        f.write('# Body\n')
        f.write('```\n')
        f.write('{\n')
        if 'body' in request.keys():
            for body_data in request['body'][request['body']['mode']]:
                if body_data['type'] == 'text':
                    f.write('   {}: {} # {}\n'.format(
                        body_data['key'], body_data['value'], body_data['type']))
                elif body_data['type'] == 'file':
                    f.write('   {}: {} # {}\n'.format(
                        body_data['key'], body_data['src'], body_data['type']))
        f.write('}\n')
        f.write('```\n')
        f.write('\n')

        # RESPONSE
        f.write('# Response\n')
        for item in response:
            f.write('### {}\n'.format(item['name']))
            if 'code' in item.keys():
                f.write('code: {}\n'.format(item['code']))
            if 'body' in item.keys():
                f.write('```\n')
                f.write('{}\n'.format(item['body']))
                f.write('```\n')
                f.write('\n')
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Automatically create markdown format for postman exports')
    parser.add_argument('file', metavar='input_file', type=str,
                        help='Postman json exported file')

    args = parser.parse_args()
    main(args.file)
