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
query(a("old")).
query(t("car")).
query(r("small")).
query(a("young")).
query(r("big")).
query(a("adult")).
query(o("self")).
query(s("M")).
query(e("high")).
query(s("F")).
query(e("uni")).
query(o("emp")).
query(t("other")).
query(t("train")).

utility(\+(a("old")),50).



utility(r("big"),11).
utility(a("adult"),50).
utility(\+(a("adult")),20).

utility(s("M"),15).


utility(s("F"),-9).



utility(o("emp"),-2).

utility(t("other"),-29).

utility(\+(t("train")),6).
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
utility(\+(o("emp")),-4.231391965700712).
utility(a("old"),10.8351787551905).
utility(r("small"),32.075843514473426).
utility(\+(s("F")),30.16935644029354).
utility(\+(r("small")),-29.406241111487326).
utility(\+(t("other")),-0.638645641570189).
utility(t("car"),8.595421096361289).
utility(\+(e("high")),24.09724996442527).
utility(o("self"),-4.231391965700712).
utility(e("high"),-21.427647561439162).
utility(e("uni"),24.09724996442527).
utility(\+(e("uni")),-21.427647561439162).
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
