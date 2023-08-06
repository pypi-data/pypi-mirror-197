"""
Curation Workflow HTML for allowed-amounts schema in price transparency
"""

def get_curate_html(cat_name='main'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')

    def tbl_link(wh_name, tbl_name, ttip=''):
        return {'tooltip': ttip, 'href': f'./explore/data/{cat_name}/{wh_name}/{tbl_name}', 'target': "_blank"}

    with dot.subgraph(name='cluster_workflow') as c:
        c.body.append('label="Price Transparency: Allowed-Amount Workflow"')
        with c.subgraph(name='cluster_pt_raw') as r:
            r.body.append('label="pt_raw"')
            r.body.append('style="filled"')
            r.body.append('color="#808080"')
            r.body.append('fillcolor="#F5F5F5"')
            with r.subgraph(name='cluster_pt_raw_aa') as raa:
                raa.body.append('label="Allowed-Amount Files"')
                raa.body.append('style="filled"')
                raa.body.append('color="#808080"')
                raa.body.append('fillcolor="#DCDCDC"')
                raa.node('aa_meta', 'aa_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                raa.node('allowed_amount_file', '.../schema=allowed-amount/*.json', fillcolor='#FFFACD', style='filled', shape='folder')
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')
            s.node('aa', '', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'inr'), shape='point')
            s.node('aa_header', 'aa_header', fillcolor='#CAD9EF', style='filled')
            s.node('aa_network', 'aa_network', fillcolor='#CAD9EF', style='filled')
            s.node('out_code', 'out_code', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'out_code'))
            s.node('out_amount', 'out_amount', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'out_amount'))
        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')
            p.node('v_out_code', 'out_code', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'out_code'))
            p.node('v_out_amount', 'out_amount', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'out_amount'))

        dot.edge('allowed_amount_file', 'aa', ltail='cluster_pt_raw_aa')

        dot.edge('aa', 'aa_network')
        dot.edge('aa', 'aa_header')


        dot.edge('aa_network', 'out_amount')
        dot.edge('aa_header', 'out_code')

        dot.edge('aa_network', 'out_code')
        dot.edge('aa_header', 'out_amount')

        dot.edge('out_code', 'v_out_code')
        dot.edge('out_amount', 'v_out_amount')

    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="900pt" aligned=center', html)
    html = re.sub(r'font-size=\"14.00\">Fact Tables</text>', 'font-size=\"12.00\">Fact Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Dimension Tables</text>', 'font-size=\"12.00\">Dimension Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">Reference Tables</text>', 'font-size=\"12.00\">Reference Tables</text>', html)
    html = re.sub(r'font-size=\"14.00\">DI Operational Tables</text>',
                  'font-size=\"12.00\">DI Operational Tables</text>', html)
    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)
    html = re.sub(r'</svg>', '</div</svg>', html)

    return html
