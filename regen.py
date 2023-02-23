#!/usr/bin/python3

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def write_autogenerated(out):
    out.write('{%comment%}\nAUTOGENERATED FILE, please run ./regen.py to regenerate it\n{%endcomment%}\n\n')

def write_status_tag(out, name):
    out.write('{%% include_cached status.liquid status=%s %%}' % name)

def filter_intop(data):
    return {k: v for k, v in data.items() if 'intop' in v and v['intop']}.items()

def write_header(out, data):
    for (k, v) in filter_intop(data):
        out.write('<th>%s</th>\n' % (v['name']))

def write_header_nested(out, data):
    for (k, v) in filter_intop(data):
        if 'items' in v and (intops := len(filter_intop(v['items']))):
            out.write('<th colspan="%d">%s</th>\n' % (intops,v['name']))
        else:
            out.write('<th rowspan="2">%s</th>\n' % (v['name']))

    out.write('</tr>\n')

    out.write('<tr>\n')
    for (k, v) in data.items():
        if not 'items' in v:
            continue
        if 'items' in v:
            write_header(out, v['items'])

def write_layout(out, data, prefix, wrap=True):
    for (k, v) in data.items():
        if not wrap:
            wrap = True
            out.write('    ')
        else:
            out.write('<tr>')
        out.write('<th>%s</th>' % v['name'])
        write_status_tag(out, '%s-%s' % (prefix, k))
        out.write('</tr>\n')

def write_layout_nested(out, data, prefix):
    for (k, v) in data.items():
        if 'items' in v:
            out.write('<th rowspan="%d">%s</th>\n' % (len(v['items']), v['name']))
            write_layout(out, v['items'], prefix + '-' + k, wrap = False)
        else:
            out.write('<tr><th colspan="2">%s</th>' % (v['name']))
            write_status_tag(out, '%s-%s' % (prefix, k))
            out.write('</tr>\n')

def write_status(out, data, prefix):
    for (k, v) in filter_intop(data):
        if 'items' in v and len(filter_intop(v['items'])):
            write_status(out, v['items'], prefix + '-' + k)
        else:
            write_status_tag(out, '%s-%s' % (prefix, k))
            out.write('\n')

with open('soc.yaml', "r") as file:
    data = load(file, Loader=Loader)

    has_nested = False
    for (k, v) in data.items():
        if 'items' in v:
            has_nested = True
            break

    with open('_includes/index_soc_header.liquid', 'w') as out:
        write_autogenerated(out)
        out.write('<tr>\n')
        if has_nested:
            out.write('<th rowspan="2">Platform</th>\n')
            write_header_nested(out, data)
        else:
            out.write('<th>Platform</th>\n')
            write_header(out, data)
        out.write('</tr>\n')

    with open('_includes/index_soc_status.liquid', 'w') as out:
        write_autogenerated(out)
        write_status(out, data, 'd.status')

    with open('_includes/layout_soc.liquid', 'w') as out:
        write_autogenerated(out)
        if has_nested:
            write_layout_nested(out, data, 'page.status')
        else:
            write_layout(out, data, 'page.status')

with open('pmic.yaml', "r") as file:
    data = load(file, Loader=Loader)

    has_nested = False
    for (k, v) in data.items():
        if 'items' in v:
            has_nested = True
            break

    with open('_includes/index_pmic_header.liquid', 'w') as out:
        write_autogenerated(out)
        out.write('<tr>\n')
        if has_nested:
            out.write('<th rowspan="2">Platform</th>\n')
            write_header_nested(out, data)
        else:
            out.write('<th>Platform</th>\n')
            write_header(out, data)
        out.write('</tr>\n')

    with open('_includes/index_pmic_status.liquid', 'w') as out:
        write_autogenerated(out)
        write_status(out, data, 'd.pmic')

    with open('_includes/layout_pmic.liquid', 'w') as out:
        write_autogenerated(out)
        if has_nested:
            write_layout_nested(out, data, 'page.pmic')
        else:
            write_layout(out, data, 'page.pmic')
