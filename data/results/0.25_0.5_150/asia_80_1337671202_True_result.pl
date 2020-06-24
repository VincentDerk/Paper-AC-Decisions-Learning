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
query(bronc).
query(tub).
query(either).
query(lung).
query(asia).
query(smoke).
query(xray).
query(dysp).
utility(bronc,0).
utility(\+(bronc),49).
utility(lung,-37).
utility(asia,-46).
utility(smoke,22).



utility(dysp,27).
utility(\+(dysp),15).
body_105(104,lung) :- body_5(4,lung).
body_113(112,lung) :- body_15(13,lung).
body_121(120,tub) :- body_23(22,tub).
body_129(128,tub) :- body_33(31,tub).
body_136(135,bronc) :- body_41(40,bronc).
body_144(143,bronc) :- body_51(49,bronc).
body_152(151,either) :- body_78(73,either).
body_160(159,xray) :- body_86(85,xray).
body_169(168,xray) :- body_96(94,xray).
body_177(176,dysp) :- body_106(103,dysp).
body_186(185,dysp) :- body_118(114,dysp).
body_194(193,dysp) :- body_129(125,dysp).
body_202(201,dysp) :- body_141(136,dysp).
utility(\+(smoke),3.564532776761376).
utility(xray,23.56411227543317).
utility(\+(xray),-44.087123702763506).
0.1::lung :- body_105(104,lung).
0.01::lung :- body_113(112,lung).
0.05::tub :- body_121(120,tub).
0.01::tub :- body_129(128,tub).
0.6::bronc :- body_136(135,bronc).
0.3::bronc :- body_144(143,bronc).
0.0::either :- body_152(151,either).
0.98::xray :- body_160(159,xray).
0.05::xray :- body_169(168,xray).
0.9::dysp :- body_177(176,dysp).
0.8::dysp :- body_186(185,dysp).
0.7::dysp :- body_194(193,dysp).
0.1::dysp :- body_202(201,dysp).
