%% ProbLog program: PGM 1
%% Created on 2019-11-05 14:00:20.215720

0.3::a("young"); 0.5::a("adult"); 0.2::a("old").
0.6::s("M"); 0.4::s("F").
0.75::e("high"); 0.25::e("uni") :- a("young"), s("M").
0.64::e("high"); 0.36::e("uni") :- a("young"), s("F").
0.72::e("high"); 0.28::e("uni") :- a("adult"), s("M").
0.7::e("high"); 0.3::e("uni") :- a("adult"), s("F").
0.88::e("high"); 0.12::e("uni") :- a("old"), s("M").
0.9::e("high"); 0.1::e("uni") :- a("old"), s("F").
0.96::o("emp"); 0.04::o("self") :- e("high").
0.92::o("emp"); 0.08::o("self") :- e("uni").
0.25::r("small"); 0.75::r("big") :- e("high").
0.2::r("small"); 0.8::r("big") :- e("uni").
0.48::t("car"); 0.42::t("train"); 0.1::t("other") :- o("emp"), r("small").
0.58::t("car"); 0.24::t("train"); 0.18::t("other") :- o("emp"), r("big").
0.56::t("car"); 0.36::t("train"); 0.08::t("other") :- o("self"), r("small").
0.7::t("car"); 0.21::t("train"); 0.09::t("other") :- o("self"), r("big").