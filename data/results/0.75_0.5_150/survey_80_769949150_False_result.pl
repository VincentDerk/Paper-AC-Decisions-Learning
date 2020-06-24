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
query(t("train")).
query(a("adult")).
query(o("emp")).
query(s("M")).
query(e("uni")).
query(e("high")).
query(r("big")).
query(a("young")).
query(t("other")).
query(r("small")).
query(t("car")).
query(a("old")).
query(s("F")).

utility(t("train"),17).
utility(\+(a("adult")),48).

utility(\+(s("M")),36).

utility(\+(e("uni")),3).

utility(r("big"),-8).
utility(\+(r("big")),29).

utility(\+(a("young")),-37).
utility(t("other"),-23).

utility(\+(r("small")),-9).


utility(a("old"),-8).

body_118(117,multi) :- body_1(0,multi).
body_136(135,multi) :- body_20(19,multi).
body_149(148,multi) :- body_36(33,multi).
body_162(161,multi) :- body_52(49,multi).
body_175(174,multi) :- body_67(64,multi).
body_188(187,multi) :- body_82(79,multi).
body_201(200,multi) :- body_97(94,multi).
body_214(213,multi) :- body_112(109,multi).
body_227(226,multi) :- body_125(124,multi).
body_240(239,multi) :- body_139(138,multi).
body_253(252,multi) :- body_152(151,multi).
body_266(265,multi) :- body_166(165,multi).
body_279(278,multi) :- body_181(178,multi).
body_298(297,multi) :- body_202(199,multi).
body_316(315,multi) :- body_222(219,multi).
body_334(333,multi) :- body_242(239,multi).
utility(\+(o("self")),-32.229622229354966).
utility(s("M"),-34.23658821480996).
utility(e("uni"),-34.93911177387458).
utility(e("high"),-1.553913057915777).
utility(a("young"),37.87379819026993).
utility(r("small"),0.356454408238793).
utility(t("car"),-67.16207618793777).
utility(\+(t("car")),30.669051356147442).
utility(s("F"),-2.25643661698031).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_118(117,multi).
0.6::s("M"); 0.4::s("F") :- body_136(135,multi).
0.75::e("high"); 0.25::e("uni") :- body_149(148,multi).
0.64::e("high"); 0.36::e("uni") :- body_162(161,multi).
0.72::e("high"); 0.28::e("uni") :- body_175(174,multi).
0.7::e("high"); 0.3::e("uni") :- body_188(187,multi).
0.88::e("high"); 0.12::e("uni") :- body_201(200,multi).
0.9::e("high"); 0.1::e("uni") :- body_214(213,multi).
0.96::o("emp"); 0.04::o("self") :- body_227(226,multi).
0.92::o("emp"); 0.08::o("self") :- body_240(239,multi).
0.25::r("small"); 0.75::r("big") :- body_253(252,multi).
0.2::r("small"); 0.8::r("big") :- body_266(265,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_279(278,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_298(297,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_316(315,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_334(333,multi).
