from pathlib import Path

import lingpy
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar, getEvoBibAsBibtex


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "logos"

    def cmd_download(self, args):
        src = {}
        for k in ["CLICS-1.0.0", "Wold2009", "Logos2008", "Key2007", "Saxena2013"]:
            src[k] = getEvoBibAsBibtex(k)
            # TODO: As far as I can tell, we have no obvious way of passing _check_id=False to
            # add_sources() in cldfbench. Will investigate. This fixes the 'invalid' bib key.
            if k == "CLICS-1.0.0":
                src[k] = src[k].replace("CLICS-1.0.0", "CLICS1")
        self.raw_dir.write("sources.bib", "\n\n".join(src.values()))

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
