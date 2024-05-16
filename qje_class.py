import re
import os


class PaperInfo:
    def __init__(self):
        self.ut_char = ""
        self.pub_year = ""
        self.SO = ""
        self.issn = ""
        self.doi = ""
        self.issue = ""
        self.volume = ""
        self.document_type = ""
        self.abstract = ""
        self.title = ""
        self.au_full_name = ""
        self.au_family_name = ""
        self.au_given_name = ""
        self.au_seq = ""
        self.au_affiliation = ""
        self.af_seq = ""
        self.af_bib = ""

    def loadbib(self, file):
        woslist = list()
        with open(file, "r") as f:
            key = f.readlines()[0].replace("\n", "").split("\t")[1:]
        with open(file, "r") as f:
            for line in f.readlines()[1:(len(f.readlines()) - 1)]:
                field = line.replace("\n", "").split("\t")[1:]
                woslist.append(dict(zip(key, field)))
        return woslist

    def load_basic(self, data_dict):
        pattern = re.compile(r'(?P<RP>\[.+\]) (?P<AFL>.+)')
        self.ut_char = data_dict["UT"]
        self.pub_year = data_dict["PY"]
        self.SO = data_dict["SO"]
        self.issn = data_dict["SN"]
        self.doi = data_dict["DI"]
        self.issue = data_dict["IS"]
        self.volume = data_dict["VL"]
        self.document_type = data_dict["DT"]
        self.abstract = data_dict["AB"]
        self.title = data_dict["TI"]
        self.au_full_name = data_dict["AF"]
        self.au_family_name = '; '.join([x.split(',')[0].strip() for x in data_dict["AF"].split('; ')])
        self.au_given_name = '; '.join([x.split(',')[1].strip() for x in data_dict["AF"].split('; ')])
        self.au_seq = '; '.join([f'{data_dict["AF"].split("; ")[x]} {x+1}' for x in range(len(data_dict["AF"].split("; ")))])
        self.au_affiliation = re.match(pattern, data_dict["C1"]).groupdict()['AFL'] if re.match(pattern, data_dict["C1"]) else data_dict["C1"]
        self.af_bib = data_dict["CR"]

    def ouput_basic(self, basic_path, woslist):
        basic_info_path = os.path.join(basic_path, 'wos_basic_information.txt')
        abstract_path = os.path.join(basic_path, 'wos_abstract.txt')
        title_path = os.path.join(basic_path, 'wos_title.txt')
        author_path = os.path.join(basic_path, 'wos_author.txt')
        affiliation_path = os.path.join(basic_path, 'wos_affiliation.txt')
        citation_path = os.path.join(basic_path, 'wos_citation.txt')
        if os.path.exists(basic_info_path):
            os.remove(basic_info_path)
        if os.path.exists(abstract_path):
            os.remove(abstract_path)
        if os.path.exists(title_path):
            os.remove(title_path)
        if os.path.exists(author_path):
            os.remove(author_path)
        if os.path.exists(affiliation_path):
            os.remove(affiliation_path)
        if os.path.exists(citation_path):
            os.remove(citation_path)

        for data in woslist:
            paper = PaperInfo()
            paper.load_basic(data)
            with open(basic_info_path, mode='a', encoding='utf-8') as f:
                f.write(f'{paper.ut_char}|{paper.pub_year}|{paper.SO}|{paper.issn}|{paper.doi}|{paper.issue}|{paper.volume}|{paper.document_type}\n')
            with open(abstract_path, mode='a', encoding='utf-8') as f:
                f.write(f'{paper.ut_char}|{paper.abstract}\n')
            with open(title_path, mode='a', encoding='utf-8') as f:
                f.write(f'{paper.ut_char}|{paper.title}\n')
            with open(author_path, mode='a', encoding='utf-8') as f:
                full_name = paper.au_full_name.split('; ')
                for fn in range(len(full_name)):
                    family_name = full_name[fn].split(',')[0].strip()
                    given_name = full_name[fn].split(',')[1].strip()
                    seq = fn + 1
                    f.write(f'{paper.ut_char}|{full_name[fn]}|{family_name}|{given_name}|{seq}\n')
            with open(affiliation_path, mode='a', encoding='utf-8') as f:
                full_name = paper.au_full_name.split('; ')
                aff = paper.au_affiliation.split('; ')
                for fn in range(len(full_name)):
                    seq = fn + 1
                    if seq <= len(aff):
                        affiliation = aff[fn]
                        aff_seq = fn + 1
                    else:
                        affiliation = aff[-1]
                        aff_seq = len(aff)
                    f.write(f'{paper.ut_char}|{full_name[fn]}|{seq}|{affiliation}|{aff_seq}\n')
            with open(citation_path, mode='a', encoding='utf-8') as f:
                citation = paper.af_bib.split('; ')
                for c in citation:
                    f.write(f'{paper.ut_char}|{c}\n')


if __name__ == '__main__':
    os.mkdir('data')
    basic_path = 'data'
    Paper = PaperInfo()
    woslist = Paper.loadbib("qje2014_2023.txt")
    Paper.ouput_basic(basic_path, woslist)