# coding:utf-8
# @文件: report_utils.py
# @创建者：州的先生
# #日期：2019/12/7
# 博客地址：zmister.com
# MrDoc文集文档导出相关功能代码
import datetime
import os
import re
import shutil
import subprocess
import sys
import time
import traceback

import django
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.wsgi import get_wsgi_application

from app_doc.models import *

sys.path.extend([r'F:\pythonproject\MrDoc', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MrDoc.settings")
application = get_wsgi_application()
django.setup()


# 导出MD文件压缩包
class ReportMD():
    def __init__(self, project_id):
        # 查询文集信息
        self.pro_id = project_id
        project_data = Project.objects.get(pk=project_id)

        # 文集名称
        self.project_name = "{0}_{1}_{2}".format(
            project_data.create_user,
            project_data.name,
            str(datetime.date.today())
        )

        # 判断MD导出临时文件夹是否存在
        if os.path.exists(settings.MEDIA_ROOT + "/reportmd_temp") is False:
            os.mkdir(settings.MEDIA_ROOT + "/reportmd_temp")

        # 判断文集名称文件夹是否存在
        self.project_path = settings.MEDIA_ROOT + \
            "/reportmd_temp/{}".format(self.project_name)
        is_fold = os.path.exists(self.project_path)
        if is_fold is False:
            os.mkdir(self.project_path)

        # 判断是否存在静态文件文件夹
        self.media_path = settings.MEDIA_ROOT + \
            "/reportmd_temp/{}/media".format(self.project_name)
        is_media = os.path.exists(self.media_path)
        if is_media is False:
            os.mkdir(self.media_path)

    def work(self):
        # 读取指定文集的文档数据
        data = Doc.objects.filter(
            top_doc=self.pro_id, parent_doc=0).order_by("sort")
        # 遍历文档
        for d in data:
            md_name = d.name
            md_content = d.pre_content
            md_content = self.operat_md_media(md_content)

            # 新建MD文件
            with open('{}/{}.md'.format(self.project_path, md_name), 'w', encoding='utf-8') as files:
                files.write(md_content)

            # 查询二级文档
            data_2 = Doc.objects.filter(parent_doc=d.id).order_by("sort")
            for d2 in data_2:
                md_name_2 = d2.name
                md_content_2 = d2.pre_content

                md_content_2 = self.operat_md_media(md_content_2)

                # 新建MD文件
                with open('{}/{}.md'.format(self.project_path, md_name_2), 'w', encoding='utf-8') as files:
                    files.write(md_content_2)

                # 获取第三级文档
                data_3 = Doc.objects.filter(parent_doc=d2.id).order_by("sort")
                for d3 in data_3:
                    md_name_3 = d3.name
                    md_content_3 = d3.pre_content

                    md_content_3 = self.operat_md_media(md_content_3)

                    # 新建MD文件
                    with open('{}/{}.md'.format(self.project_path, md_name_3), 'w', encoding='utf-8') as files:
                        files.write(md_content_3)

        # 压缩文件
        md_file = shutil.make_archive(
            base_name=self.project_path,
            format='zip',
            root_dir=self.project_path
        )
        print(md_file)
        # 删除文件夹
        shutil.rmtree(self.project_path)

        return "{}.zip".format(self.project_path)

    # 处理MD内容中的静态文件
    def operat_md_media(self, md_content):
        # 查找MD内容中的静态文件
        pattern = r"\!\[.*?\]\(.*?\)"
        media_list = re.findall(pattern, md_content)
        # print(media_list)
        # 存在静态文件,进行遍历
        if len(media_list) > 0:
            for media in media_list:
                media_filename = media.split("(")[-1].split(")")[0]  # 媒体文件的文件名
                # 对本地静态文件进行复制
                if media_filename.startswith("/"):
                    sub_folder = "/" + \
                        media_filename.split("/")[3]  # 获取子文件夹的名称
                    is_sub_folder = os.path.exists(self.media_path+sub_folder)
                    # 创建子文件夹
                    if is_sub_folder is False:
                        os.mkdir(self.media_path+sub_folder)
                    # 替换MD内容的静态文件链接
                    md_content = md_content.replace(
                        media_filename, "." + media_filename)
                    # 复制静态文件到指定文件夹
                    try:
                        shutil.copy(settings.BASE_DIR +
                                    media_filename, self.media_path+sub_folder)
                    except FileNotFoundError:
                        pass
                # 不存在本地静态文件，直接返回MD内容
                # else:
                #     print("没有本地静态文件")
            return md_content
        # 不存在静态文件，直接返回MD内容
        else:
            return md_content


# 导出EPUB
class ReportEPUB():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)
        self.base_path = settings.MEDIA_ROOT + '/report/{}/'.format(project_id)

        # 创建相关目录
        if os.path.exists(self.base_path + '/OEBPS') is False:
            os.makedirs(self.base_path + '/OEBPS')
        if os.path.exists(self.base_path + '/OEBPS/Images') is False:
            os.makedirs(self.base_path + '/OEBPS/Images')
        if os.path.exists(self.base_path + '/OEBPS/Text') is False:
            os.makedirs(self.base_path + '/OEBPS/Text')
        if os.path.exists(self.base_path + '/OEBPS/Styles') is False:
            os.makedirs(self.base_path + '/OEBPS/Styles')
        if os.path.exists(self.base_path + '/META-INF') is False:
            os.makedirs(self.base_path + '/META-INF')

        # 复制样式文件到相关目录
        shutil.copyfile(settings.BASE_DIR+'/static/report_epub/style.css',
                        self.base_path + '/OEBPS/Styles/style.css')
        shutil.copyfile(settings.BASE_DIR+'/static/katex/katex.min.css',
                        self.base_path + '/OEBPS/Styles/katex.css')
        shutil.copyfile(settings.BASE_DIR+'/static/editor.md/css/editormd.min.css/',
                        self.base_path + '/OEBPS/Styles/editormd.css')
        # 复制封面图片到相关目录
        shutil.copyfile(settings.BASE_DIR+'/static/report_epub/epub_cover1.jpg',
                        self.base_path + '/OEBPS/Images/epub_cover1.jpg')

    # 将文档内容写入HTML文件
    def write_html(self, d, html_str):
        # 使用BeautifulSoup解析拼接好的HTML文本
        html_soup = BeautifulSoup(html_str, 'lxml')
        src_tag = html_soup.find_all(
            lambda tag: tag.has_attr("src"))  # 查找所有包含src的标签
        code_tag = html_soup.find_all(name="code")
        # print(src_tag)

        # 添加css样式标签
        style_link = html_soup.new_tag(
            name='link', href="../Styles/style.css", rel="stylesheet", type="text/css")
        katex_link = html_soup.new_tag(
            name='link', href='../Styles/katex.css', rel="stylesheet", type="text/css")
        editormd_link = html_soup.new_tag(
            name='link', href='../Styles/editormd.css', rel="stylesheet", type="text/css")
        html_soup.body.insert_before(style_link)
        html_soup.body.insert_before(katex_link)
        # html_soup.body.insert_before(editormd_link)

        # 添加xlm标签声明
        # html_soup.html.insert_before('<?xml version="1.0" encoding="UTF-8"?>')
        # 添加html标签的xmlns属性
        html_soup.html['xmlns'] = "http://www.w3.org/1999/xhtml"

        # 替换HTML文本中静态文件的相对链接为绝对链接
        for src in src_tag:
            if src['src'].startswith("/"):
                src_path = src['src']  # 媒体文件原始路径
                src_filename = src['src'].split("/")[-1]  # 媒体文件名
                src['src'] = '../Images/' + src_filename  # 媒体文件在EPUB中的路径
                # 复制文件到epub的Images文件夹
                try:
                    shutil.copyfile(
                        src=settings.BASE_DIR + src_path,
                        dst=self.base_path + '/OEBPS/Images/' + src_filename
                    )
                except FileNotFoundError as e:
                    pass

        # 替换code标签的内容
        # for code in code_tag:
        #     code_str = code.get_text()
        #     code.clear()
        #     code['class'] = ''
        #     code.string = code_str

        # 创建写入临时HTML文件
        temp_file_path = self.base_path + '/OEBPS/Text/{0}.xhtml'.format(d.id)
        with open(temp_file_path, 'a+', encoding='utf-8') as htmlfile:
            htmlfile.write(
                '<?xml version="1.0" encoding="UTF-8"?>' + str(html_soup))

    # 生成文档HTML
    def generate_html(self):
        # 查询文档
        data = Doc.objects.filter(
            top_doc=self.project.id, parent_doc=0, status=1).order_by("sort")
        self.toc_list = [
            {
                'id': 0,
                'link': 'Text/toc_summary.xhtml',
                'pid': 0,
                'title': '目录'
            }
        ]
        nav_str = '''<navMap>'''
        toc_summary_str = '''<ul>'''
        nav_num = 1
        # content.opf相关
        manifest = '''<item id="book_cover" href="Text/book_cover.xhtml" media-type="application/xhtml+xml"/>
        <item id="book_title" href="Text/book_title.xhtml" media-type="application/xhtml+xml"/>
        <item id="book_desc" href="Text/book_desc.xhtml" media-type="application/xhtml+xml"/>
        <item id="toc_summary" href="Text/toc_summary.xhtml" media-type="application/xhtml+xml"/>
        '''
        spine = '<itemref idref="book_cover" linear="no"/><itemref idref="book_title"/><itemref idref="book_desc"/><itemref idref="toc_summary"/>'

        for d in data:
            # 拼接HTML字符串
            html_str = "<h1 style='page-break-before: always;'>{}</h1>".format(
                d.name)
            html_str += d.content
            self.write_html(d=d, html_str=html_str)  # 生成HTML
            # 生成HTML的目录位置
            toc = {
                'id': d.id,
                'link': '{}.xhtml'.format(d.id),
                'pid': d.parent_doc,
                'title': d.name
            }
            self.toc_list.append(toc)

            # nav
            toc_nav = '''<navPoint id="np_{nav_num}" playOrder="{nav_num}">
                    <navLabel><text>{title}</text></navLabel>
                    <content src="Text/{file}"/>
                '''.format(nav_num=nav_num, title=d.name, file=toc['link'])
            nav_str += toc_nav

            # toc_summary
            toc_summary_str += '''<li><a href="./{}">{}</a>'''.format(
                toc['link'], toc['title'])
            # content.opf
            manifest += '<item id="{}" href="Text/{}.xhtml" media-type="application/xhtml+xml"/>'.format(
                d.id, d.id)
            spine += '<itemref idref="{}"/>'.format(d.id)

            nav_num += 1

            # 获取第二级文档
            data_2 = Doc.objects.filter(
                parent_doc=d.id, status=1).order_by("sort")
            if data_2.count() > 0:
                toc_summary_str += '<ul>'
            for d2 in data_2:
                html_str = "<h1>{}</h1>".format(d2.name)
                html_str += d2.content
                self.write_html(d=d2, html_str=html_str)
                # 生成HTML的目录位置
                toc = {
                    'id': d2.id,
                    'link': '{}.xhtml'.format(d2.id),
                    'pid': d2.parent_doc,
                    'title': d2.name
                }
                self.toc_list.append(toc)
                toc_nav = '''<navPoint id="np_{nav_num}" playOrder="{nav_num}">
                                    <navLabel><text>{title}</text></navLabel>
                                    <content src="Text/{file}"/>
                                '''.format(nav_num=nav_num, title=d2.name, file=toc['link'])
                nav_str += toc_nav

                # toc_summary
                toc_summary_str += '''<li><a href="./{}">{}</a>'''.format(
                    toc['link'], toc['title'])
                # content.opf
                manifest += '<item id="{}" href="Text/{}.xhtml" media-type="application/xhtml+xml"/>'.format(
                    d2.id, d2.id)
                spine += '<itemref idref="{}"/>'.format(d2.id)

                nav_num += 1

                # 获取第三级文档
                data_3 = Doc.objects.filter(
                    parent_doc=d2.id, status=1).order_by("sort")
                if data_3.count() > 0:
                    toc_summary_str += '<ul>'
                for d3 in data_3:
                    html_str = "<h1>{}</h1>".format(d3.name)
                    html_str += d3.content
                    self.write_html(d=d3, html_str=html_str)
                    # 生成HTML的目录位置
                    toc = {
                        'id': d3.id,
                        'link': '{}.xhtml'.format(d3.id),
                        'pid': d3.parent_doc,
                        'title': d3.name
                    }
                    self.toc_list.append(toc)

                    toc_nav = '''<navPoint id="np_{nav_num}" playOrder="{nav_num}">
                                    <navLabel><text>{title}</text></navLabel>
                                    <content src="Text/{file}"/>
                                </navPoint>
                        '''.format(nav_num=nav_num, title=d3.name, file=toc['link'])
                    nav_str += toc_nav

                    # toc_summary
                    toc_summary_str += '''<li><a href="./{}">{}</a></li>'''.format(
                        toc['link'], toc['title'])
                    # content.opf
                    manifest += '<item id="{}" href="Text/{}.xhtml" media-type="application/xhtml+xml"/>'.format(d3.id,
                                                                                                                 d3.id)
                    spine += '<itemref idref="{}"/>'.format(d3.id)

                    nav_num += 1

                nav_str += "</navPoint>"
                if data_3.count() > 0:
                    toc_summary_str += "</ul></li>"
                else:
                    toc_summary_str += "</li>"

            nav_str += "</navPoint>"
            if data_2.count() > 0:
                toc_summary_str += "</ul></li>"
            else:
                toc_summary_str += "</li>"

        nav_str += '</navMap>'
        toc_summary_str += '</ul>'

        # print(nav_str)
        # print(toc_summary_str)
        self.nav_str = nav_str
        self.toc_summary_str = toc_summary_str
        # self.config_json['toc'] = self.toc_list
        self.manifest = manifest
        self.spine = spine

    # 生成书籍标题的描述HTML文件
    def generate_title_html(self):
        title_str = '''<?xml version="1.0" encoding="UTF-8"?>
            <html xmlns="http://www.w3.org/1999/xhtml">
              <head>
                <title>书籍标题</title>
                <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
                <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
              </head>
              <body class="bookname">
                  <div class="main">
                    <h1 class="title"">{title}</h1>
                    <p class="author"><b>{author} 著</b></p><br>
                    <p class="author">{create_time}</p>
                    <p class="book-src">本书籍由<a href='http://mrdoc.zmister.com'>MrDoc(mrdoc.zmister.com)</a>生成</p>
                  </div>
            </body>
            </html>
        '''.format(
            title=self.project.name,
            author=self.project.create_user,
            create_time=time.strftime(
                '%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        )
        with open(self.base_path+'/OEBPS/Text/book_title.xhtml', 'a+', encoding='utf-8') as file:
            file.write(title_str)

        desc_str = '''<?xml version="1.0" encoding="UTF-8"?>
            <html xmlns="http://www.w3.org/1999/xhtml">
              <head>
                <title>简介</title>
                <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
                <link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
              </head>
              <body class="bookdesc">
                  <div class="main">
                    <p class="title">书籍简介</p>
                    <p class="subtitle">{desc}</p>
                  </div>
            </body>
            </html>
        '''.format(desc=self.project.intro)
        with open(self.base_path+'/OEBPS/Text/book_desc.xhtml', 'a+', encoding='utf-8') as file:
            file.write(desc_str)

    # 生成元信息container.xml文件
    def generate_metainfo(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
            <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container" >
                <rootfiles>
                    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
                </rootfiles>
            </container>
            '''
        folder = self.base_path + '/META-INF'
        with open(folder+'/container.xml', 'a+', encoding='utf-8') as metafile:
            metafile.write(xml)

    # 生成元类型mimetype文件
    def generate_metatype(self):
        with open(self.base_path+'/mimetype', 'a+', encoding='utf-8') as metatype:
            metatype.write('application/epub+zip')

    # 生成封面
    def generate_cover(self):
        xml_str = '''<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh">
            <head>
              <title>封面</title>
            <style type="text/css">
            svg {padding: 0pt; margin:0pt}
            body { text-align: center; padding:0pt; margin: 0pt; }
            </style>
            </head>
            <body>
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 628 892" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
                  <image height="892" width="628" xlink:href="../Images/epub_cover1.jpg"/>
                </svg>
              </div>
            </body>
            </html>
        '''
        with open(self.base_path + '/OEBPS/Text/book_cover.xhtml', 'a+', encoding='utf-8') as cover:
            cover.write(xml_str)

    # 生成文档目录.ncx文件
    def generate_toc_ncx(self):
        ncx = '''
        <?xml version='1.0' encoding='utf-8'?>
            <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">
              <head>
                <meta name="dtb:uid" content="urn:uuid:12345"/>
                <meta name="dtb:depth" content="1"/>
                <meta name="dtb:totalPageCount" content="0"/>
                <meta name="dtb:maxPageNumber" content="0"/>
              </head>
              <docTitle>
                <text>{title}</text>
              </docTitle>
              {nav_map}
            </ncx>
        '''.format(title=self.project.name, nav_map=self.nav_str)

        with open(self.base_path+'/OEBPS/toc.ncx', 'a+', encoding='utf-8') as file:
            file.write(ncx)

    # 生成文档目录toc_summary.html文件
    def generate_toc_html(self):
        summary = '''<?xml version="1.0" encoding="UTF-8"?>
            <html lang="zh-CN">
            <head>
                <meta charset="utf-8">
                <title>目录</title>
                <style>
                    body{margin: 0px;padding: 0px;}h1{text-align: center;padding: 0px;margin: 0px;}ul,li{list-style: none;}ul{padding-left:0px;}li>ul{padding-left: 2em;}
                    a{text-decoration: none;color: #4183c4;text-decoration: none;font-size: 16px;line-height: 28px;}
                </style>
            </head>
            <body>
                <h1>目&nbsp;&nbsp;&nbsp;&nbsp;录</h1>
                %s
            </body>
            </html>
        ''' % (self.toc_summary_str)

        with open(self.base_path+'/OEBPS/Text/toc_summary.xhtml', 'a+', encoding='utf-8') as file:
            file.write(summary)

    # 生成content.opf文件
    def generate_opf(self):
        content_info = '''<?xml version="1.0" encoding="utf-8" ?>
            <package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid" >
              <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
                <dc:title>{title}</dc:title>
                <dc:language>zh</dc:language>
                <dc:creator>{creator}</dc:creator>
                <dc:identifier id="bookid">urn:uuid:12345</dc:identifier>
                <dc:publisher>MrDoc制作</dc:publisher>
                <dc:date opf:event="publication">{create_time}</dc:date>
                <dc:description>{desc}</dc:description>
                <meta name="cover" content="cover_img" />
                <meta name="output encoding" content="utf-8" />
                <meta name="primary-writing-mode" content="horizontal-lr" />
              </metadata>
              <manifest>
                  {manifest}
                <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
                <item id="css" href="stylesheet.css" media-type="text/css"/>
                <item id="cover_img" media-type="image/jpeg" href="Images/epub_cover1.jpg" />
              </manifest>
              <spine toc="ncx">
                  {spine}
              </spine>
              <guide>
                <reference type="toc" title="目录" href="Text/toc_summary.xhtml" />
                <reference href="Text/book_cover.xhtml" type="cover" title="封面"/>
              </guide>
            </package>
            '''

        with open(self.base_path+'/OEBPS/content.opf', 'a+', encoding='utf-8') as file:
            file.write(
                content_info.format(
                    title=self.project.name,
                    creator=self.project.create_user,
                    create_time=str(datetime.date.today()),
                    desc=self.project.intro,
                    manifest=self.manifest,
                    spine=self.spine,
                )
            )

    # 生成epub文件
    def generate_epub(self):
        try:
            # 生成ZIP压缩文件
            zipfile_name = settings.MEDIA_ROOT + \
                '/report/{}'.format(self.project.name) + \
                '_'+str(int(time.time()))
            zip_name = shutil.make_archive(
                base_name=zipfile_name,
                format='zip',
                root_dir=settings.MEDIA_ROOT +
                '/report/{}'.format(self.project.id)
            )
            # print(zip_name)
            # 修改zip压缩文件后缀为EPUB
            os.rename(zip_name, zipfile_name+'.epub')
            # 删除生成的临时文件夹
            shutil.rmtree(self.base_path)
            return zipfile_name
        except Exception as e:
            if settings.DEBUG:
                print(traceback.print_exc())
            return None

    def work(self):
        self.generate_html()  # 生成HTML
        self.generate_metainfo()  # 生成元信息
        self.generate_metatype()  # 生成元类型
        self.generate_toc_ncx()  # 生成目录ncx
        self.generate_toc_html()  # 生成目录html
        self.generate_cover()  # 生成封面html
        self.generate_title_html()  # 生产书籍的标题页和简介页
        self.generate_opf()  # 生成content.opf
        epub_file = self.generate_epub()
        return epub_file

# 导出Docx


class ReportDocx():
    def __init__(self, project_id):
        self.project = Project.objects.get(id=project_id)
        self.base_path = settings.MEDIA_ROOT + '/report/{}/'.format(project_id)

        self.content_str = ""
        self.doc_str = """<html xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:w="urn:schemas-microsoft-com:office:word"
            xmlns="http://www.w3.org/TR/REC-html40">
            <head><meta http-equiv=Content-Type content="text/html; charset=utf-8">
            <style type="text/css">
                table {
                    border-collapse: collapse;
                    border: none;
                    width: 100%;
                }
                td,tr {
                    border: solid #CCC 1px;
                    padding:3px;
                    font-size:9pt;
                }
                .codestyle{
                    word-break: break-all;
                    mso-highlight:rgb(252, 252, 252);
                    padding-left: 5px; background-color: rgb(252, 252, 252); border: 1px solid rgb(225, 225, 232);
                }
                img {
                    width:100;
                }
                /*预格式*/
                pre {
                  padding: 10px;
                  background: #f6f6f6;
                  border: 1px solid #ddd;
                  white-space: pre-wrap;
                  word-wrap: break-word;
                  white-space: -moz-pre-wrap;
                  white-space: -o-pre-wrap;
                }
                /*块代码*/
                pre code {
                  border: none;
                  background: none;
                }
                pre ol {
                  padding-left: 2.5em;
                  margin: 0;
                }
                /*行内代码*/
                code {
                  border: 1px solid #ddd;
                  background: #f6f6f6;
                  padding: 3px;
                  border-radius: 3px;
                  font-size: 14px;
                }
                /* 引用块 */
                blockquote {
                  color: #666;
                  border-left: 4px solid #ddd;
                  padding-left: 20px;
                  margin-left: 0;
                  font-size: 14px;
                  font-style: italic;
                }
                /* 表格 */
                table {
                  display: block;
                  width: 100%;
                  overflow: auto;
                  word-break: normal;
                  word-break: keep-all;
                  margin-bottom: 16px;
                }
                thead {
                  display: table-header-group;
                  vertical-align: middle;
                  border-color: inherit;
                }
                table thead tr {
                  background-color: #F8F8F8;
                }
                table th, table td {
                  padding: 6px 13px;
                  border: 1px solid #ddd;
                }
                /*公式*/
                p.editormd-tex {
                  text-align: center;
                }
            </style>
            <meta name=ProgId content=Word.Document>
            <meta name=Generator content="Microsoft Word 11">
            <meta name=Originator content="Microsoft Word 11">
            <xml><w:WordDocument><w:View>Print</w:View></xml></head>
            <body>
        """

    def work(self):
        # 拼接HTML字符串
        data = Doc.objects.filter(
            top_doc=self.project.id, parent_doc=0).order_by("sort")
        for d in data:
            # print(d.name,d.content)
            self.content_str += "<h1 style='page-break-before: always;'>{}</h1>".format(
                d.name)
            self.content_str += d.content
            # 获取第二级文档
            data_2 = Doc.objects.filter(parent_doc=d.id).order_by("sort")
            for d2 in data_2:
                self.content_str += "<h1>{}</h1>".format(d2.name)
                self.content_str += d2.content
                # 获取第三级文档
                data_3 = Doc.objects.filter(parent_doc=d2.id).order_by("sort")
                for d3 in data_3:
                    # print(d3.name,d3.content)
                    self.content_str += "<h1>{}</h1>".format(d3.name)
                    self.content_str += d3.content

        # 使用BeautifulSoup解析拼接好的HTML文本
        soup = BeautifulSoup(self.content_str, 'lxml')
        src_tag = soup.find_all(
            lambda tag: tag.has_attr("src"))  # 查找所有包含src的标签
        print(src_tag)

        # 替换HTML文本中静态文件的相对链接为绝对链接
        for src in src_tag:
            if src['src'].startswith("/"):
                src['src'] = settings.BASE_DIR + src['src']

        is_folder = os.path.exists(self.base_path)
        # 创建文件夹
        if is_folder is False:
            os.mkdir(self.base_path)
        temp_file_name = str(datetime.datetime.today()).replace(
            ':', '-').replace(' ', '-').replace('.', '')
        temp_file_path = self.base_path + '/{0}.docx'.format(temp_file_name)

        with open(temp_file_path, 'a+', encoding='utf-8') as htmlfile:
            htmlfile.write(self.doc_str + self.content_str + "</body></html>")


if __name__ == '__main__':
    # app = ReportMD(
    #     project_id=7
    # )
    # app.work()
    app = ReportEPUB(project_id=20)
    app.work()
    # app = ReportDocx(project_id=20)
    # app.work()
