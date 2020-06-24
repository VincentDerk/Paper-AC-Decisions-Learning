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
query(e("high")).
query(o("self")).
query(a("old")).
query(r("big")).
query(t("other")).
query(t("car")).
query(r("small")).
query(s("F")).
query(s("M")).
query(e("uni")).
query(a("young")).
query(a("adult")).
query(o("emp")).


utility(\+(e("high")),-20).
utility(o("self"),26).
utility(\+(o("self")),-13).
utility(a("old"),-47).

utility(\+(r("big")),-44).


utility(t("car"),22).
utility(r("small"),48).

utility(\+(s("F")),-33).


utility(a("young"),-42).
utility(\+(a("young")),-13).



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
utility(t("train"),11.74457813010907).
utility(\+(t("train")),0.641604374122804).
utility(r("big"),-17.07613562149501).
utility(t("other"),-5.902878812833701).
utility(\+(t("other")),18.289061317065546).
utility(s("F"),9.134871813940345).
utility(s("M"),3.25131069029154).
utility(e("uni"),-37.73621941049378).
utility(a("adult"),-34.125306759055626).
utility(o("emp"),8.420348270783995).
utility(\+(o("emp")),3.965834233447902).
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
