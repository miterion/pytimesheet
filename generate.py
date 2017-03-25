from jinja2 import Environment, FileSystemLoader
from os import getcwd, path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from subprocess import Popen, PIPE
from shutil import copy
from configparser import ConfigParser


def latex(template, context, output='output.pdf'):
    with TemporaryDirectory() as tmpdir:
        copy('logo1.png', tmpdir)
        process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tmpdir,)
        process.communicate(template.render(context).encode('utf-8'))
        with open(path.join(tmpdir, 'texput.pdf'), 'rb') as pdffile:
            pdf = pdffile.read()
            with open(output, 'wb') as outfile:
                outfile.write(pdf)

def pdf(job, period, workdays):
    conffile = ConfigParser()
    conffile.read('config.ini')
    config = conffile['Default']
    env = Environment(
            loader=FileSystemLoader(getcwd())
            )
    templ = env.get_template(config['template'])
    context = {
            'institute': job,
            'name': config['lastname'],
            'firstname': config['firstname'],
            'birthday': config['birthday'],
            'period': period,
            'workdays': workdays
            }
    latex(templ, context)

def main():
    conffile = ConfigParser()
    conffile.read('config.ini')
    config = conffile['Default']
    env = Environment(
        loader=FileSystemLoader(getcwd()))
    templ = env.get_template(config['template'])
    for job in config['jobs'].strip(',').split(','):
        context = {'institute': job,
                'name': config['lastname'],
                'firstname': config['firstname'],
                'birthday': config['birthday'],
                'period':{'start':'01.03.2017',
                          'end':'31.03.2017'  
                    },
                'workdays': [{'date':'01.03.2017', 'start':'7:00',
                    'end':'10:00', 'hours':'3'}]
            }
    print(templ.render(context))
    latex(templ, context)


if __name__ == '__main__':
    main()
