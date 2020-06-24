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
query(a("adult")).
query(t("other")).
query(a("young")).
query(a("old")).
query(r("small")).
query(s("M")).
query(e("high")).
query(r("big")).
query(t("train")).
query(t("car")).
query(e("uni")).
query(o("self")).
query(o("emp")).


utility(\+(a("adult")),-20).
utility(t("other"),26).
utility(\+(t("other")),-13).
utility(a("young"),-47).

utility(\+(a("old")),-44).


utility(s("M"),22).
utility(e("high"),48).

utility(\+(r("big")),-33).


utility(e("uni"),-42).
utility(\+(e("uni")),-13).



body_122(121,multi) :- body_1(0,multi).
body_140(139,multi) :- body_20(19,multi).
body_153(152,multi) :- body_36(33,multi).
body_166(165,multi) :- body_52(49,multi).
body_178(177,multi) :- body_67(64,multi).
body_191(190,multi) :- body_82(79,multi).
body_204(203,multi) :- body_97(94,multi).
body_217(216,multi) :- body_112(109,multi).
body_230(229,multi) :- body_125(124,multi).
body_243(242,multi) :- body_139(138,multi).
body_256(255,multi) :- body_152(151,multi).
body_269(268,multi) :- body_166(165,multi).
body_282(281,multi) :- body_181(178,multi).
body_301(300,multi) :- body_202(199,multi).
body_319(318,multi) :- body_222(219,multi).
body_337(336,multi) :- body_242(239,multi).
utility(s("F"),11.959091914995225).
utility(\+(s("F")),-19.981613920551688).
utility(a("old"),-45.44183535689017).
utility(r("small"),-31.355251449694272).
utility(\+(r("small")),23.33272944413787).
utility(r("big"),29.087256042008164).
utility(t("train"),28.356379117302335).
utility(t("car"),-40.178933266801735).
utility(o("self"),5.419166017699523).
utility(o("emp"),-1.032032510558955).
utility(\+(o("emp")),-6.990489494997538).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_122(121,multi).
0.6::s("M"); 0.4::s("F") :- body_140(139,multi).
0.75::e("high"); 0.25::e("uni") :- body_153(152,multi).
0.64::e("high"); 0.36::e("uni") :- body_166(165,multi).
0.72::e("high"); 0.28::e("uni") :- body_178(177,multi).
0.7::e("high"); 0.3::e("uni") :- body_191(190,multi).
0.88::e("high"); 0.12::e("uni") :- body_204(203,multi).
0.9::e("high"); 0.1::e("uni") :- body_217(216,multi).
0.96::o("emp"); 0.04::o("self") :- body_230(229,multi).
0.92::o("emp"); 0.08::o("self") :- body_243(242,multi).
0.25::r("small"); 0.75::r("big") :- body_256(255,multi).
0.2::r("small"); 0.8::r("big") :- body_269(268,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_282(281,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_301(300,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_319(318,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_337(336,multi).
