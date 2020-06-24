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
query(s("F")).
query(e("uni")).
query(t("train")).
query(r("small")).
query(a("young")).
query(e("high")).
query(s("M")).
query(o("emp")).
query(t("other")).
query(r("big")).
query(o("self")).
query(a("old")).
query(a("adult")).
query(t("car")).



utility(t("train"),32).

utility(\+(r("small")),26).
utility(e("high"),-18).
utility(\+(e("high")),-3).
utility(s("M"),6).

utility(o("emp"),-46).
utility(t("other"),-48).
utility(r("big"),19).

utility(a("adult"),-32).
utility(t("car"),-40).
utility(\+(t("car")),-44).
body_113(112,multi) :- body_1(0,multi).
body_131(130,multi) :- body_20(19,multi).
body_144(143,multi) :- body_36(33,multi).
body_157(156,multi) :- body_52(49,multi).
body_170(169,multi) :- body_67(64,multi).
body_183(182,multi) :- body_82(79,multi).
body_196(195,multi) :- body_97(94,multi).
body_209(208,multi) :- body_112(109,multi).
body_222(221,multi) :- body_125(124,multi).
body_234(233,multi) :- body_139(138,multi).
body_247(246,multi) :- body_152(151,multi).
body_260(259,multi) :- body_166(165,multi).
body_273(272,multi) :- body_181(178,multi).
body_292(291,multi) :- body_202(199,multi).
body_310(309,multi) :- body_222(219,multi).
body_328(327,multi) :- body_242(239,multi).
utility(s("F"),32.70323655768561).
utility(\+(s("F")),14.01719826780858).
utility(e("uni"),12.085926762700836).
utility(\+(t("train")),12.510974384091408).
utility(\+(s("M")),32.70323655768561).
utility(a("old"),-34.76852534067876).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_113(112,multi).
0.6::s("M"); 0.4::s("F") :- body_131(130,multi).
0.75::e("high"); 0.25::e("uni") :- body_144(143,multi).
0.64::e("high"); 0.36::e("uni") :- body_157(156,multi).
0.72::e("high"); 0.28::e("uni") :- body_170(169,multi).
0.7::e("high"); 0.3::e("uni") :- body_183(182,multi).
0.88::e("high"); 0.12::e("uni") :- body_196(195,multi).
0.9::e("high"); 0.1::e("uni") :- body_209(208,multi).
0.96::o("emp"); 0.04::o("self") :- body_222(221,multi).
0.92::o("emp"); 0.08::o("self") :- body_234(233,multi).
0.25::r("small"); 0.75::r("big") :- body_247(246,multi).
0.2::r("small"); 0.8::r("big") :- body_260(259,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_273(272,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_292(291,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_310(309,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_328(327,multi).
