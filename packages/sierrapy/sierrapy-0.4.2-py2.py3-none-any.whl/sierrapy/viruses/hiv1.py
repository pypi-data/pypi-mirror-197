import re
from .. import fragments
from .virus import Virus


HIV1 = Virus(
    virus_name='HIV1',

    strain_name='HIV1',

    supported_commands=[
        'fasta',
        'mutations',
        'patterns',
        'seqreads'
    ],

    default_url='https://hivdb.stanford.edu/graphql',

    gene_defs=[
        {
            'name': 'PR',
            'synonym_pattern': re.compile(r'^\s*(PR|protease)\s*$', re.I)
        },
        {
            'name': 'RT',
            'synonym_pattern': re.compile(
                r'^\s*(RT|reverse transcriptase)\s*$', re.I)
        },
        {
            'name': 'IN',
            'synonym_pattern': re.compile(r'^\s*(IN|INT|integrase)\s*$', re.I)
        },
        {
            'name': 'POL',
            'synonym_pattern': re.compile(r'^\s*(pol)\s*$', re.I),
            'target_genes': [
                {
                    'name': 'PR',
                    'offset': 0,
                    'range': (1, 99)
                },
                {
                    'name': 'RT',
                    'offset': 0,
                    'range': (100, 660)
                },
                {
                    'name': 'IN',
                    'offset': 0,
                    'range': (661, 949)
                }
            ]
        }
    ],

    default_queries={
        'fasta': fragments.HIV1_SEQUENCE_ANALYSIS_DEFAULT,
        'mutations': fragments.HIV1_MUTATIONS_ANALYSIS_DEFAULT,
        'patterns': fragments.HIV1_MUTATIONS_ANALYSIS_DEFAULT,
        'seqreads': fragments.HIV1_SEQUENCE_READS_ANALYSIS_DEFAULT
    }
)
