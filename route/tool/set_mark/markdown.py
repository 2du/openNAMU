from . import tool

import datetime
import html
import re

class head_render:
    def __init__(self):
        self.head_level = [0, 0, 0, 0, 0, 0]
        self.toc_data = '' + \
            '<div id="toc">' + \
                '<span id="toc_title">TOC</span>' + \
                '<br>' + \
                '<br>' + \
        ''
        self.toc_num = 0

    def __call__(self, match):
        head_len_num = len(match[1])
        head_len = str(head_len_num)
        head_len_num -= 1
        head_data = match[2]
        self.head_level[head_len_num] += 1
        for i in range(head_len_num + 1, 6):
            self.head_level[i] = 0
            
        self.toc_num += 1
        toc_num_str = str(self.toc_num)
        head_level_str_2 = '.'.join([str(i) for i in self.head_level if i != 0])
        head_level_str = head_level_str_2 + '.'

        self.toc_data += '<a href="#s-' + head_level_str_2 + '">' + head_level_str + '</a> ' + head_data + '<br>'
        return '<h' + head_len + ' id="s-' + head_level_str_2 + '"><a href="#toc">' + head_level_str + '</a> ' + head_data + '</h' + head_len + '>'

    def get_toc(self):
        return self.toc_data + '</div>'

class link_render:
    def __init__(self, plus_data, include_name):
        self.str_e_link_id = 0
        self.plus_data = ''
        self.include_name = include_name

    def __call__(self, match):
        str_e_link_id = str(self.str_e_link_id)
        self.str_e_link_id += 1

        if match[1] == '!':    
            file_name = ''
            if re.search(r'^http(s)?:\/\/', match[3], flags = re.I):
                file_src = match[3]
                file_alt = match[3]
                exist = '1'
            else:
                file_name = re.search(r'^([^.]+)\.([^.]+)$', match[3])
                if file_name:
                    file_end = file_name.group(2)
                    file_name = file_name.group(1)
                else:
                    file_name = 'Test'
                    file_end = 'jpg'

                file_src = '/image/' + tool.sha224_replace(file_name) + '.' + file_end
                file_alt = 'file:' + file_name + '.' + file_end
                exist = None

            return '' + \
                '<span  class="' + self.include_name + 'file_finder" ' + \
                        'under_alt="' + file_alt + '" ' + \
                        'under_src="' + file_src + '" ' + \
                        'under_href="' + ("out_link" if exist else '/upload?name=' + tool.url_pas(file_name)) + '">' + \
                '</span>' + \
            ''
        else:
            if re.search(r'^http(s)?:\/\/', match[3], flags = re.I):
                self.plus_data += '' + \
                    'document.getElementsByName("' + self.include_name + 'set_link_' + str_e_link_id + '")[0].href = ' + \
                        '"' + match[3] + '";' + \
                    '\n' + \
                ''

                return '<a  id="out_link" ' + \
                            'href="" ' + \
                            'name="' + self.include_name + 'set_link_' + str_e_link_id + '">' + match[2] + '</a>'
            else:
                self.plus_data += '' + \
                    'document.getElementsByName("' + self.include_name + 'set_link_' + str_e_link_id + '")[0].href = ' + \
                        '"/w/' + tool.url_pas(match[3]) + '";' + \
                    '\n' + \
                ''
                self.plus_data += '' + \
                    'document.getElementsByName("' + self.include_name + 'set_link_' + str_e_link_id + '")[0].title = ' + \
                        '"' + match[3] + '";' + \
                    '\n' + \
                ''

                return '<a  class="' + self.include_name + 'link_finder" ' + \
                            'title="" ' + \
                            'href="" ' + \
                            'name="' + self.include_name + 'set_link_' + str_e_link_id + '">' + match[2] + '</a>'

    def get_plus_data(self):
        return self.plus_data

def markdown(conn, data, title, include_name):
    backlink = []
    include_name = include_name + '_' if include_name else ''
    plus_data = '' + \
        'get_link_state("' + include_name + '");\n' + \
        'get_file_state("' + include_name + '");\n' + \
    ''

    data = html.escape(data)
    data = data.replace('\r\n', '\n')
    data = '\n' + data

    head_r = r'\n(#{1,6}) ?([^\n]+)'
    head_do = head_render()
    data = re.sub(head_r, head_do, data)
    data = head_do.get_toc() + data

    link_r = r'(!)?\[((?:(?!\]\().)+)\]\(([^\]]+)\)'
    link_do = link_render(plus_data, include_name)
    data = re.sub(link_r, link_do, data)
    plus_data = link_do.get_plus_data() + plus_data

    data = re.sub(r'\*\*((?:(?!\*\*).)+)\*\*', '<b>\1</b>', data)
    data = re.sub(r'__((?:(?!__).)+)__', '<i>\1</i>', data)

    data = re.sub('^\n', '', data)
    data = re.sub('\n', '<br>', data)
    
    return [data, plus_data, backlink]