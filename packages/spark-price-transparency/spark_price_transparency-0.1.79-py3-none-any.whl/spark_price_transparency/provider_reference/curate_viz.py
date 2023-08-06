"""
Provider reference curation graphic
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
        c.body.append('label="Price Transparency Workflows"')
        with c.subgraph(name='cluster_pt_raw') as r:
            r.body.append('label="Database: pt_raw"')
            r.body.append('style="filled"')
            r.body.append('color="#808080"')
            r.body.append('fillcolor="#F5F5F5"')
            with r.subgraph(name='cluster_pt_raw_pr') as rpr:
                rpr.body.append('label="Provider-Reference Files"')
                rpr.body.append('style="filled"')
                rpr.body.append('color="#808080"')
                rpr.body.append('fillcolor="#DCDCDC"')
                rpr.node('pr_meta', 'pr_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                rpr.node('provider_reference_file', '.../schema=provider-reference/*.json', fillcolor='#FFFACD',
                         style='filled', shape='folder', **{'width': "4"})
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="Database: pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')

            s.node('pr_provider', 'pr_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'pr_provider'))

            s.node('in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_rate'))
            s.node('in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'in_provider'))

        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="Database: pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')
            p.node('v_in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'in_rate'))
            p.node('v_in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'in_provider'))

        dot.edge('provider_reference_file', 'pr_provider', ltail='cluster_pt_raw_pr')

        dot.edge('pr_provider', 'in_rate', style='dashed', color='blue')
        dot.edge('pr_provider', 'in_provider', style='dashed', color='blue')

        dot.edge('in_rate', 'v_in_rate')
        dot.edge('in_provider', 'v_in_provider')

    html = dot._repr_image_svg_xml()

    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="700pt" aligned=center', html)
    html = re.sub(r'Price Transparency Workflow',
                  '<a href="https://pypi.org/project/spark-price-transparency/" target="_blank">Price Transparency Workflow</a>',
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
    html = re.sub(r'Provider&#45;Reference Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/provider-reference" target="_blank">Provider&#45;Reference Files</a>',
                  html)

    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)

    return html
