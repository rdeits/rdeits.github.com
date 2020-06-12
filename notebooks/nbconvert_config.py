"""
Usage: see convert.py


Derived from https://gist.github.com/mprat/a843b08e315621d91a667124a243abeb
See also: http://www.mprat.org/blog/2017/03/18/blogging-with-jupyter.html
"""


import os
import re
from nbconvert.preprocessors import Preprocessor
from ipython_genutils.ipstruct import Struct

def jekyllurl(path):
    """
    Take the filepath of an image output by the ExportOutputProcessor
    and convert it into a URL we can use with Jekyll
    """
    return path.replace("../../..", "")


def svg_filter(svg_xml):
    """
    Remove the DOCTYPE and XML version lines from
    the inline XML SVG
    """
    svgstr = "".join(svg_xml)
    start_index = svgstr.index("<svg")
    end_index = svgstr.index("</svg>")
    return svgstr[start_index:end_index + 6]

c = get_config()

# Can we somehow get this from nbconvert without having to set an
# environment variable?
notebook_folder = os.path.join("notebooks", os.environ["NBCONVERT_NOTEBOOK_FOLDER"])


c.NbConvertApp.export_format = 'html'
c.NbConvertApp.output_files_dir = os.path.join(
    '../../../img', notebook_folder)

# c.EmbedImagesPreprocessor.embed_images=True

class RelativeImagesPreprocessor(Preprocessor):
    def replfunc_md(self, match):
        """Read image and store as base64 encoded attachment"""
        url = match.group(2)
        print("url:", url)
        imgformat = url.split('.')[-1].lower()
        if url.startswith('http'):
            return match.group(0)
        elif url.startswith('attachment'):
            return match.group(0)
        else:
            return '![' + match.group(1) + '](/' + os.path.join(notebook_folder, match.group(2)) + ')'

    def preprocess_cell(self, cell, resources, index):
        self.path = resources['metadata']['path']
        self.attachments = getattr(cell, 'attachments', Struct())

        if cell.cell_type == "markdown":
            regex = re.compile('!\[([^"]*)\]\(([^"]+)\)')
            cell.source = regex.sub(self.replfunc_md, cell.source)
            cell.attachments = self.attachments
        return cell, resources

c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ('remove_output',)
c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)

c.HTMLExporter.preprocessors = [
    # 'nbconvert.preprocessors.ExecutePreprocessor',
    # 'jupyter_contrib_nbextensions.nbconvert_support.pre_embedimages.EmbedImagesPreprocessor',
    RelativeImagesPreprocessor,
    'nbconvert.preprocessors.TagRemovePreprocessor',
    'nbconvert.preprocessors.coalesce_streams',
    'nbconvert.preprocessors.ExtractOutputPreprocessor']
c.HTMLExporter.template_file = 'jekyll.tpl'

c.HTMLExporter.filters = {"jekyllimgurl": jekyllurl, "svg_filter": svg_filter}

# c.ExecutePreprocessor.allow_errors = True

c.FilesWriter.build_directory = os.path.join(
    "../_includes",
    notebook_folder)
