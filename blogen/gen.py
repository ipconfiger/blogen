#!/usr/bin/python
#coding=utf8
import os
import sys
import datetime
import markdown
from yaml import load, Loader
from bottle import route, run, debug, static_file
from jinja2 import Environment, FileSystemLoader
sys.path.append(os.getcwd())

PAGE_SIZE = 5
BASE_PATH = os.getcwd()
INDEX_PATH = os.sep.join([BASE_PATH, "index"])
POSTS_BASE = os.sep.join([BASE_PATH, "posts"])
HTML_BASE = os.sep.join([BASE_PATH, "html"])
STATIC_BASE = os.sep.join([BASE_PATH, "static"])
TEMPLATE_BASE = os.sep.join([BASE_PATH, "templates"])
CONFIG = {}
env = Environment(loader=FileSystemLoader(TEMPLATE_BASE))

def touni(data):
    for enc in ['utf8','gbk']:
        try:
            if isinstance(data, unicode):return data
            return data.decode(enc)
        except:
            pass

def tob(data, enc='utf8'):
    if isinstance(data, unicode):return data.encode(enc)
    return data


def load_config():
    with open(BASE_PATH+"/settings.yaml",'r') as f:
        return load(f,Loader=Loader)


def post_path(file_name,folder):
    prefix = file_name.split(".")[0]
    return os.sep.join([BASE_PATH,folder,"%s.%s"%(prefix,"md" if folder == "posts" else "html")])

def get_file(file_path):
    with open(file_path,"r") as f:
        return f.read()

def save_file(file_path, content):
    with open(file_path,"w") as f:
        f.write(tob(content))

class Posts(object):
    def __init__(self, filename, title, post_date, md_content):
        self.filename = touni(filename)
        self.title = touni(title)
        self.post_date = post_date
        self.md_content = touni(md_content)
        self.html_content = markdown.markdown(touni(md_content))

    def __repr__(self):
        return u"filename=%s\ntitle=%s\nmd_content=%s\nhtml_content=%s\n"%(touni(self.filename),touni(self.title),touni(self.md_content),touni(self.html_content))

POSTS = []
PAGE_POSTS = []

def get_date_from_filename(file_name, time_str):
    title_spans = file_name.split("-")[:3]+time_str.split("-")
    return datetime.datetime(*map(int,title_spans))

def split_content(md_file):
    lines = md_file.split("\n")
    flags = 0
    header_lines, body_lines = [], []
    for line in lines:
        if flags == 2:
            body_lines.append(line)
        else:
            if line.strip() == "---":
                flags+=1
            else:
                header_lines.append(line)
    return dict([tuple(map( lambda item:item.strip(),line.split(":"))) for line in header_lines]),os.linesep.join(body_lines)


def load_posts():
    for mdfile_name in os.listdir(POSTS_BASE):
        header,body = split_content(get_file(post_path(mdfile_name,"posts")))
        post_time = header["post_time"]
        post_date = get_date_from_filename(mdfile_name, post_time)
        title = header["title"]
        post = Posts(mdfile_name.split(".")[0], title, post_date, body)
        POSTS.append(post)
    sorted_posts = sorted(POSTS,key=lambda item:item.post_date,reverse=True)
    total = len(sorted_posts)
    pages = (total/PAGE_SIZE)+1 if total%PAGE_SIZE else total/PAGE_SIZE
    for i in range(pages):
        start = i*PAGE_SIZE
        page = sorted_posts[start:start+PAGE_SIZE]
        PAGE_POSTS.append(page)


def render_index(page_id):
    config = CONFIG
    posts = PAGE_POSTS[page_id-1] if PAGE_POSTS else []
    total = len(POSTS)
    pages = len(PAGE_POSTS)
    page_list = [(i+1,"/index_%s.html"%(i+1)) for i in range(pages) ]
    if PAGE_POSTS:
        page_list[0] = (1,"/")
    resp = env.get_template("index.html").render(**locals())
    if page_id == 1:
        page_path = "%s.html"%INDEX_PATH
    else:
        page_path = "%s_%s.html"%(INDEX_PATH,page_id)
    save_file(page_path,resp)
    return resp

def render_post(file_name):
    config = CONFIG
    post =(lambda item:item[0] if item else None)([p for p in POSTS if p.filename == touni(file_name)])
    resp = env.get_template("post.html").render(**locals())
    save_file(post_path(tob(file_name)+".md","html"),resp)
    return resp


@route('/static/<folder>/<file_name>')
def static_root(folder,file_name):
    return static_file(file_name,STATIC_BASE+"/"+folder)

@route("/html/<file_name>.html")
def show_post(file_name):
    return render_post(file_name)

@route('/')
def index():
    return render_index(1)

@route('/index_<page_id>.html')
def index_p(page_id):
    return render_index(int(page_id))


def open_server():
    debug(True)
    global  CONFIG
    CONFIG = load_config()
    if "page_size" in CONFIG:
        global PAGE_SIZE
        PAGE_SIZE = int(CONFIG["page_size"])
    port = 5000
    if len(sys.argv)>2:
        port = int(sys.argv[2])
    load_posts()
    run(host="0.0.0.0", port=port, reloader=True)

def post_posts():
    if len(sys.argv)<3:
        print "not enough arguments(file title is needed)"
        sys.exit(1)
        return
    file_title = touni(sys.argv[2].strip())
    dn = datetime.datetime.now()
    title_spans = file_title.split("-")
    if len(title_spans)>3 and sum([title_spans[0].isdigit(),title_spans[1].isdigit(),title_spans[2].isdigit()]) and int(title_spans[0])<=dn.year and 0<int(title_spans[1])<=12 and 0<int(title_spans[2])<=31:
        file_name = u"%s.md"%file_title.replace(" ","_")
        title = title_spans[3]
    else:
        file_name = u"%s-%s-%s-%s.md"%(dn.year,dn.month,dn.day,file_title.replace(" ","_"))
        title = file_title
    post_time = u"-".join(map(str,[dn.hour,dn.minute,dn.second]))
    file_header = u"\n".join([u"---",u"title:%s"%title,u"post_time:%s"%post_time,u"---",u"\n\n%s\n==============="%title,u"write the post body here"])
    local_path = os.sep.join([BASE_PATH,"posts",file_name])
    save_file(local_path, file_header)
    print "post file:",file_name
    print file_header
    print "write to posts folder complete!"

def rebuild_all():
    load_posts()
    for i in range(len(PAGE_POSTS)):
        render_index(i+1)
        print "page",i+1,"build ok"
    for p in POSTS:
        render_post(p.filename)
        print "page",p.filename,"build done"


def init_site():
    if len(sys.argv)<3:
        print "not enough arguments(site name is needed)"
        sys.exit(1)
        return
    site_name = touni(sys.argv[2].strip())
    config_file = "site_name: %s\npage_size: 5\n"%site_name
    save_file(BASE_PATH+"/settings.yaml",config_file)
    os.mkdir(STATIC_BASE)
    os.mkdir(TEMPLATE_BASE)
    os.mkdir(POSTS_BASE)
    os.mkdir(HTML_BASE)
    index_template = """<!DOCTYPE html>
<html>
<head>
    <title>{{ config.site_name }}</title>
</head>
<body>
{% for post in posts %}
    <dl>
        <dt><h2><a href="/html/{{ post.filename }}.html">{{ post.title }}</a></h2></dt>
        <dd>{{ post.post_date }}</dd>
    </dl>
{% endfor %}
<ul>
    {% for page_id,url in page_list %}
        <li><a href="{{ url }}">{{ page_id }}</a></li>
    {% endfor %}
</ul>
</body>
</html>
    """
    save_file(TEMPLATE_BASE+"/index.html",index_template)
    post_template = """<!DOCTYPE html>
<html>
<head>
    <title>{{ config.site_name }}-{{ post.filename }}</title>
</head>
<body>
<h1>{{ post.title }}</h1>
<div>
    {{ post.html_content|safe }}
</div>
<div>{{ post.post_date }}</div>
</body>
</html>
    """
    save_file(TEMPLATE_BASE+"/post.html",post_template)
    print "initialize done"


def print_help():
    for k,v in COMMAND.iteritems():
        print k,v[1]


COMMAND = {
    '--server':(open_server,"open preview server"),
    '--post':(post_posts,"create a new post data file"),
    '--rebuild':(rebuild_all,"rebuild all html files with markdown content"),
    '--init':(init_site,"initialize the site"),
    '-h':(print_help,"print command list"),
    'help':(print_help,"same as -h")
}

def main():
    if len(sys.argv)<2:
        print "not enough arguments(use -h for help)"
        sys.exit(1)
    else:
        command = COMMAND.get(sys.argv[1].strip(),None)
        if not command:
            print "no such command\n"
            sys.exit(1)
        else:
            command[0]()

if __name__ == '__main__':
    main()
