body_1(0,multi) :- true.
body_20(19,multi) :- true.
body_36(33,multi) :- a("young"), s("M").
body_52(49,multi) :- a("young"), s("F").
body_67(64,multi) :- a("adult"), s("M").
body_82(79,multi) :- a("adult"), s("F").
body_97(94,multi) :- a("old"), s("M").
body_112(109,multi) :- a("old"), s("F").
body_125(124,multi) :- e("high").
body_139(138,multi) :- e("uni").
body_152(151,multi) :- e("high").
body_166(165,multi) :- e("uni").
body_181(178,multi) :- o("emp"), r("small").
body_202(199,multi) :- o("emp"), r("big").
body_222(219,multi) :- o("self"), r("small").
body_242(239,multi) :- o("self"), r("big").
query(t("train")).
query(r("big")).
query(o("emp")).
query(o("self")).
query(s("M")).
query(t("other")).
query(r("small")).
query(a("old")).
query(e("uni")).
query(a("adult")).
query(e("high")).
query(s("F")).
query(a("young")).
query(t("car")).

utility(\+(t("train")),50).



utility(s("M"),11).
utility(t("other"),50).
utility(\+(t("other")),20).

utility(a("old"),15).


utility(a("adult"),-9).



utility(s("F"),-2).

utility(a("young"),-29).

utility(\+(t("car")),6).
body_123(122,multi) :- body_1(0,multi).
body_141(140,multi) :- body_36(33,multi).
body_154(153,multi) :- body_166(165,multi).
body_167(166,multi) :- body_202(199,multi).
body_186(185,multi) :- body_67(64,multi).
body_199(198,multi) :- body_139(138,multi).
body_212(211,multi) :- body_242(239,multi).
body_230(229,multi) :- body_112(109,multi).
body_243(242,multi) :- body_82(79,multi).
body_256(255,multi) :- body_52(49,multi).
body_269(268,multi) :- body_181(178,multi).
body_287(286,multi) :- body_20(19,multi).
body_300(299,multi) :- body_152(151,multi).
body_313(312,multi) :- body_222(219,multi).
body_331(330,multi) :- body_125(124,multi).
body_344(343,multi) :- body_97(94,multi).
utility(t("train"),21.099193678051943).
utility(\+(a("young")),-38.12852824922402).
utility(r("big"),36.919810268678724).
utility(o("emp"),33.30253429031084).
utility(\+(e("high")),-15.427900782333658).
utility(r("small"),-19.709464095529043).
utility(e("uni"),-15.427900782333658).
utility(e("high"),32.63824695548336).
utility(\+(a("adult")),48.90882618150714).
utility(\+(o("emp")),-16.09218811716114).
utility(\+(s("F")),-18.794380928728536).
utility(\+(e("uni")),32.63824695548336).
0.88::e("high"); 0.12::e("uni") :- body_344(343,multi).
0.9::e("high"); 0.1::e("uni") :- body_230(229,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_167(166,multi).
0.92::o("emp"); 0.08::o("self") :- body_199(198,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_269(268,multi).
0.96::o("emp"); 0.04::o("self") :- body_331(330,multi).
0.25::r("small"); 0.75::r("big") :- body_300(299,multi).
0.75::e("high"); 0.25::e("uni") :- body_141(140,multi).
0.7::e("high"); 0.3::e("uni") :- body_243(242,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_212(211,multi).
0.2::r("small"); 0.8::r("big") :- body_154(153,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_313(312,multi).
0.72::e("high"); 0.28::e("uni") :- body_186(185,multi).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_123(122,multi).
0.6::s("M"); 0.4::s("F") :- body_287(286,multi).
0.64::e("high"); 0.36::e("uni") :- body_256(255,multi).
