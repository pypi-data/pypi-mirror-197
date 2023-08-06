"""
End 2 End workflow graphic for all schemas in price transparency
"""


def get_end2end_html(cat_name='hive_metastore'):
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
        c.body.append('label="Price Transparency End-to-End Workflow"')
        with c.subgraph(name='cluster_toc') as toc:
            toc.body.append('style="invis"')
            toc.node('table_of_contents_file', 'table_of_contents', fillcolor='#FFFACD', style='filled', shape='folder',
                     **{'width': "2"})
            toc.node('in_network_rates_file', 'in_network_rates', fillcolor='#FFFACD', style='filled', shape='folder',
                     **{'width': "2"})
            toc.node('provider_reference_file', 'provider_reference', fillcolor='#FFFACD', style='filled',
                     shape='folder', **{'width': "2"})
            toc.node('allowed_amount_file', 'allowed_amount', fillcolor='#FFFACD', style='filled', shape='folder',
                     **{'width': "2"})

            toc.node('toc', '', fillcolor='#CAD9EF', style='filled', shape='point')
            toc.node('inr', '', fillcolor='#CAD9EF', style='filled', shape='point')
            toc.node('inr', '', fillcolor='#CAD9EF', style='filled', shape='point')
            toc.node('aa', '', fillcolor='#CAD9EF', style='filled', shape='point')

            toc.node('toc_header', 'toc_header', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'toc_header'))
            toc.node('toc_reporting', 'toc_reporting', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'toc_reporting'))
            toc.node('inr_header', 'inr_header', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'inr_header'))
            toc.node('inr_network', 'inr_network', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'inr_network'))
            toc.node('inr_provider', 'inr_provider', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'inr_provider'))

            toc.node('aa_header', 'aa_header', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'aa_header'))
            toc.node('aa_network', 'aa_network', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'aa_network'))

            toc.node('index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'index_reports'))
            toc.node('in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'in_coverage'))
            toc.node('in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_rate'))
            toc.node('in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'in_provider'))
            toc.node('in_pr_loc', 'in_pr_loc', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_pr_loc'))
            toc.node('out_rate', 'out_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'out_rate'))
            toc.node('out_provider', 'out_provider', fillcolor='#CAD9EF', style='filled',
                     **tbl_link('pt_stage', 'out_provider'))

        with c.subgraph(name='cluster_pr') as pr:
            pr.body.append('style="invis"')
            pr.node('pr_provider1', 'pr_provider', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'pr_provider'))
            pr.node('pr_provider2', 'pr_provider', fillcolor='#CAD9EF', style='invis')

    dot.edge('provider_reference_file', 'pr_provider1', ltail='cluster_toc', lhead='cluster_pr', style="invis")

    dot.edge('table_of_contents_file', 'toc')

    dot.edge('toc', 'toc_header')
    dot.edge('toc', 'toc_reporting')

    dot.edge('toc_header', 'index_reports')
    dot.edge('toc_reporting', 'index_reports')

    dot.edge('index_reports', 'allowed_amount_file')
    dot.edge('index_reports', 'in_network_rates_file')

    dot.edge('allowed_amount_file', 'aa')
    dot.edge('aa', 'aa_header')
    dot.edge('aa', 'aa_network')
    dot.edge('aa_header', 'out_rate')
    dot.edge('aa_network', 'out_provider')
    dot.edge('aa_network', 'out_rate')
    dot.edge('aa_header', 'out_provider')

    dot.edge('in_network_rates_file', 'inr')
    dot.edge('inr', 'inr_header')
    dot.edge('inr', 'inr_network')
    dot.edge('inr', 'inr_provider')

    dot.edge('inr_header', 'in_coverage')
    dot.edge('inr_network', 'in_coverage')
    dot.edge('inr_header', 'in_rate')
    dot.edge('inr_network', 'in_rate', style="invis")
    dot.edge('inr_network', 'in_rate')
    dot.edge('inr_provider', 'in_rate')
    dot.edge('inr_provider', 'in_pr_loc')
    dot.edge('inr_provider', 'in_provider')
    dot.edge('inr_network', 'in_provider')
    dot.edge('inr_header', 'in_provider')

    dot.edge('in_pr_loc', 'provider_reference_file')
    dot.edge('provider_reference_file', 'pr_provider1')

    dot.edge('pr_provider1', 'in_rate', style='dashed', color='blue', arrowhead='normal')
    dot.edge('pr_provider1', 'in_provider', style='dashed', color='blue', arrowhead='normal')

    html = dot._repr_image_svg_xml()

    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="1200pt" aligned=center', html)
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
    html = re.sub(r'Table&#45;of&#45;Contents Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/table-of-contents" target="_blank">Table&#45;of&#45;Contents Files</a>',
                  html)
    html = re.sub(r'In&#45;Network&#45;Rates Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/in-network-rates" target="_blank">In&#45;Network&#45;Rates Files</a>',
                  html)
    html = re.sub(r'Provider&#45;Reference Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/provider-reference" target="_blank">Provider&#45;Reference Files</a>',
                  html)
    html = re.sub(r'Allowed&#45;Amount Files',
                  '<a href="https://github.com/CMSgov/price-transparency-guide/tree/master/schemas/allowed-amounts" target="_blank">Allowed&#45;Amount Files</a>',
                  html)

    html = re.sub(r'stroke-width=\"2\"', 'stroke-width=\"4\"', html)

    return html
