"""
Methods used in all schemas in price transparency
"""


def get_methods_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_run_import_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_import_files_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_run_ingest_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')

    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_ingest_tables_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_run_analytic_html(cat_name='hive_metastore'):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)
    return html


def get_methods_analytic_tables_html(schema=''):
    import re
    from graphviz import Digraph

    dot = Digraph('pt')
    dot.attr(compound='true')
    dot.graph_attr['rankdir'] = 'LR'
    dot.edge_attr.update(arrowhead='none', arrowsize='2')
    dot.attr('node', shape='rectangle')
    dot.node('run_import', 'run_import()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('import_files', 'Import Files', fillcolor='#FFFACD', style='filled', shape='folder')
    dot.node('run_ingest', 'run_ingest()', fillcolor='cyan', shape='cds', style='filled')
    dot.node('ingest_tables', 'Ingest Tables', fillcolor='#CAD9EF', style='filled')
    dot.node('run_analytic', 'run_analytic()', fillcolor='cyan', shape='cds', style='filled')
    with dot.subgraph(name='cluster_workflow') as a:
        a.attr(color='#006400')
        a.attr(fillcolor='#D3F8D3')
        a.body.append('style="filled"')
        a.node('analytic_tables', 'Analytic Tables', fillcolor='#CAD9EF', style='filled')
    dot.edge('run_import', 'import_files')
    dot.edge('import_files', 'run_ingest')
    dot.edge('run_ingest', 'ingest_tables')
    dot.edge('ingest_tables', 'run_analytic')
    dot.edge('run_analytic', 'analytic_tables')
    html = dot._repr_image_svg_xml()
    html = re.sub(r'<svg width=\"\d*pt\" height=\"\d*pt\"',
                  '<div style="text-align:center;"><svg width="800pt" aligned=center', html)

    html = f'''<table><tr><td style="width:80%;"><font size="+4">Inspect {schema} Analytic Tables</font></td>
    <td >{html}</td></tr></table>'''

    return html
