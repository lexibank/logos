from pathlib import Path

import lingpy
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "logos"

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist((self.raw_dir / "D_old-clics.tsv").as_posix())
        src = {"logos": "Logos2008"}
        args.writer.add_sources(*self.raw_dir.read_bib())
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )

        for k in progressbar(wl):
            if wl[k, "value"]:
                args.writer.add_language(
                    ID=slug(wl[k, "doculect"], lowercase=False),
                    Name=wl[k, "doculect"],
                    Glottocode=wl[k, "glottolog"],
                )
                args.writer.add_form(
                    Language_ID=slug(wl[k, "doculect"], lowercase=False),
                    Parameter_ID=concepts[wl[k, "concept"]],
                    Value=wl[k, "value"],
                    Form=wl[k, "value"],
                    Source=src.get(wl[k, "source"], ""),
                )
