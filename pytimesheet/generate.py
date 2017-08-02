from pytimesheet.utils import get_config, get_config_path, open_file, get_path

from jinja2 import Environment, PackageLoader
from os import path
from tempfile import TemporaryDirectory
from subprocess import Popen, PIPE
from shutil import copy, copyfile


def latex(template, context, job, month, output='output.pdf'):
    with TemporaryDirectory() as tmpdir:
        copy(str(get_path(__file__)) + '/template/logo.png', tmpdir)
        process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tmpdir,)
        process.communicate(template.render(context).encode('utf-8'))
        outputpath = path.join(
            get_config_path(),
            'job',
            str(job),
            str(month),
            output)
        copyfile(path.join(tmpdir, 'texput.pdf'), outputpath)
        print(outputpath)
        open_file(outputpath)
        return
        with open(path.join(tmpdir, 'texput.pdf'), 'rb') as pdffile:
            pdf = pdffile.read()
            with open(output, 'wb') as outfile:
                outfile.write(pdf)


def pdf(job, month, period, workdays):
    conffile = get_config()
    config = conffile['Default']
    env = Environment(
        loader=PackageLoader('pytimesheet', 'template')
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
    latex(templ, context, job, str(month))
