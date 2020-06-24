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
query(t("car")).
query(a("young")).
query(o("emp")).
query(e("high")).
query(s("M")).
query(r("small")).
query(r("big")).
query(t("train")).
query(o("self")).
query(e("uni")).
query(s("F")).
query(a("old")).
query(t("other")).
query(a("adult")).


utility(\+(a("young")),-20).
utility(o("emp"),26).
utility(\+(o("emp")),-13).
utility(e("high"),-47).

utility(\+(s("M")),-44).


utility(r("big"),22).
utility(t("train"),48).

utility(\+(o("self")),-33).


utility(a("old"),-42).
utility(\+(a("old")),-13).



body_122(121,multi) :- body_1(0,multi).
body_140(139,multi) :- body_36(33,multi).
body_153(152,multi) :- body_166(165,multi).
body_166(165,multi) :- body_202(199,multi).
body_184(183,multi) :- body_67(64,multi).
body_197(196,multi) :- body_139(138,multi).
body_210(209,multi) :- body_242(239,multi).
body_228(227,multi) :- body_112(109,multi).
body_241(240,multi) :- body_82(79,multi).
body_254(253,multi) :- body_52(49,multi).
body_267(266,multi) :- body_181(178,multi).
body_285(284,multi) :- body_20(19,multi).
body_298(297,multi) :- body_152(151,multi).
body_311(310,multi) :- body_222(219,multi).
body_329(328,multi) :- body_125(124,multi).
body_342(341,multi) :- body_97(94,multi).
utility(t("car"),-6.483721144963527).
utility(\+(a("adult")),-4.316554510937396).
utility(e("uni"),48.46870897164501).
utility(o("self"),54.03679930997704).
utility(\+(r("small")),-0.05469083703517).
utility(a("adult"),-16.314694654263807).
utility(s("M"),0.166796332120321).
utility(s("F"),-20.7980454973216).
utility(\+(t("car")),-14.147528020237708).
utility(r("small"),-20.576558328166037).
utility(t("other"),-23.051085718948833).
0.9::e("high"); 0.1::e("uni") :- body_228(227,multi).
0.92::o("emp"); 0.08::o("self") :- body_197(196,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_166(165,multi).
0.96::o("emp"); 0.04::o("self") :- body_329(328,multi).
0.25::r("small"); 0.75::r("big") :- body_298(297,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_267(266,multi).
0.75::e("high"); 0.25::e("uni") :- body_140(139,multi).
0.7::e("high"); 0.3::e("uni") :- body_241(240,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_210(209,multi).
0.88::e("high"); 0.12::e("uni") :- body_342(341,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_311(310,multi).
0.72::e("high"); 0.28::e("uni") :- body_184(183,multi).
0.2::r("small"); 0.8::r("big") :- body_153(152,multi).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_122(121,multi).
0.6::s("M"); 0.4::s("F") :- body_285(284,multi).
0.64::e("high"); 0.36::e("uni") :- body_254(253,multi).
