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
query(either).
query(dysp).
query(lung).
query(xray).
query(tub).
query(smoke).
query(asia).
query(bronc).
utility(either,0).
utility(\+(either),49).
utility(xray,-37).
utility(tub,-46).
utility(smoke,22).
utility(\+(smoke),5).
utility(asia,21).
utility(\+(asia),-45).
utility(bronc,27).
utility(\+(bronc),15).
0.1::lung :- body_5(4,lung).
0.01::lung :- body_15(13,lung).
0.05::tub :- body_23(22,tub).
0.01::tub :- body_33(31,tub).
0.6::bronc :- body_41(40,bronc).
0.3::bronc :- body_51(49,bronc).
0.0::either :- body_78(73,either).
0.98::xray :- body_86(85,xray).
0.05::xray :- body_96(94,xray).
0.9::dysp :- body_106(103,dysp).
0.8::dysp :- body_118(114,dysp).
0.7::dysp :- body_129(125,dysp).
0.1::dysp :- body_141(136,dysp).
