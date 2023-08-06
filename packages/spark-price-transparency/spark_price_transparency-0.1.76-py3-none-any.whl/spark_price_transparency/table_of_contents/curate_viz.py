"""
Curation Workflow HTML for table-of-contents schema in price transparency
"""


def get_curate_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')

    def tbl_link(wh_name, tbl_name, ttip=''):
        return {'tooltip': ttip, 'href': f'./explore/data/{cat_name}/{wh_name}/{tbl_name}', 'target': "_blank",
                'width': "1.5"}

    with dot.subgraph(name='cluster_workflow') as c:
        c.body.append('label="Price Transparency Workflow"')
        with c.subgraph(name='cluster_pt_raw') as r:
            r.body.append('label="Database: pt_raw"')
            r.body.append('style="filled"')
            r.body.append('color="#808080"')
            r.body.append('fillcolor="#F5F5F5"')
            with r.subgraph(name='cluster_pt_raw_toc') as rtoc:
                rtoc.body.append('label="Table-of-Contents Files"')
                rtoc.body.append('style="filled"')
                rtoc.body.append('color="#808080"')
                rtoc.body.append('fillcolor="#DCDCDC"')
                rtoc.node('toc_meta', 'toc_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                rtoc.node('table_of_contents_file', '.../schema=table-of-contents/*.json', fillcolor='#FFFACD',
                          style='filled', shape='folder', **{'width': "4"})
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="Database: pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')

            s.node('toc', '', fillcolor='#CAD9EF', style='filled', shape='point')
            s.node('toc_inr', '', fillcolor='red', style='invis', shape='point')

            s.node('toc_header', 'toc_header', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'toc_header'))
            s.node('toc_reporting', 'toc_reporting', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'toc_reporting'))

            s.node('top_analytic', 'top_analytic', fillcolor='red', style='invis', **{'width': "2"})
            s.node('index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'index_reports'))

        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="Database: pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')

            p.node('v_top_analytic', 'v_top_analytic', fillcolor='red', style='invis', **{'width': "2"})
            p.node('v_index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'index_reports'))

        dot.edge('table_of_contents_file', 'toc', ltail='cluster_pt_raw_toc')
        dot.edge('table_of_contents_file', 'toc_inr', ltail='cluster_pt_raw_toc', style="invis")

        dot.edge('toc', 'toc_header')
        dot.edge('toc', 'toc_reporting')

        dot.edge('toc_header', 'top_analytic', style="invis")
        dot.edge('toc_header', 'index_reports')
        dot.edge('toc_reporting', 'index_reports')

        dot.edge('top_analytic', 'v_top_analytic', style="invis")
        dot.edge('index_reports', 'v_index_reports')

    html = dot._repr_image_svg_xml()

    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="900pt" aligned=center', html)
    html = re.sub(r'Price Transparency Workflow',
                  '<a href="https://pypi.org/project/spark-price-transparency/" ' +
                  'target="_blank">Price Transparency Workflow</a>',
                  html)
    html = re.sub(r'Database: pt_raw',
                  f'<a href="./explore/data/{cat_name}/pt_raw" target="_blank">Database&#58; pt&#95;raw</a>',
                  html)
    html = re.sub(r'Database: pt_stage',
                  f'<a href="./explore/data/{cat_name}/pt_stage" target="_blank">Database&#58; pt&#95;stage</a>',
                  html)
    html = re.sub(r'Database: pt',
                  f'<a href="./explore/data/{cat_name}/pt" target="_blank">Database&#58; pt</a>',
                  html)
    html = re.sub(r'Table&#45;of&#45;Contents Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/' +
                  'table-of-contents" target="_blank">Table&#45;of&#45;Contents Files</a>',
                  html)

    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)

    return html
