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
query(o("self")).
query(a("young")).
query(t("car")).
query(a("adult")).
query(t("other")).
query(r("small")).
query(o("emp")).
query(e("high")).
query(t("train")).
query(e("uni")).
query(a("old")).
query(s("F")).
query(s("M")).
query(r("big")).


utility(\+(a("young")),-20).
utility(t("car"),26).
utility(\+(t("car")),-13).
utility(a("adult"),-47).

utility(\+(t("other")),-44).


utility(o("emp"),22).
utility(e("high"),48).

utility(\+(t("train")),-33).


utility(s("F"),-42).
utility(\+(s("F")),-13).



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
utility(o("self"),-0.663191876585163).
utility(e("uni"),35.101548054995035).
utility(\+(o("self")),-7.601260322086909).
utility(a("old"),-38.022006499233896).
utility(\+(r("small")),3.203868418000815).
utility(t("train"),35.85895730462475).
utility(s("M"),-18.344508472989848).
utility(\+(r("big")),-6.9489645287523).
utility(t("other"),-29.106645110349902).
utility(r("small"),-11.468320616672887).
utility(r("big"),-1.315487669919774).
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
