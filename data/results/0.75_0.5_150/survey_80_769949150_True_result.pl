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
query(o("emp")).
query(e("high")).
query(o("self")).
query(t("car")).
query(s("F")).
query(a("young")).
query(a("old")).
query(r("small")).
query(t("train")).
query(t("other")).
query(a("adult")).
query(e("uni")).
query(s("M")).
query(r("big")).

utility(e("high"),17).
utility(\+(o("self")),48).

utility(\+(s("F")),36).

utility(\+(a("young")),3).

utility(r("small"),-8).
utility(\+(r("small")),29).

utility(\+(t("train")),-37).
utility(t("other"),-23).

utility(\+(a("adult")),-9).


utility(s("M"),-8).

body_118(117,multi) :- body_1(0,multi).
body_136(135,multi) :- body_36(33,multi).
body_149(148,multi) :- body_166(165,multi).
body_162(161,multi) :- body_202(199,multi).
body_181(180,multi) :- body_67(64,multi).
body_193(192,multi) :- body_139(138,multi).
body_206(205,multi) :- body_242(239,multi).
body_224(223,multi) :- body_112(109,multi).
body_237(236,multi) :- body_82(79,multi).
body_250(249,multi) :- body_52(49,multi).
body_263(262,multi) :- body_181(178,multi).
body_281(280,multi) :- body_20(19,multi).
body_294(293,multi) :- body_152(151,multi).
body_307(306,multi) :- body_222(219,multi).
body_325(324,multi) :- body_125(124,multi).
body_338(337,multi) :- body_97(94,multi).
utility(a("adult"),3.206764085989709).
utility(s("F"),-42.95888594944439).
utility(e("uni"),-0.578258907704133).
utility(a("young"),-28.711522792540745).
utility(a("old"),-20.781541214029914).
utility(\+(o("emp")),-48.595199030601016).
utility(t("train"),6.544343918465582).
utility(\+(e("uni")),46.29195898712322).
utility(r("big"),-18.34268660353519).
0.92::o("emp"); 0.08::o("self") :- body_193(192,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_162(161,multi).
0.96::o("emp"); 0.04::o("self") :- body_325(324,multi).
0.25::r("small"); 0.75::r("big") :- body_294(293,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_263(262,multi).
0.75::e("high"); 0.25::e("uni") :- body_136(135,multi).
0.7::e("high"); 0.3::e("uni") :- body_237(236,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_206(205,multi).
0.88::e("high"); 0.12::e("uni") :- body_338(337,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_307(306,multi).
0.72::e("high"); 0.28::e("uni") :- body_181(180,multi).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_118(117,multi).
0.64::e("high"); 0.36::e("uni") :- body_250(249,multi).
0.6::s("M"); 0.4::s("F") :- body_281(280,multi).
0.2::r("small"); 0.8::r("big") :- body_149(148,multi).
0.9::e("high"); 0.1::e("uni") :- body_224(223,multi).
