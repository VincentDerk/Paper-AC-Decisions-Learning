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
query(s("F")).
query(a("adult")).
query(t("other")).
query(a("young")).
query(t("car")).
query(e("high")).
query(o("emp")).
query(s("M")).
query(o("self")).
query(t("train")).
query(r("big")).
query(e("uni")).
query(r("small")).

utility(\+(a("old")),50).



utility(a("young"),11).
utility(t("car"),50).
utility(\+(t("car")),20).

utility(o("emp"),15).


utility(o("self"),-9).



utility(r("big"),-2).

utility(e("uni"),-29).

utility(\+(r("small")),6).
body_123(122,multi) :- body_1(0,multi).
body_141(140,multi) :- body_36(33,multi).
body_154(153,multi) :- body_166(165,multi).
body_167(166,multi) :- body_202(199,multi).
body_186(185,multi) :- body_67(64,multi).
body_199(198,multi) :- body_139(138,multi).
body_212(211,multi) :- body_242(239,multi).
body_230(229,multi) :- body_112(109,multi).
body_243(242,multi) :- body_82(79,multi).
body_256(255,multi) :- body_52(49,multi).
body_269(268,multi) :- body_181(178,multi).
body_287(286,multi) :- body_20(19,multi).
body_300(299,multi) :- body_152(151,multi).
body_313(312,multi) :- body_222(219,multi).
body_331(330,multi) :- body_125(124,multi).
body_344(343,multi) :- body_97(94,multi).
utility(a("old"),21.72139597378652).
utility(a("adult"),55.909626388865675).
utility(\+(r("big")),-14.921004224023784).
utility(s("F"),12.19055847072578).
utility(\+(e("uni")),-33.16368260702124).
utility(e("high"),-13.163682607021235).
utility(\+(o("self")),13.994465846366994).
utility(s("M"),-62.24366752005263).
utility(t("train"),26.777587610909784).
utility(\+(a("adult")),-28.962735438192524).
utility(\+(s("M")),20.190558470725772).
utility(\+(t("train")),24.169303339763367).
0.88::e("high"); 0.12::e("uni") :- body_344(343,multi).
0.9::e("high"); 0.1::e("uni") :- body_230(229,multi).
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- body_167(166,multi).
0.92::o("emp"); 0.08::o("self") :- body_199(198,multi).
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- body_269(268,multi).
0.96::o("emp"); 0.04::o("self") :- body_331(330,multi).
0.25::r("small"); 0.75::r("big") :- body_300(299,multi).
0.75::e("high"); 0.25::e("uni") :- body_141(140,multi).
0.7::e("high"); 0.3::e("uni") :- body_243(242,multi).
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- body_212(211,multi).
0.2::r("small"); 0.8::r("big") :- body_154(153,multi).
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- body_313(312,multi).
0.72::e("high"); 0.28::e("uni") :- body_186(185,multi).
0.3::a("young"); 0.5::a("adult"); 0.2::a("old") :- body_123(122,multi).
0.6::s("M"); 0.4::s("F") :- body_287(286,multi).
0.64::e("high"); 0.36::e("uni") :- body_256(255,multi).
