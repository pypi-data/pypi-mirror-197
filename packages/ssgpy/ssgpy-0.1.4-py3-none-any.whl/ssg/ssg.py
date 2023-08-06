"""
~ SSG.py ~
"""

import os
import re
import sys
import copy
import json
import time
import uuid
import yaml
import jsmin
import arrow
import shutil
import cssmin
import jinja2
import logging
import datetime
import frontmatter
import pkg_resources
from slugify import slugify
from . import ext
from distutils.dir_util import copy_tree
from .__about__ import *
from . import lib
from scss import Compiler


# ------------------------------------------------------------------------------

NAME = "SSG.py"
PAGE_FORMAT = (".html", ".md")
DEFAULT_LAYOUT = "layouts/default.html"


# ==============================================================================
# -------------------------------- SSG.py -------------------------------------
# ==============================================================================

HTML_REDIRECT_TEMPLATE = """<meta http-equiv="Refresh" content="0; url='{url}'" />"""

def print_info(message):
    print("- %s" % message)

cached = {}
    
class Generator(object):

    default_page_meta = {
        "title": "",            # The title of the page
        "markup": None,         # The markup to use. ie: md | html (default)
        "slug": None,           # The pretty url new name of the file. A file with the same name will be created
        "permalink": None,      # to create a full unique name. It can have slashes etc. ie: /some/page/deep/pages
        "url": "",              # This will be added when processed. Should never be modified
        "description": "",      # Page description
        # By default, all url will be pretty (search engine friendly) Set to False to keep the .html
        "pretty_url": True,
        "meta": {},
        "redirect": None,       # To allow an html redirect - the page to redirect to. 
        "layout": None,         # The layout for the page
        "template": None,       # The page template.
        "sfc": True,            # For single file component
        "__assets": {           # Contains all assets generated
            "js": [],           # List of all js url in the page
            "css": []           # List of all CSS url in the page
        }
    }
    tpl_env = None
    _templates = {}
    _pages_meta = {}

    def __init__(self, root_dir, options={}):
        """

        :param root_dir: The application root dir
        :param options: options to build
        """

        self.root_dir = root_dir
        self.build_dir = os.path.join(self.root_dir, "build")
        self.static_dir = os.path.join(self.root_dir, "static")
        self.content_dir = os.path.join(self.root_dir, "content")
        self.pages_dir = os.path.join(self.root_dir, "pages")
        self.templates_dir = os.path.join(self.root_dir, "templates")
        self.data_dir = os.path.join(self.root_dir, "data")
        self.build_static_dir = os.path.join(self.build_dir, "static")
        self.build_static_gen_dir = os.path.join(self.build_static_dir, "_gen")

        self.config_file = os.path.join(self.root_dir, "ssg.yml")
        self.config = lib.load_conf(self.config_file)
        self.config.setdefault("env", {})
        self.config.setdefault("serve", {})
        self.config.setdefault("build", {})
        self.config.setdefault("globals", {})
        self.config.setdefault("assets_bundles", {})
        self.layout = self.config.get("globals.layout", DEFAULT_LAYOUT)

        build_type = options.get("build", "build")

        self.build_config = lib.dictdot(self.config[build_type])
        site_env = self.build_config.get("env")
        if options and options.get("env") is not None:
            site_env = options.get("env")

        self.site_config = lib.dictdot(self.config.get("site", {}))
        if site_env:
            if site_env in self.config["env"]:
                self.site_config = lib.merge_dicts(self.site_config, self.config.get('env.%s' % site_env))
            else:
                raise ValueError("Environment Error: env %s@%s not found" % (site_env, build_type))

        self.site_env = site_env
        self.site_config.setdefault("base_url", "/")
        self.site_config.setdefault("static_url", "/static")
        self.base_url = self.site_config.get("base_url")
        self.static_url = self.site_config.get("static_url")
        self._context_root = "./"
        self._data = {}
        self._load_data()

        # Map the pages so it can be easily resolve, ie: index -> index.html, hello/world -> hello/world.html
        self.pages_short_mapper = {}
        self.print_info = False

        self._init_jinja({
            "get_page": self._get_page,
            "get_page_url": self._get_page_url,
            "get_static_url": self._get_static_url,
            "get_data": self._get_data,
            "get_static_bundle": self._get_page_static_bundle_url,
            "get_site": self._get_site,
            "format_date": lambda dt, format="MM/DD/YYYY h:mm a": arrow.get(dt).format(format),
            "current_date": lambda: arrow.now(),
            "site": self.site_config,
            "__info": self._load_info(),
        })

        
    def _load_info(self):
        """ Global variables """
        now = datetime.datetime.now()
        return {
            "name": __title__,
            "version": __version__,
            "url": __uri__,
            "generator": "%s %s" % (__title__, __version__),
            "year": now.year,
            "timestamp": int(time.time())
        }

    def _init_jinja(self, global_context={}):


        loader = jinja2.ChoiceLoader([
            jinja2.PrefixLoader({'content':jinja2.FileSystemLoader(self.content_dir)}),
            jinja2.FileSystemLoader(self.templates_dir)
        ])

        # Extension
        env_extensions = [
            'ssg.ext.MarkdownExtension',
            'ssg.ext.MarkdownTagExtension',
        ]
        if self.build_config.get("compress_html") is True:
            env_extensions.append('ssg.ext.HTMLCompress')

        self.tpl_env = jinja2.Environment(loader=loader, extensions=env_extensions)

        self.tpl_env.add_extension('jinja2.ext.do')
        self.tpl_env.globals.update(global_context)

    def _get_data(self, path):
        """
        Get the data from /data dir

        Params:
            path:dotNotationStr
        Returns: mixed
        """
        return self._data.get(path)

    def _get_page_meta_data(self, page):
        """
        Cache the page meta from the frontmatter and assign new keys
        The cache data will be used to build links or other properties
        """
        page = self.pages_short_mapper.get(page)
        meta = self._pages_meta.get(page)
        if not meta:
            src_file = os.path.join(self.pages_dir, page)
            with open(src_file) as f:
                _, _ext = os.path.splitext(src_file)
                markup = _ext.replace(".", "")
                _meta, _ = frontmatter.parse(f.read())
                meta = self.default_page_meta.copy()
                meta["meta"].update(self.config.get("site.meta", {}))
                meta.update(_meta)
                dest_file, url = self._get_dest_file_and_url(page, meta)
                meta["url"] = url
                meta["filepath"] = dest_file
                if meta.get("markup") is None:
                    meta["markup"] = markup
                self._pages_meta[page] = lib.dictdot(meta)
        return meta

    def _get_page_content(self, page):
        """ Get the page content without the frontmatter """
        src_file = os.path.join(self.pages_dir, page)
        with open(src_file) as f:
            _meta, content = frontmatter.parse(f.read())
            return content

    def _get_page(self, page_dot_path:str):
        """
        To get page properties, ie: title, description, data, etc

        Example
            {{ get_page("about.title")}}
            {{ get_page("about.description") }}
            {{ get_page("about.data") }} : dict|list

        Params:
            page_dot_path:str - a page dot path notation, ie: $[page].$path -> [about].[title]
        
        Returns: mixed
        """
        s = page_dot_path.split(".", 1)
        if len(s) == 2:
            return self._get_page_meta_data(s[0]).get(s[1])
        else:
            return self._get_page_meta_data(s[0])
        
    def _get_page_url(self, page, full_url=False):
        """ Get the url of a  page """
        anchor = ""
        if "#" in page:
            page, anchor = page.split("#")
            anchor = "#" + anchor
        meta = self._get_page_meta_data(page)
        return self._make_url(meta.get("url"), full_url=full_url)

    def _make_url(self, url, full_url=False):
        """
        """
        if full_url:
            return self.base_url.rstrip("/") + "/" + url.lstrip("/")
        if len(self._context_root.split("..")) > 1:
            return self._context_root.rstrip("/") + url
        if "./" + url.strip("/") == "./":
            return "../"
        return url 

    def _get_page_static_bundle_url(self, page, bundle_name):
        _page = lib.dictdot(page)
        if url := _page.get("__assets.%s" % bundle_name):
            return self._get_static_url(url)
        return ""

    def _get_static_url(self, url):
        """Returns the static url """
        if url.startswith("//") or url.startswith("http"):
            return url
        url = self.static_url.rstrip("/") + "/" + url.lstrip("/")
        if len(self._context_root.split("..")) > 1:
            self._context_root.rstrip("/") + url
        return url

    def _get_dest_file_and_url(self, filepath, page_meta={}):
        """ Return tuple of the file destination and url """

        slugname = None
        # permalink 
        if permalink := page_meta.get("permalink"):
            filepath = permalink
            if not filepath.endswith((".html", ".md")):
                filepath += ".html"

        elif slug := page_meta.get("slug"):
            slugname = slugify(slug)

        filename = filepath.split("/")[-1]
        slugname = slugname or filename
        filepath_base = filepath.replace(filename, "").rstrip("/")
        fname = slugname.replace(".html", "").replace(".md", "")
            
        if page_meta.get("pretty_url") is False:
            dest_file = os.path.join(filepath_base, "%s.html" % fname)
        else:
            dest_dir = filepath_base
            if filename not in ["index.html", "index.md"]:
                dest_dir = os.path.join(filepath_base, fname)
            dest_file = os.path.join(dest_dir, "index.html")

        url = "/" + dest_file.replace("index.html", "")
        return dest_file, url

    def _load_data(self):
        data = {}
        # Load data from the data directory
        for root, _, files in os.walk(self.data_dir):
            for fname in files:
                if fname.endswith((".json",)):
                    name = fname.replace(".json", "")
                    fname = os.path.join(root, fname)
                    if os.path.isfile(fname):
                        with open(fname) as f:
                            _ = json.load(f)
                            if isinstance(_, dict):
                                _ = lib.dictdot(_)
                            data[name] = _
        self._data = lib.dictdot(data)

    def _get_site(self, prop):
        return self.site_config.get(prop)

    def clean_build_dir(self):
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

    def build_static(self):
        """ Build static files """
        if not os.path.isdir(self.build_static_dir):
            os.makedirs(self.build_static_dir)
        if (self.print_info):
            print_info('copying static dir to build folder...')
        copy_tree(self.static_dir, self.build_static_dir)

    def build_pages(self):
        """Iterate over the pages_dir and build the pages """
        src_files = []
        self._pages_meta = {}
 
        # Aggregate all the files
        for root, _, files in os.walk(self.pages_dir):
            if (self.print_info):
                print_info('aggregating pages files...')

            base_dir = root.replace(self.pages_dir, "").lstrip("/")
            if not base_dir.startswith("_"):
                for f in files:
                    fname, _ext = os.path.splitext(f)
                    self.pages_short_mapper.update({fname: f, f: f})
                    markup = _ext.replace(".", "")
                    src_file = os.path.join(base_dir, f)
                    src_files.append(src_file)
        # Build pages
        if (self.print_info):
            print_info('initiating page building...')
        [self._build_page(src_file) for src_file in src_files]

    def _build_page(self, filepath):
        """ To build from filepath, relative to pages_dir """
        filename = filepath.split("/")[-1]
        # If filename starts with _ (underscore) or . (dot) do not build
        if not filename.startswith(("_", ".")) and (filename.endswith(PAGE_FORMAT)):
            meta = self._get_page_meta_data(filepath)
            content = self._get_page_content(filepath)

            # The default context for the page
            _default_page = {
                "build_dir": self.build_dir,
                "filepath": meta["filepath"],
                "context": {"page": meta},
                "content": content,
                "markup": meta.get("markup"),
                "template": meta.get("template"),
                "layout": meta.get("layout") or self.layout
            }

            # GENERATOR
            # Allows to generate
            _generator = meta.get("_generator")
            if _generator:
                raise NotImplementedError('GENERATOR IS NOT PROPERLY IMPLEMENTED YET')
                exit()
                data = self._data.get(_generator.get("data_source"))

                # We want these back in meta in they exists in the data
                special_meta = ["title", "slug", "description"]

                # SINGLE
                if _generator.get("type") == "single":
                    for d in data:
                        dmeta = copy.deepcopy(meta)
                        page = copy.deepcopy(_default_page)
                        for _ in special_meta:
                            if _ in d:
                                dmeta[_] = d.get(_)

                        # If generator has the slug, it will substitute if
                        # Slug in the generator must have token from the data
                        # to generate the slug
                        if "slug" in _generator:
                            dmeta["slug"] = _generator.get("slug").format(**d)

                        # Slug is required
                        if "slug" not in dmeta:
                            print(
                                "WARNING: Skipping page because it's missing `slug`")
                            continue
                        slug = dmeta.get("slug")
                        dmeta["url"] = slug
                        dmeta["context"] = d

                        page.update({
                            "filepath": slug,
                            "context": {"page": dmeta}
                        })
                        self.create_page(**page)

                if _generator.get("type") == "pagination":

                    per_page = int(_generator.get(
                        "per_page", self.site_config.get("pagination.per_page", 10)))
                    left_edge = int(_generator.get(
                        "left_edge", self.site_config.get("pagination.left_edge", 2)))
                    left_current = int(_generator.get(
                        "left_edge", self.site_config.get("pagination.left_current", 3)))
                    right_current = int(_generator.get(
                        "right_current", self.site_config.get("pagination.right_current", 4)))
                    right_edge = int(_generator.get(
                        "right_edge", self.site_config.get("pagination.right_edge", 2)))
                    padding = _generator.get("padding")
                    slug = _generator.get("slug")
                    limit = _generator.get("limit")

                    if "limit" in _generator:
                        data = data[:int(limit)]
                    data_chunks = lib.chunk_list(data, per_page)
                    len_data = len(data)

                    for i, d in enumerate(data_chunks):
                        dmeta = copy.deepcopy(meta)
                        page = copy.deepcopy(_default_page)

                        page_num = i + 1
                        _paginator = Paginator([],
                                               total=len_data,
                                               page=page_num,
                                               per_page=per_page,
                                               padding=padding,
                                               left_edge=left_edge,
                                               right_edge=right_edge,
                                               left_current=left_current,
                                               right_current=right_current)
                        _paginator.slug = slug
                        _paginator.index_slug = _generator.get("index_slug")

                        _slug = slug.format(**{"page_num": page_num})
                        dmeta["url"] = _slug
                        dmeta["context"] = d
                        dmeta["paginator"] = _paginator
                        page.update({
                            "filepath": _slug,
                            "context": {"page": dmeta}
                        })
                        self.create_page(**page)

                        # First page need to generate the index
                        if i == 0 and _generator.get("index_slug"):
                            page["filepath"] = _generator.get("index_slug")
                            self.create_page(**page)

            # NORMAL PAGE
            else:
                self.create_page(**_default_page)

    def _reset_page_context_assets(self, context):
        context["page"]["__assets"] = {
            "js": [],
            "css": []
        }

    def create_page(self, build_dir, filepath, context={}, content=None, template=None, markup=None, layout=None):
        """
        To dynamically create a page and save it in the build_dir
        :param build_dir: (path) The base directory that will hold the created page
        :param filepath: (string) the name of the file to create. May  contain slash to indicate directory
                        It will also create the url based on that name
                        If the filename doesn't end with .html, it will create a subdirectory
                        and create `index.html`
                        If file contains `.html` it will stays as is
                        ie:
                            post/waldo/where-is-waldo/ -> post/waldo/where-is-waldo/index.html
                            another/music/new-rap-song.html -> another/music/new-rap-song.html
                            post/page/5 -> post/page/5/index.html
        :param context: (dict) context data
        :param content: (text) The content of the file to be created. Will be overriden by template
        :param template: (path) if source is not provided, template can be used to create the page.
                         Along with context it allows to create dynamic pages.
                         The file is relative to `/templates/`
                         file can be in html|md
        :param markup: (string: html|md), when using content. To indicate which markup to use.
                        based on the markup it will parse the data
                        html: will render as is
                        md: convert to the appropriate format
        :param layout: (string) when using content. The layout to use.
                        The file location is relative to `/templates/`
                        file can be in html|md
        :return:
        """

        _context = lib.dictdot(context)
        build_dir = build_dir.rstrip("/")
        filepath = filepath.lstrip("/").rstrip("/")
        if not filepath.endswith(".html"):
            filepath += "/index.html"

        dest_file = os.path.join(build_dir, filepath)
        dest_dir = os.path.dirname(dest_file)

        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        
        if "page" not in _context:
            _context["page"] = self.default_page_meta.copy()
        if "url" not in _context["page"]:
            _context["page"]["url"] = "/" + \
                filepath.lstrip("/").replace("index.html", "")
        self._reset_page_context_assets(_context)
        _context["this"] = _context["page"]

        #! redirect
        if redirect := _context.get("page.redirect"):
            url = redirect if lib.is_external_url(redirect) else self._get_page_url(redirect, full_url=True)
            content = HTML_REDIRECT_TEMPLATE.format(url=url)
            lib.write_file(dest=dest_file, contents=content)
            return


        if template:
            if template not in self._templates:
                self._templates[template] = self.tpl_env.get_template(template)
            tpl = self._templates[template]
        else:
            is_sfc, sfc_c = lib.destruct_sfc(content)
            content = sfc_c.get('template')
            if markup == "md":
                content = ext.convert(content)

            # Page must be extended by a layout and have a block 'body'
            # These tags will be included if they are missing
            if re.search(lib.RE_EXTENDS, content) is None:
                layout = layout or self.layout
                content = "\n{% extends '{}' %} \n\n".replace("{}", layout) + content

            if re.search(lib.RE_BLOCK_BODY, content) is None:
                _layout_block = re.search(lib.RE_EXTENDS, content).group(0)
                content = content.replace(_layout_block, "")
                content = "\n" + _layout_block + "\n" + \
                          "{% block __SSG_BODY_BLOCK__ %} \n" + content.strip() + \
                    "\n{% endblock %}"
                
            # Create SFC Assets
            if is_sfc is True:
                if not os.path.isdir(self.build_static_gen_dir):
                    os.makedirs(self.build_static_gen_dir)
                sfc_hash = lib.gen_hash()
                sfc_asset_filepath = slugify(filepath)
                sfc_o = {"script": "js", "style": "css"}
                for o in sfc_o:

                    if (sfc_c.get(o)):
                        _ff = os.path.join(self.build_static_gen_dir, "%s_%s.%s" % (
                            sfc_asset_filepath, sfc_hash, sfc_o[o]))
                        _sff = _ff.replace(self.build_static_dir, '').lstrip("/")
                        _context["page"]["sfc_%s_path" % sfc_o[o]] = _sff

                        # write content
                        o_content = sfc_c.get(o)
                        o_content = o_content.replace('{%STATIC_URL%}', self.static_url.rstrip("/"))
                        # convert SCSS to css -> <style scss>
                        if o == 'style' and "scss" in sfc_c["style_props"].strip():
                            o_content = lib.scss_to_css(o_content)
                        lib.write_file(dest=_ff, contents=o_content)

                        if o == "script":
                            # "attributes": sfc_c["script_props"]
                            _context["page"]["__assets"]["js"].append(_sff)
                        elif o == "style":
                            _context["page"]["__assets"]["css"].append(_sff)

            tpl = self.tpl_env.from_string(content)

        # Bundle assets
        if True:
            """
            With bundle enabled, you can instead put the bundle on the page instead of individual files

            = Bundle
                <link rel="stylesheet" type="text/css" href="{{ get_static_bundle(page, 'page_css_bundle') }}">

                <script type="text/javascript" src="{{ get_static_bundle(page, 'page_js_bundle') }}"></script>

            = No bundle

                {% for file in page.__assets.js %}
                    <script type="text/javascript" src="{{ get_static_url(file) }}"></script>
                {% endfor %}

                {% for file in page.__assets.css %}
                    <link rel="stylesheet" type="text/css" href="{{ get_static_url(file) }}">
                {% endfor %}

            """
            name = "bundle_%s_%s" % (slugify(filepath), lib.gen_hash())
            filepath_ = os.path.join(self.build_static_gen_dir, name)
            bundlename_ = filepath_.replace(self.build_static_dir, '').lstrip("/")
        
            ftypes = {
                "css": ("assets_bundles.page_css_bundle", "page.__assets.css", "page_css_bundle"),
                "js": ("assets_bundles.page_js_bundle", "page.__assets.js", "page_js_bundle"),
            }
            for ftype, s in ftypes.items():
                cached_contents_ = cached.get(s[2]) or ""
                if not cached_contents_:
                    if self.config.get(s[0]):
                        cached[s[2]] = lib.minify_static_contents(ftype=ftype, contents=lib.merge_files_contents([os.path.join(self.static_dir, f) for f in self.config.get(s[0]) or []]))
                        cached_contents_ = cached[s[2]]

                if _c := _context.get(s[1]):
                    cached_contents_ += lib.minify_static_contents(ftype=ftype, contents=lib.merge_files_contents([os.path.join(self.build_static_dir, f) for f in _c]))

                if cached_contents_:
                    _context["page"]["__assets"][s[2]] = "%s.%s" %  (bundlename_, ftype)
                    lib.write_file(contents=cached_contents_, dest="%s.%s" %  (filepath_, ftype))


        # Write file
        if (self.print_info):
            print_info('creating page: %s...' % filepath)
        self._context_root = lib.context_root(_context.get("page.url"))
        lib.write_file(dest=dest_file, contents=tpl.render(**_context))

    def build(self, print_info=False):
        self.print_info = print_info
        self.clean_build_dir()
        if not os.path.isdir(self.build_dir):
            os.makedirs(self.build_dir)
        self.build_static()
        self.build_pages()
