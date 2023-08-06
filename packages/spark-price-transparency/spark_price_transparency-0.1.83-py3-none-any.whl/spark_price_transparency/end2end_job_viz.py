"""
Curation Workflow HTML for all schemas in price transparency
"""


def get_end2end_job_html(cat_name='hive_metastore'):
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
        c.body.append('label="Price Transparency End-to-End Job"')
        with c.subgraph(name='cluster_toc') as toc:
            toc.body.append('label="guide.run_table_of_contents(urls)"')
            toc.body.append('style="filled"')
            toc.body.append('color="#808080"')
            toc.body.append('fillcolor="#F5F5F5"')
            toc.node('toc_a', 'table_of_contents.run_import()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            toc.node('toc_b', 'table_of_contents.run_ingest()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            toc.node('toc_c', 'table_of_contents.run_analytic()', fillcolor='cyan', style='filled', **{'width': "3.6"})
        c.node('toc_aa', '', fillcolor='#CAD9EF', style='invis', shape='point')
        with c.subgraph(name='cluster_aa') as aa:
            aa.body.append('label="guide.run_allowed_amounts()"')
            aa.body.append('style="filled"')
            aa.body.append('color="#808080"')
            aa.body.append('fillcolor="#F5F5F5"')
            aa.node('aa_a', 'allowed-amount.run_import()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            aa.node('aa_b', 'allowed_amount.run_ingest()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            aa.node('aa_c', 'allowed-amount.run_analytic()', fillcolor='cyan', style='filled', **{'width': "3.6"})
        c.node('toc_inr', '', fillcolor='#CAD9EF', style='invis', shape='point')
        with c.subgraph(name='cluster_inr') as inr:
            inr.body.append('label="guide.run_in_network_rates()"')
            inr.body.append('style="filled"')
            inr.body.append('color="#808080"')
            inr.body.append('fillcolor="#F5F5F5"')
            inr.node('inr_a', 'in_network_rates.run_import()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            inr.node('inr_b', 'in_network_rates.run_ingest()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            inr.node('inr_c', 'in_network_rates.run_analytic()', fillcolor='cyan', style='filled', **{'width': "3.6"})
        c.node('inr_pr', '', fillcolor='#CAD9EF', style='invis', shape='point')
        with c.subgraph(name='cluster_pr') as pr:
            pr.body.append('label="guide.run_provider_reference()"')
            pr.body.append('style="filled"')
            pr.body.append('color="#808080"')
            pr.body.append('fillcolor="#F5F5F5"')
            pr.node('pr_a', 'provider_reference.run_import()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            pr.node('pr_b', 'provider_reference.run_ingest()', fillcolor='cyan', style='filled', **{'width': "3.6"})
            pr.node('pr_c', 'provider_reference.run_analytic()', fillcolor='cyan', style='filled', **{'width': "3.6"})

    dot.edge('toc_a', 'aa_a', style="invis")
    dot.edge('toc_a', 'toc_aa', style="invis")
    dot.edge('toc_aa', 'aa_a', style="invis")
    dot.edge('toc_a', 'inr_a', style="invis")
    dot.edge('toc_b', 'aa_b', ltail='cluster_toc', lhead='cluster_aa')
    dot.edge('toc_b', 'inr_b', ltail='cluster_toc', lhead='cluster_inr')
    dot.edge('toc_c', 'aa_c', style="invis")
    dot.edge('toc_c', 'inr_c', style="invis")
    dot.edge('toc_c', 'toc_inr', style="invis")
    dot.edge('toc_inr', 'inr_c', style="invis")
    dot.edge('inr_a', 'pr_a', style="invis")
    dot.edge('inr_b', 'pr_b', ltail='cluster_inr', lhead='cluster_pr')
    dot.edge('inr_b', 'inr_pr', style="invis")
    dot.edge('inr_pr', 'pr_b', style="invis")
    dot.edge('inr_c', 'pr_c', style="invis")

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
