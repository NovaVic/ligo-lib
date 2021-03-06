from jinja2 import Environment, PackageLoader
from linker.core.base import LINKING_RELATIONSHIPS, LINKING_METHODS

from xhtml2pdf import pisa
import logging

logger = logging.getLogger(__name__)


def generate_linking_summary(data, dest_dir):
    logger.debug('>>--- generate_linking_summary --->>')
    project = data.project
    logger.info("Generating summary report of project %s with task UUID: %s.",
                project['name'], project['task_uuid'])

    jenv = Environment(loader=PackageLoader('linker.reports', 'templates'))

    template = jenv.get_template("linking_summary.html")

    datasets = [dataset['name'] for dataset in project['datasets']]
    relationship = None
    if project['type'] == 'LINK':
        for rel in LINKING_RELATIONSHIPS:
            if rel[0] == project['relationship_type']:
                relationship = rel[1]

    steps = []
    for step in data.project['steps']:
        step = {
            "seq": step['seq'],
            "linking_method": LINKING_METHODS.get(step['linking_method'], "Deterministic"),
            "blocking_schema": step['blocking_schema'],
            "linking_schema": step['linking_schema'],
            "total_records_linked": data.steps[step['seq']].get('total_records_linked', None),
            "total_entities": data.steps[step['seq']].get('total_entities', None),
            "total_matched_not_linked": data.steps[step['seq']].get('total_matched_not_linked', None)
        }

        steps.append(step)

    project_types = {
        'LINK': 'Linking',
        'DEDUP': 'De-Duplication'
    }

    template_vars = {
        "name": project['name'],
        "type": project_types[project['type']],
        "datasets": ", ".join(datasets),
        "relationship_type": relationship,
        "total_records_linked": data.total_records_linked,
        "total_entities": data.total_entities,
        "steps": steps
    }

    html_out = template.render(template_vars)

    # removing extra / from file path; depends on django media_root setting in common.py though
    report_file_name = dest_dir + project['name'] + "_summary.pdf"
    report_file = open(report_file_name, "w+b")
    logger.debug('Summary report file name: %s', report_file_name)
    try:
        pisa.CreatePDF(html_out.encode('utf-8'), dest=report_file, encoding='utf-8')
    except Exception as e:
        logger.error('Failed to generate summary report pdf.', exc_info=True)
        logger.debug(e)

    logger.info('Project summary report is generated. %s', report_file_name)
    logger.debug('<<--- generate_linking_summary ---<<')
    return report_file_name
