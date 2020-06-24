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
query(e("uni")).
query(e("high")).
query(t("car")).
query(t("train")).
query(s("F")).
query(o("self")).
query(r("small")).
query(r("big")).
query(o("emp")).
query(t("other")).
query(a("old")).
query(s("M")).
query(a("adult")).
query(a("young")).
utility(e("uni"),t(V_0)) :- true.
utility(\+(e("uni")),t(V_0)) :- true.
utility(e("high"),t(V_0)) :- true.
utility(t("car"),32).
utility(\+(t("car")),t(V_0)) :- true.
utility(\+(t("train")),26).
utility(o("self"),-18).
utility(\+(o("self")),-3).
utility(r("small"),6).
utility(\+(r("small")),t(V_0)) :- true.
utility(r("big"),-46).
utility(o("emp"),-48).
utility(t("other"),19).
utility(s("M"),t(V_0)) :- true.
utility(a("adult"),-32).
utility(a("young"),-40).
utility(\+(a("young")),-44).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_1(0,multi).
0.6::s("M"); 0.4::s("F") :- body_20(19,multi).
0.75::e("high"); 0.25::e("uni") :- body_36(33,multi).
0.64::e("high"); 0.36::e("uni") :- body_52(49,multi).
0.72::e("high"); 0.28::e("uni") :- body_67(64,multi).
0.7::e("high"); 0.3::e("uni") :- body_82(79,multi).
0.88::e("high"); 0.12::e("uni") :- body_97(94,multi).
0.9::e("high"); 0.1::e("uni") :- body_112(109,multi).
0.96::o("emp"); 0.04::o("self") :- body_125(124,multi).
0.92::o("emp"); 0.08::o("self") :- body_139(138,multi).
0.25::r("small"); 0.75::r("big") :- body_152(151,multi).
0.2::r("small"); 0.8::r("big") :- body_166(165,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_181(178,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_202(199,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_222(219,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_242(239,multi).
