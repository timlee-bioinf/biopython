# Copyright 2006-2014 by Peter Cock.  All rights reserved.
# Revisions copyright 2011 Brandon Invergo. All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.
"""Tests for Bio.Align.phylip module."""
import unittest
from io import StringIO
from tempfile import NamedTemporaryFile

from Bio import Align
from Bio.Align import substitution_matrices

substitution_matrix = substitution_matrices.load("BLOSUM62")

try:
    import numpy as np
except ImportError:
    from Bio import MissingPythonDependencyError

    raise MissingPythonDependencyError(
        "Install numpy if you want to use Bio.Align.phylip."
    ) from None


class TestPhylipReading(unittest.TestCase):
    def check_reading_writing(self, path):
        alignments = Align.parse(path, "phylip")
        stream = StringIO()
        n = Align.write(alignments, stream, "phylip")
        self.assertEqual(n, 1)
        alignments = Align.parse(path, "phylip")
        alignment = next(alignments)
        stream.seek(0)
        saved_alignments = Align.parse(stream, "phylip")
        saved_alignment = next(saved_alignments)
        with self.assertRaises(StopIteration):
            next(saved_alignments)
        self.assertEqual(len(alignment), len(saved_alignment))
        for i, (sequence, saved_sequence) in enumerate(
            zip(alignment.sequences, saved_alignment.sequences)
        ):
            self.assertEqual(sequence.id, saved_sequence.id)
            self.assertEqual(sequence.seq, saved_sequence.seq)
            self.assertEqual(alignment[i], saved_alignment[i])
        self.assertTrue(
            np.array_equal(alignment.coordinates, saved_alignment.coordinates)
        )

    def test_one(self):
        path = "Phylip/one.dat"
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            self.check_one(alignments)
            alignments = iter(alignments)
            self.check_one(alignments)
        with Align.parse(path, "phylip") as alignments:
            self.check_one(alignments)
        with self.assertRaises(AttributeError):
            alignments._stream
        with Align.parse(path, "phylip") as alignments:
            pass
        with self.assertRaises(AttributeError):
            alignments._stream
        self.check_reading_writing(path)
        with open(path) as stream:
            data = stream.read()
        stream = NamedTemporaryFile("w+t")
        stream.write(data)
        stream.seek(0)
        alignments = Align.parse(stream, "phylip")
        self.check_one(alignments)

    def check_one(self, alignments):
        alignment = next(alignments)
        with self.assertRaises(StopIteration):
            next(alignments)
        self.assertEqual(
            repr(alignment),
            "<Alignment object (8 rows x 286 columns) at 0x%x>" % id(alignment),
        )
        self.assertEqual(len(alignment), 8)
        self.assertEqual(alignment.sequences[0].id, "V_Harveyi_")
        self.assertEqual(alignment.sequences[1].id, "B_subtilis")
        self.assertEqual(alignment.sequences[2].id, "B_subtilis")
        self.assertEqual(alignment.sequences[3].id, "YA80_HAEIN")
        self.assertEqual(alignment.sequences[4].id, "FLIY_ECOLI")
        self.assertEqual(alignment.sequences[5].id, "E_coli_Gln")
        self.assertEqual(alignment.sequences[6].id, "Deinococcu")
        self.assertEqual(alignment.sequences[7].id, "HISJ_E_COL")
        self.assertEqual(
            alignment.sequences[0].seq,
            "MKNWIKVAVAAIALSAATVQAATEVKVGMSGRYFPFTFVKQDKLQGFEVDMWDEIGKRNDYKIEYVTANFSGLFGLLETGRIDTISNQITMTDARKAKYLFADPYVVDGAQITVRKGNDSIQGVEDLAGKTVAVNLGSNFEQLLRDYDKDGKINIKTYDTGIEHDVALGRADAFIMDRLSALELIKKTGLPLQLAGEPFETIQNAWPFVDNEKGRKLQAEVNKALAEMRADGTVEKISVKWFGADITK",
        )
        self.assertEqual(
            alignment.sequences[1].seq,
            "MKMKKWTVLVVAALLAVLSACGNGNSSSKEDDNVLHVGATGQSYPFAYKENGKLTGFDVEVMEAVAKKIDMKLDWKLLEFSGLMGELQTGKLDTISNQVAVTDERKETYNFTKPYAYAGTQIVVKKDNTDIKSVDDLKGKTVAAVLGSNHAKNLESKDPDKKINIKTYETQEGTLKDVAYGRVDAYVNSRTVLIAQIKKTGLPLKLAGDPIVYEQVAFPFAKDDAHDKLRKKVNKALDELRKDGTLKKLSEKYFNEDITVEQKH",
        )
        self.assertEqual(
            alignment.sequences[2].seq,
            "MKKALLALFMVVSIAALAACGAGNDNQSKDNAKDGDLWASIKKKGVLTVGTEGTYEPFTYHDKDTDKLTGYDVEVITEVAKRLGLKVDFKETQWGSMFAGLNSKRFDVVANQVGKTDREDKYDFSDKYTTSRAVVVTKKDNNDIKSEADVKGKTSAQSLTSNYNKLATNAGAKVEGVEGMAQALQMIQQARVDMTYNDKLAVLNYLKTSGNKNVKIAFETGEPQSTYFTFRKGSGEVVDQVNKALKEMKEDGTLSKISKKWFGEDVSK",
        )
        self.assertEqual(
            alignment.sequences[3].seq,
            "MKKLLFTTALLTGAIAFSTFSHAGEIADRVEKTKTLLVGTEGTYAPFTFHDKSGKLTGFDVEVIRKVAEKLGLKVEFKETQWDAMYAGLNAKRFDVIANQTNPSPERLKKYSFTTPYNYSGGVIVTKSSDNSIKSFEDLKGRKSAQSATSNWGKDAKAAGAQILVVDGLAQSLELIKQGRAEATINDKLAVLDYFKQHPNSGLKIAYDRGDKTPTAFAFLQGEDALITKFNQVLEALRQDGTLKQISIEWFGYDITQ",
        )
        self.assertEqual(
            alignment.sequences[4].seq,
            "MKLAHLGRQALMGVMAVALVAGMSVKSFADEGLLNKVKERGTLLVGLEGTYPPFSFQGDDGKLTGFEVEFAQQLAKHLGVEASLKPTKWDGMLASLDSKRIDVVINQVTISDERKKKYDFSTPYTISGIQALVKKGNEGTIKTADDLKGKKVGVGLGTNYEEWLRQNVQGVDVRTYDDDPTKYQDLRVGRIDAILVDRLAALDLVKKTNDTLAVTGEAFSRQESGVALRKGNEDLLKAVNDAIAEMQKDGTLQALSEKWFGADVTK",
        )
        self.assertEqual(
            alignment.sequences[5].seq,
            "MKSVLKVSLAALTLAFAVSSHAADKKLVVATDTAFVPFEFKQGDKYVGFDVDLWAAIAKELKLDYELKPMDFSGIIPALQTKNVDLALAGITITDERKKAIDFSDGYYKSGLLVMVKANNNDVKSVKDLDGKVVAVKSGTGSVDYAKANIKTKDLRQFPNIDNAYMELGTNRADAVLHDTPNILYFIKTAGNGQFKAVGDSLEAQQYGIAFPKGSDELRDKVNGALKTLRENGTYNEIYKKWFGTEPK",
        )
        self.assertEqual(
            alignment.sequences[6].seq,
            "MKKSLLSLKLSGLLVPSVLALSLSACSSPSSTLNQGTLKIAMEGTYPPFTSKNEQGELVGFDVDIAKAVAQKLNLKPEFVLTEWSGILAGLQANKYDVIVNQVGITPERQNSIGFSQPYAYSRPEIIVAKNNTFNPQSLADLKGKRVGSTLGSNYEKQLIDTGDIKIVTYPGAPEILADLVAGRIDAAYNDRLVVNYIINDQKLPVRGAGQIGDAAPVGIALKKGNSALKDQIDKALTEMRSDGTFEKISQKWFGQDVGQP",
        )
        self.assertEqual(
            alignment.sequences[7].seq,
            "MKKLVLSLSLVLAFSSATAAFAAIPQNIRIGTDPTYAPFESKNSQGELVGFDIDLAKELCKRINTQCTFVENPLDALIPSLKAKKIDAIMSSLSITEKRQQEIAFTDKLYAADSRLVVAKNSDIQPTVESLKGKRVGVLQGTTQETFGNEHWAPKGIEIVSYQGQDNIYSDLTAGRIDAAFQDEVAASEGFLKQPVGKDYKFGGPSVKDEKLFGVGTGMGLRKEDNELREALNKAFAEMRADGTYEKLAKKYFDFDVYGG",
        )
        self.assertEqual(
            alignment[0],
            "--MKNWIKVAVAAIA--LSAA------------------TVQAATEVKVGMSGRYFPFTFVKQ--DKLQGFEVDMWDEIGKRNDYKIEYVTANFSGLFGLLETGRIDTISNQITMTDARKAKYLFADPYVVDG-AQITVRKGNDSIQGVEDLAGKTVAVNLGSNFEQLLRDYDKDGKINIKTYDT--GIEHDVALGRADAFIMDRLSALE-LIKKT-GLPLQLAGEPFETI-----QNAWPFVDNEKGRKLQAEVNKALAEMRADGTVEKISVKWFGADITK----",
        )
        self.assertEqual(
            alignment[1],
            "MKMKKWTVLVVAALLAVLSACG------------NGNSSSKEDDNVLHVGATGQSYPFAYKEN--GKLTGFDVEVMEAVAKKIDMKLDWKLLEFSGLMGELQTGKLDTISNQVAVTDERKETYNFTKPYAYAG-TQIVVKKDNTDIKSVDDLKGKTVAAVLGSNHAKNLESKDPDKKINIKTYETQEGTLKDVAYGRVDAYVNSRTVLIA-QIKKT-GLPLKLAGDPIVYE-----QVAFPFAKDDAHDKLRKKVNKALDELRKDGTLKKLSEKYFNEDITVEQKH",
        )
        self.assertEqual(
            alignment[2],
            "MKKALLALFMVVSIAALAACGAGNDNQSKDNAKDGDLWASIKKKGVLTVGTEGTYEPFTYHDKDTDKLTGYDVEVITEVAKRLGLKVDFKETQWGSMFAGLNSKRFDVVANQVG-KTDREDKYDFSDKYTTSR-AVVVTKKDNNDIKSEADVKGKTSAQSLTSNYNKLATN----AGAKVEGVEGMAQALQMIQQARVDMTYNDKLAVLN-YLKTSGNKNVKIAFETGEPQ-----STYFTFRKGS--GEVVDQVNKALKEMKEDGTLSKISKKWFGEDVSK----",
        )
        self.assertEqual(
            alignment[3],
            "MKKLLFTTALLTGAIAFSTF-----------SHAGEIADRVEKTKTLLVGTEGTYAPFTFHDK-SGKLTGFDVEVIRKVAEKLGLKVEFKETQWDAMYAGLNAKRFDVIANQTNPSPERLKKYSFTTPYNYSG-GVIVTKSSDNSIKSFEDLKGRKSAQSATSNWGKDAKA----AGAQILVVDGLAQSLELIKQGRAEATINDKLAVLD-YFKQHPNSGLKIAYDRGDKT-----PTAFAFLQGE--DALITKFNQVLEALRQDGTLKQISIEWFGYDITQ----",
        )
        self.assertEqual(
            alignment[4],
            "MKLAHLGRQALMGVMAVALVAG---MSVKSFADEG-LLNKVKERGTLLVGLEGTYPPFSFQGD-DGKLTGFEVEFAQQLAKHLGVEASLKPTKWDGMLASLDSKRIDVVINQVTISDERKKKYDFSTPYTISGIQALVKKGNEGTIKTADDLKGKKVGVGLGTNYEEWLRQNV--QGVDVRTYDDDPTKYQDLRVGRIDAILVDRLAALD-LVKKT-NDTLAVTGEAFSRQ-----ESGVALRKGN--EDLLKAVNDAIAEMQKDGTLQALSEKWFGADVTK----",
        )
        self.assertEqual(
            alignment[5],
            "--MKSVLKVSLAALTLAFAVS------------------SHAADKKLVVATDTAFVPFEFKQG--DKYVGFDVDLWAAIAKELKLDYELKPMDFSGIIPALQTKNVDLALAGITITDERKKAIDFSDGYYKSG-LLVMVKANNNDVKSVKDLDGKVVAVKSGTGSVDYAKAN--IKTKDLRQFPNIDNAYMELGTNRADAVLHDTPNILY-FIKTAGNGQFKAVGDSLEAQ-----QYGIAFPKGS--DELRDKVNGALKTLRENGTYNEIYKKWFGTEPK-----",
        )
        self.assertEqual(
            alignment[6],
            "-MKKSLLSLKLSGLLVPSVLALS--------LSACSSPSSTLNQGTLKIAMEGTYPPFTSKNE-QGELVGFDVDIAKAVAQKLNLKPEFVLTEWSGILAGLQANKYDVIVNQVGITPERQNSIGFSQPYAYSRPEIIVAKNNTFNPQSLADLKGKRVGSTLGSNYEKQLIDTG---DIKIVTYPGAPEILADLVAGRIDAAYNDRLVVNY-IINDQ-KLPVRGAGQIGDAA-----PVGIALKKGN--SALKDQIDKALTEMRSDGTFEKISQKWFGQDVGQP---",
        )
        self.assertEqual(
            alignment[7],
            "MKKLVLSLSLVLAFSSATAAF-------------------AAIPQNIRIGTDPTYAPFESKNS-QGELVGFDIDLAKELCKRINTQCTFVENPLDALIPSLKAKKIDAIMSSLSITEKRQQEIAFTDKLYAADSRLVVAKNSDIQP-TVESLKGKRVGVLQGTTQETFGNEHWAPKGIEIVSYQGQDNIYSDLTAGRIDAAFQDEVAASEGFLKQPVGKDYKFGGPSVKDEKLFGVGTGMGLRKED--NELREALNKAFAEMRADGTYEKLAKKYFDFDVYGG---",
        )
        self.assertEqual(
            str(alignment),
            """\
V_Harveyi         0 --MKNWIKVAVAAIA--LSAA------------------TVQAATEVKVGMSGRYFPFTF
B_subtili         0 MKMKKWTVLVVAALLAVLSACG------------NGNSSSKEDDNVLHVGATGQSYPFAY
B_subtili         0 MKKALLALFMVVSIAALAACGAGNDNQSKDNAKDGDLWASIKKKGVLTVGTEGTYEPFTY
YA80_HAEI         0 MKKLLFTTALLTGAIAFSTF-----------SHAGEIADRVEKTKTLLVGTEGTYAPFTF
FLIY_ECOL         0 MKLAHLGRQALMGVMAVALVAG---MSVKSFADEG-LLNKVKERGTLLVGLEGTYPPFSF
E_coli_Gl         0 --MKSVLKVSLAALTLAFAVS------------------SHAADKKLVVATDTAFVPFEF
Deinococc         0 -MKKSLLSLKLSGLLVPSVLALS--------LSACSSPSSTLNQGTLKIAMEGTYPPFTS
HISJ_E_CO         0 MKKLVLSLSLVLAFSSATAAF-------------------AAIPQNIRIGTDPTYAPFES

V_Harveyi        38 VKQ--DKLQGFEVDMWDEIGKRNDYKIEYVTANFSGLFGLLETGRIDTISNQITMTDARK
B_subtili        48 KEN--GKLTGFDVEVMEAVAKKIDMKLDWKLLEFSGLMGELQTGKLDTISNQVAVTDERK
B_subtili        60 HDKDTDKLTGYDVEVITEVAKRLGLKVDFKETQWGSMFAGLNSKRFDVVANQVG-KTDRE
YA80_HAEI        49 HDK-SGKLTGFDVEVIRKVAEKLGLKVEFKETQWDAMYAGLNAKRFDVIANQTNPSPERL
FLIY_ECOL        56 QGD-DGKLTGFEVEFAQQLAKHLGVEASLKPTKWDGMLASLDSKRIDVVINQVTISDERK
E_coli_Gl        40 KQG--DKYVGFDVDLWAAIAKELKLDYELKPMDFSGIIPALQTKNVDLALAGITITDERK
Deinococc        51 KNE-QGELVGFDVDIAKAVAQKLNLKPEFVLTEWSGILAGLQANKYDVIVNQVGITPERQ
HISJ_E_CO        41 KNS-QGELVGFDIDLAKELCKRINTQCTFVENPLDALIPSLKAKKIDAIMSSLSITEKRQ

V_Harveyi        96 AKYLFADPYVVDG-AQITVRKGNDSIQGVEDLAGKTVAVNLGSNFEQLLRDYDKDGKINI
B_subtili       106 ETYNFTKPYAYAG-TQIVVKKDNTDIKSVDDLKGKTVAAVLGSNHAKNLESKDPDKKINI
B_subtili       119 DKYDFSDKYTTSR-AVVVTKKDNNDIKSEADVKGKTSAQSLTSNYNKLATN----AGAKV
YA80_HAEI       108 KKYSFTTPYNYSG-GVIVTKSSDNSIKSFEDLKGRKSAQSATSNWGKDAKA----AGAQI
FLIY_ECOL       115 KKYDFSTPYTISGIQALVKKGNEGTIKTADDLKGKKVGVGLGTNYEEWLRQNV--QGVDV
E_coli_Gl        98 KAIDFSDGYYKSG-LLVMVKANNNDVKSVKDLDGKVVAVKSGTGSVDYAKAN--IKTKDL
Deinococc       110 NSIGFSQPYAYSRPEIIVAKNNTFNPQSLADLKGKRVGSTLGSNYEKQLIDTG---DIKI
HISJ_E_CO       100 QEIAFTDKLYAADSRLVVAKNSDIQP-TVESLKGKRVGVLQGTTQETFGNEHWAPKGIEI

V_Harveyi       155 KTYDT--GIEHDVALGRADAFIMDRLSALE-LIKKT-GLPLQLAGEPFETI-----QNAW
B_subtili       165 KTYETQEGTLKDVAYGRVDAYVNSRTVLIA-QIKKT-GLPLKLAGDPIVYE-----QVAF
B_subtili       174 EGVEGMAQALQMIQQARVDMTYNDKLAVLN-YLKTSGNKNVKIAFETGEPQ-----STYF
YA80_HAEI       163 LVVDGLAQSLELIKQGRAEATINDKLAVLD-YFKQHPNSGLKIAYDRGDKT-----PTAF
FLIY_ECOL       173 RTYDDDPTKYQDLRVGRIDAILVDRLAALD-LVKKT-NDTLAVTGEAFSRQ-----ESGV
E_coli_Gl       155 RQFPNIDNAYMELGTNRADAVLHDTPNILY-FIKTAGNGQFKAVGDSLEAQ-----QYGI
Deinococc       167 VTYPGAPEILADLVAGRIDAAYNDRLVVNY-IINDQ-KLPVRGAGQIGDAA-----PVGI
HISJ_E_CO       159 VSYQGQDNIYSDLTAGRIDAAFQDEVAASEGFLKQPVGKDYKFGGPSVKDEKLFGVGTGM

V_Harveyi       206 PFVDNEKGRKLQAEVNKALAEMRADGTVEKISVKWFGADITK---- 248
B_subtili       218 PFAKDDAHDKLRKKVNKALDELRKDGTLKKLSEKYFNEDITVEQKH 264
B_subtili       228 TFRKGS--GEVVDQVNKALKEMKEDGTLSKISKKWFGEDVSK---- 268
YA80_HAEI       217 AFLQGE--DALITKFNQVLEALRQDGTLKQISIEWFGYDITQ---- 257
FLIY_ECOL       226 ALRKGN--EDLLKAVNDAIAEMQKDGTLQALSEKWFGADVTK---- 266
E_coli_Gl       209 AFPKGS--DELRDKVNGALKTLRENGTYNEIYKKWFGTEPK----- 248
Deinococc       220 ALKKGN--SALKDQIDKALTEMRSDGTFEKISQKWFGQDVGQP--- 261
HISJ_E_CO       219 GLRKED--NELREALNKAFAEMRADGTYEKLAKKYFDFDVYGG--- 260
""",
        )
        self.assertTrue(
            np.array_equal(
                alignment.coordinates,
                # fmt: off
                np.array(
                    [[  0,   0,   0,  13,  13,  16,  17,  17,  17,  17,  17,
                       17,  17,  17,  17,  18,  41,  41,  41,  90,  91, 109,
                      109, 121, 122, 146, 147, 148, 149, 150, 151, 160, 160,
                      183, 183, 188, 188, 202, 202, 212, 214, 247, 248, 248,
                      248],
                     [  0,   1,   2,  15,  17,  20,  21,  22,  22,  22,  22,
                       22,  23,  24,  27,  28,  51,  51,  51, 100, 101, 119,
                      119, 131, 132, 156, 157, 158, 159, 160, 161, 170, 172,
                      195, 195, 200, 200, 214, 214, 224, 226, 259, 260, 261,
                      264],
                     [  0,   1,   2,  15,  17,  20,  21,  22,  23,  25,  31,
                       34,  35,  36,  39,  40,  63,  64,  65, 114, 114, 132,
                      132, 144, 145, 169, 169, 169, 169, 169, 170, 179, 181,
                      204, 204, 209, 210, 224, 224, 234, 234, 267, 268, 268,
                      268],
                     [  0,   1,   2,  15,  17,  20,  20,  20,  20,  20,  20,
                       23,  24,  25,  28,  29,  52,  52,  53, 102, 103, 121,
                      121, 133, 134, 158, 158, 158, 158, 158, 159, 168, 170,
                      193, 193, 198, 199, 213, 213, 223, 223, 256, 257, 257,
                      257],
                     [   0,   1,   2,  15,  17,  20,  21,  22,  22,  22,  28,
                        31,  32,  32,  35,  36,  59,  59,  60, 109, 110, 128,
                       129, 141, 142, 166, 167, 168, 168, 168, 169, 178, 180,
                       203, 203, 208, 208, 222, 222, 232, 232, 265, 266, 266,
                       266],
                     [   0,   0,   0,  13,  15,  18,  19,  19,  19,  19,  19,
                        19,  19,  19,  19,  20,  43,  43,  43,  92,  93, 111,
                       111, 123, 124, 148, 149, 149, 149, 150, 151, 160, 162,
                       185, 185, 190, 191, 205, 205, 215, 215, 248, 248, 248,
                       248],
                     [   0,   0,   1,  14,  16,  19,  20,  21,  22,  22,  22,
                        25,  26,  27,  30,  31,  54,  54,  55, 104, 105, 123,
                       124, 136, 137, 161, 162, 163, 163, 163, 163, 172, 174,
                       197, 197, 202, 202, 216, 216, 226, 226, 259, 260, 261,
                       261],
                      [  0,   1,   2,  15,  17,  20,  21,  21,  21,  21,  21,
                        21,  21,  21,  21,  21,  44,  44,  45,  94,  95, 113,
                       114, 126, 126, 150, 151, 152, 153, 154, 155, 164, 166,
                       189, 190, 195, 196, 210, 215, 225, 225, 258, 259, 260,
                       260]]),
                # fmt: on
            )
        )
        self.assertEqual(
            format(alignment, "phylip"),
            """\
8 286
V_Harveyi_--MKNWIKVAVAAIA--LSAA------------------TVQAATEVKVGMSGRYFPFTFVKQ--DKLQGFEVDMWDEIGKRNDYKIEYVTANFSGLFGLLETGRIDTISNQITMTDARKAKYLFADPYVVDG-AQITVRKGNDSIQGVEDLAGKTVAVNLGSNFEQLLRDYDKDGKINIKTYDT--GIEHDVALGRADAFIMDRLSALE-LIKKT-GLPLQLAGEPFETI-----QNAWPFVDNEKGRKLQAEVNKALAEMRADGTVEKISVKWFGADITK----
B_subtilisMKMKKWTVLVVAALLAVLSACG------------NGNSSSKEDDNVLHVGATGQSYPFAYKEN--GKLTGFDVEVMEAVAKKIDMKLDWKLLEFSGLMGELQTGKLDTISNQVAVTDERKETYNFTKPYAYAG-TQIVVKKDNTDIKSVDDLKGKTVAAVLGSNHAKNLESKDPDKKINIKTYETQEGTLKDVAYGRVDAYVNSRTVLIA-QIKKT-GLPLKLAGDPIVYE-----QVAFPFAKDDAHDKLRKKVNKALDELRKDGTLKKLSEKYFNEDITVEQKH
B_subtilisMKKALLALFMVVSIAALAACGAGNDNQSKDNAKDGDLWASIKKKGVLTVGTEGTYEPFTYHDKDTDKLTGYDVEVITEVAKRLGLKVDFKETQWGSMFAGLNSKRFDVVANQVG-KTDREDKYDFSDKYTTSR-AVVVTKKDNNDIKSEADVKGKTSAQSLTSNYNKLATN----AGAKVEGVEGMAQALQMIQQARVDMTYNDKLAVLN-YLKTSGNKNVKIAFETGEPQ-----STYFTFRKGS--GEVVDQVNKALKEMKEDGTLSKISKKWFGEDVSK----
YA80_HAEINMKKLLFTTALLTGAIAFSTF-----------SHAGEIADRVEKTKTLLVGTEGTYAPFTFHDK-SGKLTGFDVEVIRKVAEKLGLKVEFKETQWDAMYAGLNAKRFDVIANQTNPSPERLKKYSFTTPYNYSG-GVIVTKSSDNSIKSFEDLKGRKSAQSATSNWGKDAKA----AGAQILVVDGLAQSLELIKQGRAEATINDKLAVLD-YFKQHPNSGLKIAYDRGDKT-----PTAFAFLQGE--DALITKFNQVLEALRQDGTLKQISIEWFGYDITQ----
FLIY_ECOLIMKLAHLGRQALMGVMAVALVAG---MSVKSFADEG-LLNKVKERGTLLVGLEGTYPPFSFQGD-DGKLTGFEVEFAQQLAKHLGVEASLKPTKWDGMLASLDSKRIDVVINQVTISDERKKKYDFSTPYTISGIQALVKKGNEGTIKTADDLKGKKVGVGLGTNYEEWLRQNV--QGVDVRTYDDDPTKYQDLRVGRIDAILVDRLAALD-LVKKT-NDTLAVTGEAFSRQ-----ESGVALRKGN--EDLLKAVNDAIAEMQKDGTLQALSEKWFGADVTK----
E_coli_Gln--MKSVLKVSLAALTLAFAVS------------------SHAADKKLVVATDTAFVPFEFKQG--DKYVGFDVDLWAAIAKELKLDYELKPMDFSGIIPALQTKNVDLALAGITITDERKKAIDFSDGYYKSG-LLVMVKANNNDVKSVKDLDGKVVAVKSGTGSVDYAKAN--IKTKDLRQFPNIDNAYMELGTNRADAVLHDTPNILY-FIKTAGNGQFKAVGDSLEAQ-----QYGIAFPKGS--DELRDKVNGALKTLRENGTYNEIYKKWFGTEPK-----
Deinococcu-MKKSLLSLKLSGLLVPSVLALS--------LSACSSPSSTLNQGTLKIAMEGTYPPFTSKNE-QGELVGFDVDIAKAVAQKLNLKPEFVLTEWSGILAGLQANKYDVIVNQVGITPERQNSIGFSQPYAYSRPEIIVAKNNTFNPQSLADLKGKRVGSTLGSNYEKQLIDTG---DIKIVTYPGAPEILADLVAGRIDAAYNDRLVVNY-IINDQ-KLPVRGAGQIGDAA-----PVGIALKKGN--SALKDQIDKALTEMRSDGTFEKISQKWFGQDVGQP---
HISJ_E_COLMKKLVLSLSLVLAFSSATAAF-------------------AAIPQNIRIGTDPTYAPFESKNS-QGELVGFDIDLAKELCKRINTQCTFVENPLDALIPSLKAKKIDAIMSSLSITEKRQQEIAFTDKLYAADSRLVVAKNSDIQP-TVESLKGKRVGVLQGTTQETFGNEHWAPKGIEIVSYQGQDNIYSDLTAGRIDAAFQDEVAASEGFLKQPVGKDYKFGGPSVKDEKLFGVGTGMGLRKED--NELREALNKAFAEMRADGTYEKLAKKYFDFDVYGG---
""",
        )
        counts = alignment.counts(substitution_matrix)
        self.assertEqual(
            repr(counts),
            "<AlignmentCounts object (substitution score = 10177.0; 6978 aligned letters; 2258 identities; 4720 mismatches; 3674 positives; 548 gaps) at 0x%x>"
            % id(counts),
        )
        self.assertEqual(
            str(counts),
            """\
AlignmentCounts object with
    substitution_score = 10177.0,
    aligned = 6978:
        identities = 2258,
        positives = 3674,
        mismatches = 4720.
    gaps = 548:
        left_gaps = 27:
            left_insertions = 15:
                open_left_insertions = 4,
                extend_left_insertions = 11;
            left_deletions = 12:
                open_left_deletions = 3,
                extend_left_deletions = 9;
        internal_gaps = 478:
            internal_insertions = 252:
                open_internal_insertions = 99,
                extend_internal_insertions = 153;
            internal_deletions = 226:
                open_internal_deletions = 69,
                extend_internal_deletions = 157;
        right_gaps = 43:
            right_insertions = 16:
                open_right_insertions = 11,
                extend_right_insertions = 5;
            right_deletions = 27:
                open_right_deletions = 10,
                extend_right_deletions = 17.
""",
        )
        self.assertEqual(counts.left_insertions, 15)
        self.assertEqual(counts.left_deletions, 12)
        self.assertEqual(counts.right_insertions, 16)
        self.assertEqual(counts.right_deletions, 27)
        self.assertEqual(counts.internal_insertions, 252)
        self.assertEqual(counts.internal_deletions, 226)
        self.assertEqual(counts.left_gaps, 27)
        self.assertEqual(counts.right_gaps, 43)
        self.assertEqual(counts.internal_gaps, 478)
        self.assertEqual(counts.insertions, 283)
        self.assertEqual(counts.deletions, 265)
        self.assertEqual(counts.gaps, 548)
        self.assertEqual(counts.aligned, 6978)
        self.assertEqual(counts.identities, 2258)
        self.assertEqual(counts.mismatches, 4720)
        self.assertEqual(counts.positives, 3674)

    def test_two_and_three(self):
        paths = ("Phylip/two.dat", "Phylip/three.dat")
        # derived from http://atgc.lirmm.fr/phyml/usersguide.html
        for path in paths:
            with open(path) as stream:
                alignments = Align.parse(stream, "phylip")
                alignment = next(alignments)
                with self.assertRaises(StopIteration):
                    next(alignments)
            self.assertEqual(
                repr(alignment),
                "<Alignment object (5 rows x 60 columns) at 0x%x>" % id(alignment),
            )
            self.assertEqual(len(alignment), 5)
            self.assertEqual(alignment.sequences[0].id, "Tax1")
            self.assertEqual(alignment.sequences[1].id, "Tax2")
            self.assertEqual(alignment.sequences[2].id, "Tax3")
            self.assertEqual(alignment.sequences[3].id, "Tax4")
            self.assertEqual(alignment.sequences[4].id, "Tax5")
            self.assertEqual(
                alignment.sequences[0].seq,
                "CCATCTCACGGTCGGTACGATACACCTGCTTTTGGCAGGAAATGGTCAATATTACAAGGT",
            )
            self.assertEqual(
                alignment.sequences[1].seq,
                "CCATCTCACGGTCAGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAACATTAAAAGAT",
            )
            self.assertEqual(
                alignment.sequences[2].seq,
                "CCATCTCCCGCTCAGTAAGATACCCCTGCTGTTGGCGGGAAATCGTCAATATTAAAAGGT",
            )
            self.assertEqual(
                alignment.sequences[3].seq,
                "TCATCTCATGGTCAATAAGATACTCCTGCTTTTGGCGGGAAATGGTCAATCTTAAAAGGT",
            )
            self.assertEqual(
                alignment.sequences[4].seq,
                "CCATCTCACGGTCGGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAATATTAAAAGGT",
            )
            self.assertEqual(
                alignment[0],
                "CCATCTCACGGTCGGTACGATACACCTGCTTTTGGCAGGAAATGGTCAATATTACAAGGT",
            )
            self.assertEqual(
                alignment[1],
                "CCATCTCACGGTCAGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAACATTAAAAGAT",
            )
            self.assertEqual(
                alignment[2],
                "CCATCTCCCGCTCAGTAAGATACCCCTGCTGTTGGCGGGAAATCGTCAATATTAAAAGGT",
            )
            self.assertEqual(
                alignment[3],
                "TCATCTCATGGTCAATAAGATACTCCTGCTTTTGGCGGGAAATGGTCAATCTTAAAAGGT",
            )
            self.assertEqual(
                alignment[4],
                "CCATCTCACGGTCGGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAATATTAAAAGGT",
            )
            self.check_reading_writing(path)
            self.assertTrue(
                np.array_equal(
                    alignment.coordinates,
                    np.array([[0, 60], [0, 60], [0, 60], [0, 60], [0, 60]]),
                )
            )
            self.assertEqual(
                str(alignment),
                """\
Tax1              0 CCATCTCACGGTCGGTACGATACACCTGCTTTTGGCAGGAAATGGTCAATATTACAAGGT
Tax2              0 CCATCTCACGGTCAGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAACATTAAAAGAT
Tax3              0 CCATCTCCCGCTCAGTAAGATACCCCTGCTGTTGGCGGGAAATCGTCAATATTAAAAGGT
Tax4              0 TCATCTCATGGTCAATAAGATACTCCTGCTTTTGGCGGGAAATGGTCAATCTTAAAAGGT
Tax5              0 CCATCTCACGGTCGGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAATATTAAAAGGT

Tax1             60 
Tax2             60 
Tax3             60 
Tax4             60 
Tax5             60 
""",
            )
            self.assertEqual(
                format(alignment, "phylip"),
                """\
5 60
Tax1      CCATCTCACGGTCGGTACGATACACCTGCTTTTGGCAGGAAATGGTCAATATTACAAGGT
Tax2      CCATCTCACGGTCAGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAACATTAAAAGAT
Tax3      CCATCTCCCGCTCAGTAAGATACCCCTGCTGTTGGCGGGAAATCGTCAATATTAAAAGGT
Tax4      TCATCTCATGGTCAATAAGATACTCCTGCTTTTGGCGGGAAATGGTCAATCTTAAAAGGT
Tax5      CCATCTCACGGTCGGTAAGATACACCTGCTTTTGGCGGGAAATGGTCAATATTAAAAGGT
""",
            )
            counts = alignment.counts()
            self.assertEqual(
                repr(counts),
                "<AlignmentCounts object (600 aligned letters; 535 identities; 65 mismatches; 0 gaps) at 0x%x>"
                % id(counts),
            )
            self.assertEqual(
                str(counts),
                """\
AlignmentCounts object with
    aligned = 600:
        identities = 535,
        mismatches = 65.
    gaps = 0:
        left_gaps = 0:
            left_insertions = 0:
                open_left_insertions = 0,
                extend_left_insertions = 0;
            left_deletions = 0:
                open_left_deletions = 0,
                extend_left_deletions = 0;
        internal_gaps = 0:
            internal_insertions = 0:
                open_internal_insertions = 0,
                extend_internal_insertions = 0;
            internal_deletions = 0:
                open_internal_deletions = 0,
                extend_internal_deletions = 0;
        right_gaps = 0:
            right_insertions = 0:
                open_right_insertions = 0,
                extend_right_insertions = 0;
            right_deletions = 0:
                open_right_deletions = 0,
                extend_right_deletions = 0.
""",
            )
            self.assertEqual(counts.left_insertions, 0)
            self.assertEqual(counts.left_deletions, 0)
            self.assertEqual(counts.right_insertions, 0)
            self.assertEqual(counts.right_deletions, 0)
            self.assertEqual(counts.internal_insertions, 0)
            self.assertEqual(counts.internal_deletions, 0)
            self.assertEqual(counts.left_gaps, 0)
            self.assertEqual(counts.right_gaps, 0)
            self.assertEqual(counts.internal_gaps, 0)
            self.assertEqual(counts.insertions, 0)
            self.assertEqual(counts.deletions, 0)
            self.assertEqual(counts.gaps, 0)
            self.assertEqual(counts.aligned, 600)
            self.assertEqual(counts.identities, 535)
            self.assertEqual(counts.mismatches, 65)

    def test_four(self):
        path = "Phylip/four.dat"
        # File derived from here:
        # http://evolution.genetics.washington.edu/phylip/doc/sequence.html
        # Note the lack of any white space between names 2 and 3 and their seqs.
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            alignment = next(alignments)
            with self.assertRaises(StopIteration):
                next(alignments)
        self.assertTrue(
            np.array_equal(
                np.array(alignment, "U"),
                # fmt: off
np.array([['A', 'A', 'G', 'C', 'T', 'N', 'G', 'G', 'G', 'C', 'A', 'T', 'T',
           'T', 'C', 'A', 'G', 'G', 'G', 'T', 'G', 'A', 'G', 'C', 'C', 'C',
           'G', 'G', 'G', 'C', 'A', 'A', 'T', 'A', 'C', 'A', 'G', 'G', 'G',
           'T', 'A', 'T'],
          ['A', 'A', 'G', 'C', 'C', 'T', 'T', 'G', 'G', 'C', 'A', 'G', 'T',
           'G', 'C', 'A', 'G', 'G', 'G', 'T', 'G', 'A', 'G', 'C', 'C', 'G',
           'T', 'G', 'G', 'C', 'C', 'G', 'G', 'G', 'C', 'A', 'C', 'G', 'G',
           'T', 'A', 'T'],
          ['A', 'C', 'C', 'G', 'G', 'T', 'T', 'G', 'G', 'C', 'C', 'G', 'T',
           'T', 'C', 'A', 'G', 'G', 'G', 'T', 'A', 'C', 'A', 'G', 'G', 'T',
           'T', 'G', 'G', 'C', 'C', 'G', 'T', 'T', 'C', 'A', 'G', 'G', 'G',
           'T', 'A', 'A'],
          ['A', 'A', 'A', 'C', 'C', 'C', 'T', 'T', 'G', 'C', 'C', 'G', 'T',
           'T', 'A', 'C', 'G', 'C', 'T', 'T', 'A', 'A', 'A', 'C', 'C', 'G',
           'A', 'G', 'G', 'C', 'C', 'G', 'G', 'G', 'A', 'C', 'A', 'C', 'T',
           'C', 'A', 'T'],
          ['A', 'A', 'A', 'C', 'C', 'C', 'T', 'T', 'G', 'C', 'C', 'G', 'G',
           'T', 'A', 'C', 'G', 'C', 'T', 'T', 'A', 'A', 'A', 'C', 'C', 'A',
           'T', 'T', 'G', 'C', 'C', 'G', 'G', 'T', 'A', 'C', 'G', 'C', 'T',
           'T', 'A', 'A']], dtype='U')
                # fmt: on
            )
        )
        self.assertEqual(
            repr(alignment),
            "<Alignment object (5 rows x 42 columns) at 0x%x>" % id(alignment),
        )
        self.assertEqual(len(alignment), 5)
        self.assertEqual(alignment.sequences[0].id, "Turkey")
        self.assertEqual(alignment.sequences[1].id, "Salmo gair")
        self.assertEqual(alignment.sequences[2].id, "H. Sapiens")
        self.assertEqual(alignment.sequences[3].id, "Chimp")
        self.assertEqual(alignment.sequences[4].id, "Gorilla")
        self.assertEqual(
            alignment.sequences[0].seq, "AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT"
        )
        self.assertEqual(
            alignment.sequences[1].seq, "AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT"
        )
        self.assertEqual(
            alignment.sequences[2].seq, "ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA"
        )
        self.assertEqual(
            alignment.sequences[3].seq, "AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT"
        )
        self.assertEqual(
            alignment.sequences[4].seq, "AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA"
        )
        self.assertEqual(alignment[0], "AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT")
        self.assertEqual(alignment[1], "AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT")
        self.assertEqual(alignment[2], "ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA")
        self.assertEqual(alignment[3], "AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT")
        self.assertEqual(alignment[4], "AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA")
        self.check_reading_writing(path)
        self.assertTrue(
            np.array_equal(
                alignment.coordinates,
                np.array([[0, 42], [0, 42], [0, 42], [0, 42], [0, 42]]),
            )
        )
        self.assertEqual(
            str(alignment),
            """\
Turkey            0 AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT 42
Salmo gai         0 AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT 42
H. Sapien         0 ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA 42
Chimp             0 AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT 42
Gorilla           0 AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA 42
""",
        )
        self.assertEqual(
            format(alignment, "phylip"),
            """\
5 42
Turkey    AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT
Salmo gairAAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT
H. SapiensACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA
Chimp     AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT
Gorilla   AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA
""",
        )
        counts = alignment.counts()
        self.assertEqual(
            repr(counts),
            "<AlignmentCounts object (420 aligned letters; 230 identities; 190 mismatches; 0 gaps) at 0x%x>"
            % id(counts),
        )
        self.assertEqual(
            str(counts),
            """\
AlignmentCounts object with
    aligned = 420:
        identities = 230,
        mismatches = 190.
    gaps = 0:
        left_gaps = 0:
            left_insertions = 0:
                open_left_insertions = 0,
                extend_left_insertions = 0;
            left_deletions = 0:
                open_left_deletions = 0,
                extend_left_deletions = 0;
        internal_gaps = 0:
            internal_insertions = 0:
                open_internal_insertions = 0,
                extend_internal_insertions = 0;
            internal_deletions = 0:
                open_internal_deletions = 0,
                extend_internal_deletions = 0;
        right_gaps = 0:
            right_insertions = 0:
                open_right_insertions = 0,
                extend_right_insertions = 0;
            right_deletions = 0:
                open_right_deletions = 0,
                extend_right_deletions = 0.
""",
        )
        self.assertEqual(counts.left_insertions, 0)
        self.assertEqual(counts.left_deletions, 0)
        self.assertEqual(counts.right_insertions, 0)
        self.assertEqual(counts.right_deletions, 0)
        self.assertEqual(counts.internal_insertions, 0)
        self.assertEqual(counts.internal_deletions, 0)
        self.assertEqual(counts.left_gaps, 0)
        self.assertEqual(counts.right_gaps, 0)
        self.assertEqual(counts.internal_gaps, 0)
        self.assertEqual(counts.insertions, 0)
        self.assertEqual(counts.deletions, 0)
        self.assertEqual(counts.gaps, 0)
        self.assertEqual(counts.aligned, 420)
        self.assertEqual(counts.identities, 230)
        self.assertEqual(counts.mismatches, 190)

    def test_five_and_six(self):
        paths = ("Phylip/five.dat", "Phylip/six.dat")
        # http://evolution.genetics.washington.edu/phylip/doc/sequence.html
        for path in paths:
            with open(path) as stream:
                alignments = Align.parse(stream, "phylip")
                alignment = next(alignments)
                with self.assertRaises(StopIteration):
                    next(alignments)
            self.assertEqual(
                repr(alignment),
                "<Alignment object (5 rows x 42 columns) at 0x%x>" % id(alignment),
            )
            self.assertEqual(len(alignment), 5)
            self.assertEqual(alignment.sequences[0].id, "Turkey")
            self.assertEqual(alignment.sequences[1].id, "Salmo gair")
            self.assertEqual(alignment.sequences[2].id, "H. Sapiens")
            self.assertEqual(alignment.sequences[3].id, "Chimp")
            self.assertEqual(alignment.sequences[4].id, "Gorilla")
            self.assertEqual(
                alignment.sequences[0].seq, "AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT"
            )
            self.assertEqual(
                alignment.sequences[1].seq, "AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT"
            )
            self.assertEqual(
                alignment.sequences[2].seq, "ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA"
            )
            self.assertEqual(
                alignment.sequences[3].seq, "AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT"
            )
            self.assertEqual(
                alignment.sequences[4].seq, "AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA"
            )
            self.assertEqual(alignment[0], "AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT")
            self.assertEqual(alignment[1], "AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT")
            self.assertEqual(alignment[2], "ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA")
            self.assertEqual(alignment[3], "AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT")
            self.assertEqual(alignment[4], "AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA")
            self.assertEqual(
                str(alignment),
                """\
Turkey            0 AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT 42
Salmo gai         0 AAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT 42
H. Sapien         0 ACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA 42
Chimp             0 AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT 42
Gorilla           0 AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA 42
""",
            )
            self.assertTrue(
                np.array_equal(
                    alignment.coordinates,
                    np.array([[0, 42], [0, 42], [0, 42], [0, 42], [0, 42]]),
                )
            )
            self.assertEqual(
                format(alignment, "phylip"),
                """\
5 42
Turkey    AAGCTNGGGCATTTCAGGGTGAGCCCGGGCAATACAGGGTAT
Salmo gairAAGCCTTGGCAGTGCAGGGTGAGCCGTGGCCGGGCACGGTAT
H. SapiensACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA
Chimp     AAACCCTTGCCGTTACGCTTAAACCGAGGCCGGGACACTCAT
Gorilla   AAACCCTTGCCGGTACGCTTAAACCATTGCCGGTACGCTTAA
""",
            )
            self.check_reading_writing(path)
            counts = alignment.counts()
            self.assertEqual(
                repr(counts),
                "<AlignmentCounts object (420 aligned letters; 230 identities; 190 mismatches; 0 gaps) at 0x%x>"
                % id(counts),
            )
            self.assertEqual(
                str(counts),
                """\
AlignmentCounts object with
    aligned = 420:
        identities = 230,
        mismatches = 190.
    gaps = 0:
        left_gaps = 0:
            left_insertions = 0:
                open_left_insertions = 0,
                extend_left_insertions = 0;
            left_deletions = 0:
                open_left_deletions = 0,
                extend_left_deletions = 0;
        internal_gaps = 0:
            internal_insertions = 0:
                open_internal_insertions = 0,
                extend_internal_insertions = 0;
            internal_deletions = 0:
                open_internal_deletions = 0,
                extend_internal_deletions = 0;
        right_gaps = 0:
            right_insertions = 0:
                open_right_insertions = 0,
                extend_right_insertions = 0;
            right_deletions = 0:
                open_right_deletions = 0,
                extend_right_deletions = 0.
""",
            )
            self.assertEqual(counts.left_insertions, 0)
            self.assertEqual(counts.left_deletions, 0)
            self.assertEqual(counts.right_insertions, 0)
            self.assertEqual(counts.right_deletions, 0)
            self.assertEqual(counts.internal_insertions, 0)
            self.assertEqual(counts.internal_deletions, 0)
            self.assertEqual(counts.left_gaps, 0)
            self.assertEqual(counts.right_gaps, 0)
            self.assertEqual(counts.internal_gaps, 0)
            self.assertEqual(counts.insertions, 0)
            self.assertEqual(counts.deletions, 0)
            self.assertEqual(counts.gaps, 0)
            self.assertEqual(counts.aligned, 420)
            self.assertEqual(counts.identities, 230)
            self.assertEqual(counts.mismatches, 190)

    def test_interlaced(self):
        path = "Phylip/interlaced.phy"
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            self.check_sequential_interlaced(alignments)
            alignments = iter(alignments)
            self.check_sequential_interlaced(alignments)
        with Align.parse(path, "phylip") as alignments:
            self.check_sequential_interlaced(alignments)
        with self.assertRaises(AttributeError):
            alignments._stream
        with Align.parse(path, "phylip") as alignments:
            pass
        with self.assertRaises(AttributeError):
            alignments._stream
        self.check_reading_writing(path)

    def test_sequential(self):
        path = "Phylip/sequential.phy"
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            self.check_sequential_interlaced(alignments)
            alignments = iter(alignments)
            self.check_sequential_interlaced(alignments)
        with Align.parse(path, "phylip") as alignments:
            self.check_sequential_interlaced(alignments)
        with self.assertRaises(AttributeError):
            alignments._stream
        with Align.parse(path, "phylip") as alignments:
            pass
        with self.assertRaises(AttributeError):
            alignments._stream
        self.check_reading_writing(path)

    def check_sequential_interlaced(self, alignments):
        alignment = next(alignments)
        with self.assertRaises(StopIteration):
            next(alignments)
        self.assertEqual(
            repr(alignment),
            "<Alignment object (3 rows x 384 columns) at 0x%x>" % id(alignment),
        )
        self.assertEqual(len(alignment), 3)
        self.assertEqual(alignment.sequences[0].id, "CYS1_DICDI")
        self.assertEqual(alignment.sequences[1].id, "ALEU_HORVU")
        self.assertEqual(alignment.sequences[2].id, "CATH_HUMAN")
        self.assertEqual(
            alignment.sequences[0].seq,
            "MKVILLFVLAVFTVFVSSRGIPPEEQSQFLEFQDKFNKKYSHEEYLERFEIFKSNLGKIEELNLIAINHKADTKFGVNKFADLSSDEFKNYYLNNKEAIFTDDLPVADYLDDEFINSIPTAFDWRTRGAVTPVKNQGQCGSCWSFSTTGNVEGQHFISQNKLVSLSEQNLVDCDHECMEYEGEEACDEGCNGGLQPNAYNYIIKNGGIQTESSYPYTAETGTQCNFNSANIGAKISNFTMIPKNETVMAGYIVSTGPLAIAADAVEWQFYIGGVFDIPCNPNSLDHGILIVGYSAKNTIFRKNMPYWIVKNSWGADWGEQGYIYLRRGKNTCGVSNFVSTSII",
        )
        self.assertEqual(
            alignment.sequences[1].seq,
            "MAHARVLLLALAVLATAAVAVASSSSFADSNPIRPVTDRAASTLESAVLGALGRTRHALRFARFAVRYGKSYESAAEVRRRFRIFSESLEEVRSTNRKGLPYRLGINRFSDMSWEEFQATRLGAAQTCSATLAGNHLMRDAAALPETKDWREDGIVSPVKNQAHCGSCWTFSTTGALEAAYTQATGKNISLSEQQLVDCAGGFNNFGCNGGLPSQAFEYIKYNGGIDTEESYPYKGVNGVCHYKAENAAVQVLDSVNITLNAEDELKNAVGLVRPVSVAFQVIDGFRQYKSGVYTSDHCGTTPDDVNHAVLAVGYGVENGVPYWLIKNSWGADWGDNGYFKMEMGKNMCAIATCASYPVVAA",
        )
        self.assertEqual(
            alignment.sequences[2].seq,
            "MWATLPLLCAGAWLLGVPVCGAAELSVNSLEKFHFKSWMSKHRKTYSTEEYHHRLQTFASNWRKINAHNNGNHTFKMALNQFSDMSFAEIKHKYLWSEPQNCSATKSNYLRGTGPYPPSVDWRKKGNFVSPVKNQGACGSCWTFSTTGALESAIAIATGKMLSLAEQQLVDCAQDFNNYGCQGGLPSQAFEYILYNKGIMGEDTYPYQGKDGYCKFQPGKAIGFVKDVANITIYDEEAMVEAVALYNPVSFAFEVTQDFMMYRTGIYSSTSCHKTPDKVNHAVLAVGYGEKNGIPYWIVKNSWGPQWGMNGYFLIERGKNMCGLAACASYPIPLV",
        )
        self.assertEqual(
            alignment[0],
            "-----MKVILLFVLAVFTVFVSS---------------RGIPPEEQ------------SQFLEFQDKFNKKY-SHEEYLERFEIFKSNLGKIEELNLIAINHKADTKFGVNKFADLSSDEFKNYYLNNKEAIFTDDLPVADYLDDEFINSIPTAFDWRTRG-AVTPVKNQGQCGSCWSFSTTGNVEGQHFISQNKLVSLSEQNLVDCDHECMEYEGEEACDEGCNGGLQPNAYNYIIKNGGIQTESSYPYTAETGTQCNFNSANIGAKISNFTMIP-KNETVMAGYIVSTGPLAIAADAVE-WQFYIGGVF-DIPCN--PNSLDHGILIVGYSAKNTIFRKNMPYWIVKNSWGADWGEQGYIYLRRGKNTCGVSNFVSTSII--",
        )
        self.assertEqual(
            alignment[1],
            "MAHARVLLLALAVLATAAVAVASSSSFADSNPIRPVTDRAASTLESAVLGALGRTRHALRFARFAVRYGKSYESAAEVRRRFRIFSESLEEVRSTN----RKGLPYRLGINRFSDMSWEEFQATRL-GAAQTCSATLAGNHLMRDA--AALPETKDWREDG-IVSPVKNQAHCGSCWTFSTTGALEAAYTQATGKNISLSEQQLVDCAGGFNNF--------GCNGGLPSQAFEYIKYNGGIDTEESYPYKGVNGV-CHYKAENAAVQVLDSVNITLNAEDELKNAVGLVRPVSVAFQVIDGFRQYKSGVYTSDHCGTTPDDVNHAVLAVGYGVENGV-----PYWLIKNSWGADWGDNGYFKMEMGKNMCAIATCASYPVVAA",
        )
        self.assertEqual(
            alignment[2],
            "------MWATLPLLCAGAWLLGV--------PVCGAAELSVNSLEK------------FHFKSWMSKHRKTY-STEEYHHRLQTFASNWRKINAHN----NGNHTFKMALNQFSDMSFAEIKHKYLWSEPQNCSAT--KSNYLRGT--GPYPPSVDWRKKGNFVSPVKNQGACGSCWTFSTTGALESAIAIATGKMLSLAEQQLVDCAQDFNNY--------GCQGGLPSQAFEYILYNKGIMGEDTYPYQGKDGY-CKFQPGKAIGFVKDVANITIYDEEAMVEAVALYNPVSFAFEVTQDFMMYRTGIYSSTSCHKTPDKVNHAVLAVGYGEKNGI-----PYWIVKNSWGPQWGMNGYFLIERGKNMCGLAACASYPIPLV",
        )
        self.assertEqual(
            str(alignment),
            """\
CYS1_DICD         0 -----MKVILLFVLAVFTVFVSS---------------RGIPPEEQ------------SQ
ALEU_HORV         0 MAHARVLLLALAVLATAAVAVASSSSFADSNPIRPVTDRAASTLESAVLGALGRTRHALR
CATH_HUMA         0 ------MWATLPLLCAGAWLLGV--------PVCGAAELSVNSLEK------------FH

CYS1_DICD        28 FLEFQDKFNKKY-SHEEYLERFEIFKSNLGKIEELNLIAINHKADTKFGVNKFADLSSDE
ALEU_HORV        60 FARFAVRYGKSYESAAEVRRRFRIFSESLEEVRSTN----RKGLPYRLGINRFSDMSWEE
CATH_HUMA        34 FKSWMSKHRKTY-STEEYHHRLQTFASNWRKINAHN----NGNHTFKMALNQFSDMSFAE

CYS1_DICD        87 FKNYYLNNKEAIFTDDLPVADYLDDEFINSIPTAFDWRTRG-AVTPVKNQGQCGSCWSFS
ALEU_HORV       116 FQATRL-GAAQTCSATLAGNHLMRDA--AALPETKDWREDG-IVSPVKNQAHCGSCWTFS
CATH_HUMA        89 IKHKYLWSEPQNCSAT--KSNYLRGT--GPYPPSVDWRKKGNFVSPVKNQGACGSCWTFS

CYS1_DICD       146 TTGNVEGQHFISQNKLVSLSEQNLVDCDHECMEYEGEEACDEGCNGGLQPNAYNYIIKNG
ALEU_HORV       172 TTGALEAAYTQATGKNISLSEQQLVDCAGGFNNF--------GCNGGLPSQAFEYIKYNG
CATH_HUMA       145 TTGALESAIAIATGKMLSLAEQQLVDCAQDFNNY--------GCQGGLPSQAFEYILYNK

CYS1_DICD       206 GIQTESSYPYTAETGTQCNFNSANIGAKISNFTMIP-KNETVMAGYIVSTGPLAIAADAV
ALEU_HORV       224 GIDTEESYPYKGVNGV-CHYKAENAAVQVLDSVNITLNAEDELKNAVGLVRPVSVAFQVI
CATH_HUMA       197 GIMGEDTYPYQGKDGY-CKFQPGKAIGFVKDVANITIYDEEAMVEAVALYNPVSFAFEVT

CYS1_DICD       265 E-WQFYIGGVF-DIPCN--PNSLDHGILIVGYSAKNTIFRKNMPYWIVKNSWGADWGEQG
ALEU_HORV       283 DGFRQYKSGVYTSDHCGTTPDDVNHAVLAVGYGVENGV-----PYWLIKNSWGADWGDNG
CATH_HUMA       256 QDFMMYRTGIYSSTSCHKTPDKVNHAVLAVGYGEKNGI-----PYWIVKNSWGPQWGMNG

CYS1_DICD       321 YIYLRRGKNTCGVSNFVSTSII-- 343
ALEU_HORV       338 YFKMEMGKNMCAIATCASYPVVAA 362
CATH_HUMA       311 YFLIERGKNMCGLAACASYPIPLV 335
""",
        )
        self.assertTrue(
            np.array_equal(
                alignment.coordinates,
                # fmt: off
                np.array(
       [[ 0,   0,   1,  18,  18,  18,  26,  26,  40,  40,  63,  67,  93,
         94, 103, 105, 113, 115, 128, 128, 180, 188, 222, 223, 242, 242,
        266, 266, 275, 275, 280, 280, 299, 304, 343, 343],
       [  0,   5,   6,  23,  31,  38,  46,  58,  72,  73,  96,  96, 122,
        122, 131, 133, 141, 141, 154, 154, 206, 206, 240, 240, 259, 260,
        284, 285, 294, 295, 300, 302, 321, 321, 360, 362],
       [  0,   0,   0,  17,  17,  24,  32,  32,  46,  46,  69,  69,  95,
         96, 105, 105, 113, 113, 126, 127, 179, 179, 213, 213, 232, 233,
        257, 258, 267, 268, 273, 275, 294, 294, 333, 335]])
                # fmt: on
            )
        )
        self.assertEqual(
            format(alignment, "phylip"),
            """\
3 384
CYS1_DICDI-----MKVILLFVLAVFTVFVSS---------------RGIPPEEQ------------SQFLEFQDKFNKKY-SHEEYLERFEIFKSNLGKIEELNLIAINHKADTKFGVNKFADLSSDEFKNYYLNNKEAIFTDDLPVADYLDDEFINSIPTAFDWRTRG-AVTPVKNQGQCGSCWSFSTTGNVEGQHFISQNKLVSLSEQNLVDCDHECMEYEGEEACDEGCNGGLQPNAYNYIIKNGGIQTESSYPYTAETGTQCNFNSANIGAKISNFTMIP-KNETVMAGYIVSTGPLAIAADAVE-WQFYIGGVF-DIPCN--PNSLDHGILIVGYSAKNTIFRKNMPYWIVKNSWGADWGEQGYIYLRRGKNTCGVSNFVSTSII--
ALEU_HORVUMAHARVLLLALAVLATAAVAVASSSSFADSNPIRPVTDRAASTLESAVLGALGRTRHALRFARFAVRYGKSYESAAEVRRRFRIFSESLEEVRSTN----RKGLPYRLGINRFSDMSWEEFQATRL-GAAQTCSATLAGNHLMRDA--AALPETKDWREDG-IVSPVKNQAHCGSCWTFSTTGALEAAYTQATGKNISLSEQQLVDCAGGFNNF--------GCNGGLPSQAFEYIKYNGGIDTEESYPYKGVNGV-CHYKAENAAVQVLDSVNITLNAEDELKNAVGLVRPVSVAFQVIDGFRQYKSGVYTSDHCGTTPDDVNHAVLAVGYGVENGV-----PYWLIKNSWGADWGDNGYFKMEMGKNMCAIATCASYPVVAA
CATH_HUMAN------MWATLPLLCAGAWLLGV--------PVCGAAELSVNSLEK------------FHFKSWMSKHRKTY-STEEYHHRLQTFASNWRKINAHN----NGNHTFKMALNQFSDMSFAEIKHKYLWSEPQNCSAT--KSNYLRGT--GPYPPSVDWRKKGNFVSPVKNQGACGSCWTFSTTGALESAIAIATGKMLSLAEQQLVDCAQDFNNY--------GCQGGLPSQAFEYILYNKGIMGEDTYPYQGKDGY-CKFQPGKAIGFVKDVANITIYDEEAMVEAVALYNPVSFAFEVTQDFMMYRTGIYSSTSCHKTPDKVNHAVLAVGYGEKNGI-----PYWIVKNSWGPQWGMNGYFLIERGKNMCGLAACASYPIPLV
""",
        )
        counts = alignment.counts(substitution_matrix)
        self.assertEqual(
            repr(counts),
            "<AlignmentCounts object (substitution score = 2116.0; 975 aligned letters; 400 identities; 575 mismatches; 563 positives; 130 gaps) at 0x%x>"
            % id(counts),
        )
        self.assertEqual(
            str(counts),
            """\
AlignmentCounts object with
    substitution_score = 2116.0,
    aligned = 975:
        identities = 400,
        positives = 563,
        mismatches = 575.
    gaps = 130:
        left_gaps = 12:
            left_insertions = 5:
                open_left_insertions = 1,
                extend_left_insertions = 4;
            left_deletions = 7:
                open_left_deletions = 2,
                extend_left_deletions = 5;
        internal_gaps = 114:
            internal_insertions = 48:
                open_internal_insertions = 15,
                extend_internal_insertions = 33;
            internal_deletions = 66:
                open_internal_deletions = 16,
                extend_internal_deletions = 50;
        right_gaps = 4:
            right_insertions = 4:
                open_right_insertions = 2,
                extend_right_insertions = 2;
            right_deletions = 0:
                open_right_deletions = 0,
                extend_right_deletions = 0.
""",
        )
        self.assertEqual(counts.left_insertions, 5)
        self.assertEqual(counts.left_deletions, 7)
        self.assertEqual(counts.right_insertions, 4)
        self.assertEqual(counts.right_deletions, 0)
        self.assertEqual(counts.internal_insertions, 48)
        self.assertEqual(counts.internal_deletions, 66)
        self.assertEqual(counts.left_gaps, 12)
        self.assertEqual(counts.right_gaps, 4)
        self.assertEqual(counts.internal_gaps, 114)
        self.assertEqual(counts.insertions, 57)
        self.assertEqual(counts.deletions, 73)
        self.assertEqual(counts.gaps, 130)
        self.assertEqual(counts.aligned, 975)
        self.assertEqual(counts.identities, 400)
        self.assertEqual(counts.mismatches, 575)
        self.assertEqual(counts.positives, 563)

    def test_interlaced2(self):
        path = "Phylip/interlaced2.phy"
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            self.check_sequential_interlaced2(alignments)
            alignments = iter(alignments)
            self.check_sequential_interlaced2(alignments)
        with Align.parse(path, "phylip") as alignments:
            self.check_sequential_interlaced2(alignments)
        with self.assertRaises(AttributeError):
            alignments._stream
        with Align.parse(path, "phylip") as alignments:
            pass
        with self.assertRaises(AttributeError):
            alignments._stream
        self.check_reading_writing(path)

    def test_sequential2(self):
        path = "Phylip/sequential2.phy"
        with open(path) as stream:
            alignments = Align.parse(stream, "phylip")
            self.check_sequential_interlaced2(alignments)
            alignments = iter(alignments)
            self.check_sequential_interlaced2(alignments)
        with Align.parse(path, "phylip") as alignments:
            self.check_sequential_interlaced2(alignments)
        with self.assertRaises(AttributeError):
            alignments._stream
        with Align.parse(path, "phylip") as alignments:
            pass
        with self.assertRaises(AttributeError):
            alignments._stream
        self.check_reading_writing(path)

    def check_sequential_interlaced2(self, alignments):
        alignment = next(alignments)
        with self.assertRaises(StopIteration):
            next(alignments)
        self.assertEqual(
            repr(alignment),
            "<Alignment object (4 rows x 131 columns) at 0x%x>" % id(alignment),
        )
        self.assertEqual(len(alignment), 4)
        self.assertEqual(alignment.sequences[0].id, "IXI_234")
        self.assertEqual(alignment.sequences[1].id, "IXI_235")
        self.assertEqual(alignment.sequences[2].id, "IXI_236")
        self.assertEqual(alignment.sequences[3].id, "IXI_237")
        self.assertEqual(
            alignment.sequences[0].seq,
            "TSPASIRPPAGPSSRPAMVSSRRTRPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE",
        )
        self.assertEqual(
            alignment.sequences[1].seq,
            "TSPASIRPPAGPSSRRPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGWRASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE",
        )
        self.assertEqual(
            alignment.sequences[2].seq,
            "TSPASIRPPAGPSSRPAMVSSRRPSPPPPRRPPGRPCCSAAPPRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSRGSRPPRFAPPLMSSCITSTTGPPPPAGDRSHE",
        )
        self.assertEqual(
            alignment.sequences[3].seq,
            "TSPASLRPPAGPSSRPAMVSSRRRPSPPGPRRPTCSAAPRRPQATGGYKTCSGTCTTSTSTRHRGRSGYSARTTTAACLRASRKSMRAACSRGSRPNRFAPTLMSSCLTSTTGPPAYAGDRSHE",
        )
        self.assertEqual(
            alignment[0],
            "TSPASIRPPAGPSSRPAMVSSRRTRPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE",
        )
        self.assertEqual(
            alignment[1],
            "TSPASIRPPAGPSSR---------RPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGW----------RASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE",
        )
        self.assertEqual(
            alignment[2],
            "TSPASIRPPAGPSSRPAMVSSR--RPSPPPPRRPPGRPCCSAAPPRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSR--GSRPPRFAPPLMSSCITSTTGPPPPAGDRSHE",
        )
        self.assertEqual(
            alignment[3],
            "TSPASLRPPAGPSSRPAMVSSRR-RPSPPGPRRPT----CSAAPRRPQATGGYKTCSGTCTTSTSTRHRGRSGYSARTTTAACLRASRKSMRAACSR--GSRPNRFAPTLMSSCLTSTTGPPAYAGDRSHE",
        )
        self.assertEqual(
            str(alignment),
            """\
IXI_234           0 TSPASIRPPAGPSSRPAMVSSRRTRPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTC
IXI_235           0 TSPASIRPPAGPSSR---------RPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTC
IXI_236           0 TSPASIRPPAGPSSRPAMVSSR--RPSPPPPRRPPGRPCCSAAPPRPQATGGWKTCSGTC
IXI_237           0 TSPASLRPPAGPSSRPAMVSSRR-RPSPPGPRRPT----CSAAPRRPQATGGYKTCSGTC

IXI_234          60 TTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTG
IXI_235          51 TTSTSTRHRGRSGW----------RASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTG
IXI_236          58 TTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSR--GSRPPRFAPPLMSSCITSTTG
IXI_237          55 TTSTSTRHRGRSGYSARTTTAACLRASRKSMRAACSR--GSRPNRFAPTLMSSCLTSTTG

IXI_234         120 PPAWAGDRSHE 131
IXI_235         101 PPAWAGDRSHE 112
IXI_236         116 PPPPAGDRSHE 127
IXI_237         113 PPAYAGDRSHE 124
""",
        )
        self.assertTrue(
            np.array_equal(
                alignment.coordinates,
                # fmt: off
                np.array([[0, 15, 22, 23, 24, 35, 39, 74, 84, 97, 99, 131],
                          [0, 15, 15, 15, 15, 26, 30, 65, 65, 78, 80, 112],
                          [0, 15, 22, 22, 22, 33, 37, 72, 82, 95, 95, 127],
                          [0, 15, 22, 23, 23, 34, 34, 69, 79, 92, 92, 124]])
                # fmt: on
            )
        )
        self.assertEqual(
            format(alignment, "phylip"),
            """\
4 131
IXI_234   TSPASIRPPAGPSSRPAMVSSRRTRPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE
IXI_235   TSPASIRPPAGPSSR---------RPSPPGPRRPTGRPCCSAAPRRPQATGGWKTCSGTCTTSTSTRHRGRSGW----------RASRKSMRAACSRSAGSRPNRFAPTLMSSCITSTTGPPAWAGDRSHE
IXI_236   TSPASIRPPAGPSSRPAMVSSR--RPSPPPPRRPPGRPCCSAAPPRPQATGGWKTCSGTCTTSTSTRHRGRSGWSARTTTAACLRASRKSMRAACSR--GSRPPRFAPPLMSSCITSTTGPPPPAGDRSHE
IXI_237   TSPASLRPPAGPSSRPAMVSSRR-RPSPPGPRRPT----CSAAPRRPQATGGYKTCSGTCTTSTSTRHRGRSGYSARTTTAACLRASRKSMRAACSR--GSRPNRFAPTLMSSCLTSTTGPPAYAGDRSHE
""",
        )
        counts = alignment.counts(substitution_matrix)
        self.assertEqual(
            repr(counts),
            "<AlignmentCounts object (substitution score = 3602.0; 702 aligned letters; 667 identities; 35 mismatches; 681 positives; 78 gaps) at 0x%x>"
            % id(counts),
        )
        self.assertEqual(
            str(counts),
            """\
AlignmentCounts object with
    substitution_score = 3602.0,
    aligned = 702:
        identities = 667,
        positives = 681,
        mismatches = 35.
    gaps = 78:
        left_gaps = 0:
            left_insertions = 0:
                open_left_insertions = 0,
                extend_left_insertions = 0;
            left_deletions = 0:
                open_left_deletions = 0,
                extend_left_deletions = 0;
        internal_gaps = 78:
            internal_insertions = 36:
                open_internal_insertions = 5,
                extend_internal_insertions = 31;
            internal_deletions = 42:
                open_internal_deletions = 11,
                extend_internal_deletions = 31;
        right_gaps = 0:
            right_insertions = 0:
                open_right_insertions = 0,
                extend_right_insertions = 0;
            right_deletions = 0:
                open_right_deletions = 0,
                extend_right_deletions = 0.
""",
        )
        self.assertEqual(counts.left_insertions, 0)
        self.assertEqual(counts.left_deletions, 0)
        self.assertEqual(counts.right_insertions, 0)
        self.assertEqual(counts.right_deletions, 0)
        self.assertEqual(counts.internal_insertions, 36)
        self.assertEqual(counts.internal_deletions, 42)
        self.assertEqual(counts.left_gaps, 0)
        self.assertEqual(counts.right_gaps, 0)
        self.assertEqual(counts.internal_gaps, 78)
        self.assertEqual(counts.insertions, 36)
        self.assertEqual(counts.deletions, 42)
        self.assertEqual(counts.gaps, 78)
        self.assertEqual(counts.aligned, 702)
        self.assertEqual(counts.identities, 667)
        self.assertEqual(counts.mismatches, 35)
        self.assertEqual(counts.positives, 681)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
