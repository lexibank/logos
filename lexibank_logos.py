# coding=utf-8
from __future__ import unicode_literals, print_function
from itertools import groupby

import attr
import lingpy
from pycldf.sources import Source

from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "logos"

    def cmd_download(self, **kw):
        src = {}
        for k in ['List2014f', 'Wold2009', 'Logos2008', 'Key2007',
                'Saxena2013']:
            src[k] = getEvoBibAsBibtex(k)
        self.raw.write(
                'sources.bib', 
                '\n\n'.join(src.values())
                )

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(self.raw_dir.joinpath('D_old-clics.tsv').as_posix())

        src = {

                'logos': 'Logos2008'
                }

        args.writer.add_sources()
        for k in pb(wl, desc='wl-to-cldf'):
            if wl[k, 'value']:
                args.writer.add_language(
                    ID=slug(wl[k, 'doculect']),
                    Name=wl[k, 'doculect'],
                    Glottocode=wl[k, 'glottolog'])
                args.writer.add_concept(
                    ID=slug(wl[k, 'concept']),
                    Name=wl[k, 'concept'],
                    Concepticon_ID=wl[k, 'concepticon_id']
                    )
                args.writer.add_lexemes(
                    Language_ID=slug(wl[k, 'doculect']),
                    Parameter_ID=slug(wl[k, 'concept']),
                    Value=wl[k, 'value'],
                    Source=src.get(wl[k, 'source'], ''))
