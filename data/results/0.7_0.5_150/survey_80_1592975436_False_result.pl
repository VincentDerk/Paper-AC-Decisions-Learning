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

utility(\+(s("F")),50).



utility(a("old"),11).
utility(r("small"),50).
utility(\+(r("small")),20).

utility(e("high"),15).


utility(t("train"),-9).



utility(e("uni"),-2).

utility(o("self"),-29).

utility(\+(o("emp")),6).
body_123(122,multi) :- body_1(0,multi).
body_141(140,multi) :- body_20(19,multi).
body_154(153,multi) :- body_36(33,multi).
body_167(166,multi) :- body_52(49,multi).
body_180(179,multi) :- body_67(64,multi).
body_193(192,multi) :- body_82(79,multi).
body_206(205,multi) :- body_97(94,multi).
body_219(218,multi) :- body_112(109,multi).
body_232(231,multi) :- body_125(124,multi).
body_245(244,multi) :- body_139(138,multi).
body_258(257,multi) :- body_152(151,multi).
body_271(270,multi) :- body_166(165,multi).
body_284(283,multi) :- body_181(178,multi).
body_303(302,multi) :- body_202(199,multi).
body_321(320,multi) :- body_222(219,multi).
body_339(338,multi) :- body_242(239,multi).
utility(s("F"),20.930827249136676).
utility(a("adult"),21.089136916452773).
utility(t("other"),38.96284473828756).
utility(\+(t("other")),-45.32497139022846).
utility(s("M"),-27.29295390107757).
utility(r("big"),-28.367836769498535).
utility(\+(r("big")),22.005710117557673).
utility(\+(t("train")),40.38509905981959).
utility(t("car"),1.42225432153198).
utility(\+(t("car")),-7.784380973472871).
utility(\+(e("uni")),-21.91306322704477).
utility(\+(o("self")),-28.19567720389607).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_123(122,multi).
0.6::s("M"); 0.4::s("F") :- body_141(140,multi).
0.75::e("high"); 0.25::e("uni") :- body_154(153,multi).
0.64::e("high"); 0.36::e("uni") :- body_167(166,multi).
0.72::e("high"); 0.28::e("uni") :- body_180(179,multi).
0.7::e("high"); 0.3::e("uni") :- body_193(192,multi).
0.88::e("high"); 0.12::e("uni") :- body_206(205,multi).
0.9::e("high"); 0.1::e("uni") :- body_219(218,multi).
0.96::o("emp"); 0.04::o("self") :- body_232(231,multi).
0.92::o("emp"); 0.08::o("self") :- body_245(244,multi).
0.25::r("small"); 0.75::r("big") :- body_258(257,multi).
0.2::r("small"); 0.8::r("big") :- body_271(270,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_284(283,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_303(302,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_321(320,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_339(338,multi).
