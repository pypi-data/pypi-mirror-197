
import os
import re
import yaml
import jsmin
import cssmin 
import mimetypes
from scss import Compiler
import uuid
 
"""
For Single File Component
"""

RE_SSG_BODY_BLOCK = re.compile(r'<ssg\:body\s*/>', re.IGNORECASE)
RE_SFC_TEMPLATE = re.compile(r'<ssg\:template\s*>\n?([\S\s]*?)<\/ssg\:template\s*>', re.IGNORECASE)
RE_SFC_SCRIPT = re.compile(r'<ssg\:script\s*(.*)\s*>\n?([\S\s]*?)<\/ssg\:script\s*>', re.IGNORECASE)
RE_SFC_STYLE = re.compile(r'<ssg\:style\s*(.*)\s*>\n?([\S\s]*?)<\/ssg\:style\s*>', re.IGNORECASE)
RE_BLOCK_BODY = re.compile(r'{%\s*block\s+__SSG_BODY_BLOCK__\s*%}')
RE_EXTENDS = re.compile(r'{%\s*extends\s+(.*?)\s*%}')
RE_BLOCK_BODY_PARSED = re.compile(r'{%\s*block\s+__SSG_BODY_BLOCK__\s*%}(.*?){%\s*endblock\s*%}')


def gen_hash() -> str:
    """ Create a hash value """
    return uuid.uuid4().hex

def replace_layout_body_block(template:str) -> str:
  if RE_SSG_BODY_BLOCK.search(template):
    template = re.sub(RE_SSG_BODY_BLOCK, "{% block __SSG_BODY_BLOCK__ %}{% endblock %}", template, 1)
  return template

def destruct_sfc(content):
    """
    To destruct a single file component into template, script, style
    :param: string content 
    :returns: tuple - (Bool, {template, script, style, script_props, style_props})
    """
    s_template = re.search(RE_SFC_TEMPLATE, content)
    s_script = re.search(RE_SFC_SCRIPT, content)
    s_style = re.search(RE_SFC_STYLE, content)

    if s_template:
        return (True, {
            "template": s_template.group(1) if s_template else content,
            "script": s_script.group(2).replace("\"","'") if s_script else None,
            "script_props": s_script.group(1) if s_script else None,
            "style": s_style.group(2) if s_style else None,
            "style_props": s_style.group(1) if s_style else None,
        })
    else:
        return (False, {"template": content, "script": None, "style": None, "script_props": "", "style_props": ""})


"""
To get the macros in a content
Must be in this format
{% macro macro_name(...) %}
"""
RE_MACROS = re.compile(r'{%\s*macro\s+([\S\s]*?)\s*\(', re.IGNORECASE)
"""
To get macro document and match them to the macro 
Must be in this format:
{# macro_name: description #}
"""
RE_MACROS_DOC = re.compile(r'{#\s*([\S\s]*?)#}', re.IGNORECASE)

def get_macros_definition(tpl):
    """
    Get file/content containing macros, and return a dict of key and description
    To be used in documentation of macros
    :param text:
    :return dict:
    """
    macros = {m: '' for m in re.findall(RE_MACROS, tpl) if not m.startswith("_")}
    if macros:
      for d in re.findall(RE_MACROS_DOC, tpl):
        sd = d.split(':', 1)
        if len(sd) == 2:
            name, description = sd
            if name.strip() in macros:
                macros[name.strip()] = description.strip()
    return macros

class dictdot(dict):
    """
    A dict extension that allows dot notation to access the data.
    ie: dict.get('key.key2.0.keyx'). Still can use dict[key1][k2]
    To create: dictdot(my)
    """
    def get(self, key, default=None):
        """ access data via dot notation """
        try:
            val = self
            if "." not in key:
                return self[key]
            for k in key.split('.'):
                if k.isdigit():
                    k = int(k)
                val = val[k]
            return val
        except (TypeError, KeyError, IndexError) as e:
            return default


def load_conf(yml_file, conf={}):
    """
    To load the config
    :param yml_file: the config file path
    :param conf: dict, to override global config
    :return: dict
    """
    with open(yml_file) as f:
        data = yaml.safe_load(f)
        if conf:
            data.update(conf)
        return dictdot(data)


def extract_sitename(s):
    return re.sub(r"https?://(www\.)?", '', s).replace("www.", "")


def chunk_list(items, size):
    """
    Return a list of chunks
    :param items: List
    :param size: int The number of items per chunk
    :return: List
    """
    size = max(1, size)
    return [items[i:i + size] for i in range(0, len(items), size)]


def merge_dicts(dict1, dict2):
    """ Recursively merges dict2 into dict1 """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1

def scss_to_css(content):
    return Compiler().compile_string(content)


def bundle_assets(ftype: str, files: list, dest: str):
    """
    To  bundle assets files together

    Params:
        ftype: str - the file type [css|js]
        files:list - list of files to bundle
        dest: the destination to save file
    """
    contents = ""
    for file in files:
        with open(file) as f:
            contents += f.read()
    if ftype == "css":
        contents = cssmin.cssmin(contents)
    elif ftype == "js":
        contents = jsmin.jsmin(contents)
    if contents:
        with open(dest, "w") as f:
            f.write(contents)

def merge_files_contents(files: list) -> str:
    contents = ""
    for file in files:
        with open(file) as f:
            contents += f.read()
    return contents

def minify_static_contents(ftype:str, contents:str):
    """
    To minify contents for static files. 

    Params:
        ftype:str - type, css|js
        contents:str - the conent to minify
    """
    if ftype == "css":
        return cssmin.cssmin(contents)
    elif ftype == "js":
        return jsmin.jsmin(contents)
    return contents

def write_file(contents:str, dest:str):
    """
    To minify contents for static files. 

    Params:
        contents:str - the conent to minify
        dest:path - the output file 
    """
    if contents:
        with open(dest, "w") as f:
            f.write(contents)

def is_external_url(url:str) -> bool:
    return url.startswith(('http://', 'https://'))

def context_root(context:str):
  contexts = context.strip("/").split("/")
  if len(contexts) == 1:
    return "./"
  return "/".join([".." for _ in contexts])