0.01::asia.
0.5::smoke.
body_5(4,lung) :- smoke.
body_15(13,lung) :- \+smoke.
body_23(22,tub) :- asia.
body_33(31,tub) :- \+asia.
body_41(40,bronc) :- smoke.
body_51(49,bronc) :- \+smoke.
either :- lung, tub.
either :- lung, \+tub.
either :- \+lung, tub.
body_78(73,either) :- \+lung, \+tub.
body_86(85,xray) :- either.
body_96(94,xray) :- \+either.
body_106(103,dysp) :- bronc, either.
body_118(114,dysp) :- bronc, \+either.
body_129(125,dysp) :- \+bronc, either.
body_141(136,dysp) :- \+bronc, \+either.
query(xray).
query(smoke).
query(dysp).
query(bronc).
query(tub).
query(either).
query(asia).
query(lung).
utility(xray,43).



utility(\+(dysp),16).
utility(\+(bronc),26).


utility(asia,6).
utility(\+(asia),22).

body_109(108,lung) :- body_5(4,lung).
body_117(116,lung) :- body_15(13,lung).
body_125(124,tub) :- body_23(22,tub).
body_133(132,tub) :- body_33(31,tub).
body_141(140,bronc) :- body_41(40,bronc).
body_148(147,bronc) :- body_51(49,bronc).
body_156(155,either) :- body_78(73,either).
body_164(163,xray) :- body_86(85,xray).
body_173(172,xray) :- body_96(94,xray).
body_181(180,dysp) :- body_106(103,dysp).
body_190(189,dysp) :- body_118(114,dysp).
body_198(197,dysp) :- body_129(125,dysp).
body_206(205,dysp) :- body_141(136,dysp).
utility(\+(xray),13.81343680960047).
utility(smoke,17.987872397639766).
utility(dysp,30.460573636292526).
utility(either,-66.67939322009921).
utility(\+(either),-4.828750179667736).
utility(lung,3.320679298648416).
0.1::lung :- body_109(108,lung).
0.01::lung :- body_117(116,lung).
0.05::tub :- body_125(124,tub).
0.01::tub :- body_133(132,tub).
0.6::bronc :- body_141(140,bronc).
0.3::bronc :- body_148(147,bronc).
0.0::either :- body_156(155,either).
0.98::xray :- body_164(163,xray).
0.05::xray :- body_173(172,xray).
0.9::dysp :- body_181(180,dysp).
0.8::dysp :- body_190(189,dysp).
0.7::dysp :- body_198(197,dysp).
0.1::dysp :- body_206(205,dysp).