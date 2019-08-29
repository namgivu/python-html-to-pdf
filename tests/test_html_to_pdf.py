import datetime
import os
import unittest
import jinja2
import pdfkit

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/..'
TEMPLATE_HOME = f'{PROJECT_PATH}/fixture'


class Test(unittest.TestCase):

    def test(self):
        #region prepare html from template and fixture

        # load template from html file in :TEMPLATE_HOME folder
        env = jinja2.Environment(loader=jinja2.FileSystemLoader([TEMPLATE_HOME, TEMPLATE_HOME]), trim_blocks=True)
        template_filename = 'some_template.html'
        t = env.get_template(template_filename)  # t aka template

        params = {
            'some_var1': 122,
            'some_var2': 'abbccc',
        }
        template_rendered = t.render(**params)

        # write template to /tmp and make pdf file from it
        o  = '/tmp'  # o aka output path
        fn = 'test_html_to_pdf'  # fn aka filename
        today = datetime.datetime.today(); suffix = today.strftime('%Y%m%d-%H%M%S'); os.makedirs(o, exist_ok=True)  # suffix as timestamp for multi-thread safety
        html_file = f'{o}/{fn}_{suffix}.html'
        pdf_file  = f'{o}/{fn}_{suffix}.pdf'

        with open(html_file, 'w') as f:
            f.write(template_rendered)
            f.close()

        # convert html to pdf
        options = {
            'page-size': 'A4',  # this is also default value for page-size
            'encoding' : 'UTF-8',
        }

        #endregion prepare html from template and fixture

        # the testee
        pdfkit.from_file(html_file, pdf_file, options)

        # assert the expected output
        assert os.path.isfile(pdf_file)
