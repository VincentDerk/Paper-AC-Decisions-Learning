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
query(t("other")).
query(s("F")).
query(o("emp")).
query(t("car")).
query(a("adult")).
query(e("high")).
query(r("small")).
query(t("train")).
query(a("young")).
query(s("M")).
query(r("big")).
query(e("uni")).
query(o("self")).

utility(\+(a("old")),38).

utility(o("emp"),-19).



utility(r("small"),-27).


utility(s("M"),-50).
utility(r("big"),49).
utility(\+(r("big")),-29).
utility(\+(e("uni")),-25).

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
utility(a("young"),-9.045763158775554).
utility(o("self"),40.017182953569844).
utility(a("old"),-14.370411319295538).
utility(\+(t("car")),0.249009907629781).
utility(\+(s("F")),33.42802364233007).
utility(t("train"),-7.959346323746481).
utility(e("high"),-44.31557194463744).
utility(\+(a("adult")),-29.416174478071138).
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
