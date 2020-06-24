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
query(r("big")).
query(t("other")).
query(a("adult")).
query(o("self")).
query(t("train")).
query(e("high")).
query(a("old")).
query(s("F")).
query(o("emp")).
query(r("small")).
query(s("M")).
query(t("car")).
query(a("young")).
query(e("uni")).



utility(a("adult"),32).

utility(\+(o("self")),26).
utility(e("high"),-18).
utility(\+(e("high")),-3).
utility(a("old"),6).

utility(s("F"),-46).
utility(o("emp"),-48).
utility(r("small"),19).

utility(a("young"),-32).
utility(e("uni"),-40).
utility(\+(e("uni")),-44).
body_113(112,multi) :- body_1(0,multi).
body_131(130,multi) :- body_36(33,multi).
body_144(143,multi) :- body_166(165,multi).
body_157(156,multi) :- body_202(199,multi).
body_176(175,multi) :- body_67(64,multi).
body_189(188,multi) :- body_139(138,multi).
body_202(201,multi) :- body_242(239,multi).
body_219(218,multi) :- body_112(109,multi).
body_232(231,multi) :- body_82(79,multi).
body_245(244,multi) :- body_52(49,multi).
body_258(257,multi) :- body_181(178,multi).
body_276(275,multi) :- body_20(19,multi).
body_289(288,multi) :- body_152(151,multi).
body_302(301,multi) :- body_222(219,multi).
body_320(319,multi) :- body_125(124,multi).
body_333(332,multi) :- body_97(94,multi).
utility(r("big"),30.76098187414424).
utility(t("other"),2.903139801306861).
utility(\+(r("big")),-2.47853115022711).
utility(\+(a("old")),29.80047441101443).
utility(\+(a("adult")),29.969713818942516).
utility(t("car"),-38.63813125273928).
0.25::r("small"); 0.75::r("big") :- body_289(288,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_258(257,multi).
0.75::e("high"); 0.25::e("uni") :- body_131(130,multi).
0.7::e("high"); 0.3::e("uni") :- body_232(231,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_202(201,multi).
0.88::e("high"); 0.12::e("uni") :- body_333(332,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_302(301,multi).
0.2::r("small"); 0.8::r("big") :- body_144(143,multi).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_113(112,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_157(156,multi).
0.6::s("M"); 0.4::s("F") :- body_276(275,multi).
0.64::e("high"); 0.36::e("uni") :- body_245(244,multi).
0.9::e("high"); 0.1::e("uni") :- body_219(218,multi).
0.72::e("high"); 0.28::e("uni") :- body_176(175,multi).
0.92::o("emp"); 0.08::o("self") :- body_189(188,multi).
0.96::o("emp"); 0.04::o("self") :- body_320(319,multi).
