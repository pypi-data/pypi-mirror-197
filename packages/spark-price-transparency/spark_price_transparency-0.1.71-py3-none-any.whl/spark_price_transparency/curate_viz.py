"""
Curation Workflow HTML for all schemas in price transparency
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
            with r.subgraph(name='cluster_pt_raw_inr') as rinr:
                rinr.body.append('label="In-Network-Rates Files"')
                rinr.body.append('style="filled"')
                rinr.body.append('color="#808080"')
                rinr.body.append('fillcolor="#DCDCDC"')
                rinr.node('inr_meta', 'inr_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                rinr.node('in_network_file', '.../schema=in-network-rates/*.json', fillcolor='#FFFACD', style='filled',
                          shape='folder', **{'width': "4"})
            with r.subgraph(name='cluster_pt_raw_pr') as rpr:
                rpr.body.append('label="Provider-Reference Files"')
                rpr.body.append('style="filled"')
                rpr.body.append('color="#808080"')
                rpr.body.append('fillcolor="#DCDCDC"')
                rpr.node('pr_meta', 'pr_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                rpr.node('provider_reference_file', '.../schema=provider-reference/*.json', fillcolor='#FFFACD',
                         style='filled', shape='folder', **{'width': "4"})
            with r.subgraph(name='cluster_pt_raw_aa') as raa:
                raa.body.append('label="Allowed-Amount Files"')
                raa.body.append('style="filled"')
                raa.body.append('color="#808080"')
                raa.body.append('fillcolor="#DCDCDC"')
                raa.node('aa_meta', 'aa_meta', fillcolor='#F5F5F5', style='filled', shape='tab')
                raa.node('allowed_amount_file', '.../schema=allowed-amount/*.json', fillcolor='#FFFACD', style='filled',
                         shape='folder', **{'width': "4"})
        with c.subgraph(name='cluster_pt_stage') as s:
            s.body.append('label="Database: pt_stage"')
            s.body.append('style="filled"')
            s.body.append('color="#808080"')
            s.body.append('fillcolor="#F5F5F5"')

            s.node('toc', '', fillcolor='#CAD9EF', style='filled', shape='point')
            s.node('toc_inr', '', fillcolor='red', style='invis', shape='point')
            s.node('inr', '', fillcolor='#CAD9EF', style='filled', shape='point')
            s.node('inr', '', fillcolor='#CAD9EF', style='filled', shape='point')
            s.node('pr', '', fillcolor='#CAD9EF', style='filled', shape='point')
            s.node('pr_aa', '', fillcolor='red', style='invis', shape='point')
            s.node('aa', '', fillcolor='#CAD9EF', style='filled', shape='point')

            s.node('toc_header', 'toc_header', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'toc_header'))
            s.node('toc_reporting', 'toc_reporting', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'toc_reporting'))
            s.node('toc_inr_ingest', 'toc_inr_ingest', fillcolor='red', style='invis', **{'width': "2"})
            s.node('inr_header', 'inr_header', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'inr_header'))
            s.node('inr_network', 'inr_network', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'inr_network'))
            s.node('inr_provider', 'inr_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'inr_provider'))
            s.node('pr_provider', 'pr_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'pr_provider'))
            s.node('pr_aa_ingest', 'pr_aa_ingest', fillcolor='red', style='invis', **{'width': "2"})
            s.node('aa_header', 'aa_header', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'aa_header'))
            s.node('aa_network', 'aa_network', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'aa_network'))

            s.node('top_analytic', 'top_analytic', fillcolor='red', style='invis', **{'width': "2"})
            s.node('index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'index_reports'))
            s.node('toc_inr_analytic', 'toc_inr_analytic', fillcolor='red', style='invis', **{'width': "2"})
            s.node('in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'in_coverage'))
            s.node('in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_rate'))
            s.node('in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'in_provider'))
            s.node('pr_aa_analytic', 'pr_aa_analytic', fillcolor='red', style='invis', **{'width': "2"})
            s.node('out_rate', 'out_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'out_rate'))
            s.node('out_provider', 'out_provider', fillcolor='#CAD9EF', style='filled',
                   **tbl_link('pt_stage', 'out_provider'))

        with c.subgraph(name='cluster_pt') as p:
            p.body.append('label="Database: pt"')
            p.body.append('style="filled"')
            p.body.append('color="#808080"')
            p.body.append('fillcolor="#F5F5F5"')

            p.node('v_top_analytic', 'v_top_analytic', fillcolor='red', style='invis', **{'width': "2"})
            p.node('v_index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'index_reports'))
            p.node('v_toc_inr_analytic', 'toc_inr_analytic', fillcolor='red', style='invis', **{'width': "2"})
            p.node('v_in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'in_coverage'))
            p.node('v_in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'in_rate'))
            p.node('v_in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'in_provider'))
            p.node('v_pr_aa_analytic1', 'pr_aa_analytic1', fillcolor='red', style='invis', **{'width': "2"})
            p.node('v_pr_aa_analytic2', 'pr_aa_analytic2', fillcolor='red', style='invis', **{'width': "2"})
            p.node('v_out_rate', 'out_rate', fillcolor='#CAD9EF', style='filled,dashed', **tbl_link('pt', 'out_rate'))
            p.node('v_out_provider', 'out_provider', fillcolor='#CAD9EF', style='filled,dashed',
                   **tbl_link('pt', 'out_provider'))

        dot.edge('table_of_contents_file', 'toc', ltail='cluster_pt_raw_toc')
        dot.edge('table_of_contents_file', 'toc_inr', ltail='cluster_pt_raw_toc', style="invis")
        dot.edge('in_network_file', 'toc_inr', ltail='cluster_pt_raw_inr', style="invis")
        dot.edge('in_network_file', 'inr', ltail='cluster_pt_raw_inr')
        dot.edge('provider_reference_file', 'pr', ltail='cluster_pt_raw_pr')
        dot.edge('provider_reference_file', 'pr_aa', ltail='cluster_pt_raw_pr', style="invis")
        dot.edge('allowed_amount_file', 'pr_aa', ltail='cluster_pt_raw_aa', style="invis")
        dot.edge('allowed_amount_file', 'aa', ltail='cluster_pt_raw_aa')

        dot.edge('toc', 'toc_header')
        dot.edge('toc', 'toc_reporting')
        dot.edge('toc_inr', 'toc_inr_ingest', style="invis")
        dot.edge('inr', 'inr_header')
        dot.edge('inr', 'inr_network')
        dot.edge('inr', 'inr_provider')
        dot.edge('pr', 'pr_provider')
        dot.edge('pr_aa', 'pr_aa_ingest', style="invis")
        dot.edge('aa', 'aa_header')
        dot.edge('aa', 'aa_network')

        dot.edge('toc_header', 'top_analytic', style="invis")
        dot.edge('toc_header', 'index_reports')
        dot.edge('toc_reporting', 'index_reports')
        dot.edge('toc_inr_ingest', 'top_analytic', style="invis")
        dot.edge('toc_inr_ingest', 'toc_inr_analytic', style="invis")
        dot.edge('inr_header', 'in_coverage')
        dot.edge('inr_network', 'in_coverage')
        dot.edge('inr_header', 'in_rate')
        dot.edge('inr_network', 'in_rate')
        dot.edge('inr_provider', 'in_rate')
        dot.edge('inr_network', 'in_provider')
        dot.edge('inr_header', 'in_provider')
        dot.edge('inr_provider', 'in_provider')
        dot.edge('pr_provider', 'in_rate')
        dot.edge('pr_provider', 'in_provider')
        dot.edge('pr_aa_ingest', 'pr_aa_analytic', style="invis")
        dot.edge('aa_header', 'out_rate')
        dot.edge('aa_network', 'out_provider')
        dot.edge('aa_network', 'out_rate')
        dot.edge('aa_header', 'out_provider')

        dot.edge('top_analytic', 'v_top_analytic', style="invis")
        dot.edge('index_reports', 'v_index_reports')
        dot.edge('toc_inr_analytic', 'v_toc_inr_analytic', style="invis")
        dot.edge('in_coverage', 'v_in_coverage')
        dot.edge('in_rate', 'v_in_rate')
        dot.edge('in_provider', 'v_in_provider')
        dot.edge('pr_aa_analytic', 'v_pr_aa_analytic1', style="invis")
        dot.edge('pr_aa_analytic', 'v_pr_aa_analytic2', style="invis")
        dot.edge('out_rate', 'v_out_rate')
        dot.edge('out_provider', 'v_out_provider')

    html = dot._repr_image_svg_xml()

    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="4500pt" aligned=center', html)
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
