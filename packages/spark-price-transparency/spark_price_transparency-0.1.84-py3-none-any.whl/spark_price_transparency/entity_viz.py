"""
Entity HTML for all schemas in price transparency
"""


def get_entity_html(cat_name='hive_metastore'):
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
        c.body.append('label="Price Transparency Entity Types"')
        c.node('run_import', '*.run_import()', fillcolor='cyan', shape='cds', style='filled', **{'width': "2"})
        with c.subgraph(name='cluster_pt_raw_file') as rf:
            rf.body.append('label="Import Files"')
            rf.attr(fillcolor='#F5F5F5')
            rf.body.append('style="filled"')
            rf.node('file1', 'file1', fillcolor='red', style='invis', **{'width': "2"})
            rf.node('table_of_contents_files', 'Table-of-Contents Files', fillcolor='#FFFACD', style='filled',
                    shape='folder', **{'width': "2.8"})
            rf.node('file3', 'file3', fillcolor='red', style='invis', **{'width': "2"})
            rf.node('file4', 'file4', fillcolor='red', style='invis', **{'width': "2"})
            rf.node('provider_reference_files', 'Provider-Reference Files', fillcolor='#FFFACD', style='filled',
                    shape='folder', **{'width': "2.8"})
            rf.node('in_network_rates_files', 'In-Network-Rates Files', fillcolor='#FFFACD', style='filled',
                    shape='folder', **{'width': "2.8"})
            rf.node('file7', 'file7', fillcolor='red', style='invis', **{'width': "2"})
            rf.node('file8', 'file8', fillcolor='red', style='invis', **{'width': "2"})
            rf.node('allowed-amount_files', 'Allowed-Amount Files', fillcolor='#FFFACD', style='filled', shape='folder',
                    **{'width': "2.8"})
            rf.node('file10', 'file10', fillcolor='red', style='invis', **{'width': "2"})
        c.node('run_ingest', '*.run_ingest()', fillcolor='cyan', shape='cds', style='filled', **{'width': "2"})
        with c.subgraph(name='cluster_pt_stage_ingest') as si:
            si.body.append('label="Ingest Tables"')
            si.attr(fillcolor='#F5F5F5')
            si.body.append('style="filled"')
            si.node('toc_reporting', 'toc_reporting', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'toc_reporting'))
            si.node('toc_header', 'toc_header', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'toc_header'))
            si.node('ingest3', 'ingest3', fillcolor='red', style='invis', **{'width': "2"})
            si.node('inr_header', 'inr_header', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'inr_header'))
            si.node('inr_network', 'inr_network', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'inr_network'))
            si.node('inr_provider', 'inr_provider', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'inr_provider'))
            si.node('pr_provider', 'pr_provider', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'pr_provider'))
            si.node('ingest8', 'ingest8', fillcolor='red', style='invis', **{'width': "2"})
            si.node('aa_header', 'aa_header', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'aa_header'))
            si.node('aa_network', 'aa_network', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'aa_network'))
        c.node('run_analytic', '*.run_analytic()', fillcolor='cyan', shape='cds', style='filled', **{'width': "2"})
        with c.subgraph(name='cluster_pt_stage_analytic') as sa:
            sa.body.append('label="Analytic Tables"')
            sa.attr(fillcolor='#F5F5F5')
            sa.body.append('style="filled"')
            sa.node('index_reports', 'index_reports', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'index_reports'))
            sa.node('analytic2', 'analytic2', fillcolor='red', style='invis', **{'width': "2"})
            sa.node('toc_inr_analytic', 'toc_inr_analytic', fillcolor='red', style='invis', **{'width': "2"})
            sa.node('in_coverage', 'in_coverage', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'in_coverage'))
            sa.node('in_rate', 'in_rate', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'in_rate'))
            sa.node('in_provider', 'in_provider', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'in_provider'))
            sa.node('analytic7', 'analytic7', fillcolor='red', style='invis', **{'width': "2"})
            sa.node('analytic8', 'analytic8', fillcolor='red', style='invis', **{'width': "2"})
            sa.node('out_code', 'out_code', fillcolor='#CAD9EF', style='filled', **tbl_link('pt_stage', 'out_code'))
            sa.node('out_amount', 'out_amount', fillcolor='#CAD9EF', style='filled',
                    **tbl_link('pt_stage', 'out_amount'))

        dot.edge('run_import', 'allowed-amount_files', style="invis")
        dot.edge('run_import', 'file10', style="invis")
        dot.edge('run_import', 'file3', style="invis")
        dot.edge('run_import', 'file4', style="invis")
        dot.edge('run_import', 'in_network_rates_files', style="invis")
        dot.edge('run_import', 'provider_reference_files', style="invis")
        dot.edge('run_import', 'file7', style="invis")
        dot.edge('run_import', 'file8', style="invis")
        dot.edge('run_import', 'file1', style="invis")
        dot.edge('run_import', 'table_of_contents_files', style="invis")

        dot.edge('file1', 'toc_header', style="invis")
        dot.edge('table_of_contents_files', 'toc_reporting', style="invis")
        dot.edge('file3', 'ingest3', style="invis")
        dot.edge('file4', 'inr_header', style="invis")
        dot.edge('in_network_rates_files', 'inr_network', style="invis")
        dot.edge('provider_reference_files', 'inr_provider', style="invis")
        dot.edge('file7', 'pr_provider', style="invis")
        dot.edge('file8', 'ingest8', style="invis")
        dot.edge('allowed-amount_files', 'aa_header', style="invis")
        dot.edge('file10', 'aa_network', style="invis")

        dot.edge('file1', 'run_ingest', style="invis")
        dot.edge('table_of_contents_files', 'run_ingest', style="invis")
        dot.edge('file3', 'run_ingest', style="invis")
        dot.edge('file4', 'run_ingest', style="invis")
        dot.edge('in_network_rates_files', 'run_ingest', style="invis")
        dot.edge('provider_reference_files', 'run_ingest', style="invis")
        dot.edge('file7', 'run_ingest', style="invis")
        dot.edge('file8', 'run_ingest', style="invis")
        dot.edge('allowed-amount_files', 'run_ingest', style="invis")
        dot.edge('file10', 'run_ingest', style="invis")

        dot.edge('run_ingest', 'toc_reporting', style="invis")
        dot.edge('run_ingest', 'toc_header', style="invis")
        dot.edge('run_ingest', 'ingest3', style="invis")
        dot.edge('run_ingest', 'inr_header', style="invis")
        dot.edge('run_ingest', 'inr_network', style="invis")
        dot.edge('run_ingest', 'inr_provider', style="invis")
        dot.edge('run_ingest', 'pr_provider', style="invis")
        dot.edge('run_ingest', 'ingest8', style="invis")
        dot.edge('run_ingest', 'aa_header', style="invis")
        dot.edge('run_ingest', 'aa_network', style="invis")

        dot.edge('toc_reporting', 'run_analytic', style="invis")
        dot.edge('toc_header', 'run_analytic', style="invis")
        dot.edge('ingest3', 'run_analytic', style="invis")
        dot.edge('inr_header', 'run_analytic', style="invis")
        dot.edge('inr_provider', 'run_analytic', style="invis")
        dot.edge('inr_network', 'run_analytic', style="invis")
        dot.edge('pr_provider', 'run_analytic', style="invis")
        dot.edge('ingest8', 'run_analytic', style="invis")
        dot.edge('aa_header', 'run_analytic', style="invis")
        dot.edge('aa_network', 'run_analytic', style="invis")

        dot.edge('run_analytic', 'analytic2', style="invis")
        dot.edge('run_analytic', 'index_reports', style="invis")
        dot.edge('run_analytic', 'toc_inr_analytic', style="invis")
        dot.edge('run_analytic', 'in_coverage', style="invis")
        dot.edge('run_analytic', 'in_rate', style="invis")
        dot.edge('run_analytic', 'in_provider', style="invis")
        dot.edge('run_analytic', 'analytic7', style="invis")
        dot.edge('run_analytic', 'analytic8', style="invis")
        dot.edge('run_analytic', 'out_code', style="invis")
        dot.edge('run_analytic', 'out_amount', style="invis")

        dot.edge('toc_header', 'analytic2', style="invis")
        dot.edge('toc_reporting', 'index_reports', style="invis")
        dot.edge('ingest3', 'toc_inr_analytic', style="invis")
        dot.edge('inr_header', 'in_coverage', style="invis")
        dot.edge('inr_network', 'in_rate', style="invis")
        dot.edge('inr_provider', 'in_provider', style="invis")
        dot.edge('pr_provider', 'analytic7', style="invis")
        dot.edge('ingest8', 'analytic8', style="invis")
        dot.edge('aa_header', 'out_code', style="invis")
        dot.edge('aa_network', 'out_amount', style="invis")

    html = dot._repr_image_svg_xml()

    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg height="600pt" aligned=center', html)
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
