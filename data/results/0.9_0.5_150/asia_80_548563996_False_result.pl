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
utility(either,17).
utility(\+(either),3).



utility(xray,-47).



utility(\+(smoke),-18).


body_112(111,lung) :- body_5(4,lung).
body_120(119,lung) :- body_15(13,lung).
body_128(127,tub) :- body_23(22,tub).
body_136(135,tub) :- body_33(31,tub).
body_144(143,bronc) :- body_41(40,bronc).
body_152(151,bronc) :- body_51(49,bronc).
body_160(159,either) :- body_78(73,either).
body_168(167,xray) :- body_86(85,xray).
body_177(176,xray) :- body_96(94,xray).
body_185(184,dysp) :- body_106(103,dysp).
body_194(193,dysp) :- body_118(114,dysp).
body_202(201,dysp) :- body_129(125,dysp).
body_210(209,dysp) :- body_141(136,dysp).
utility(\+(dysp),-41.08059745935331).
utility(lung,8.129762637966564).
utility(\+(lung),-28.07336315842413).
utility(tub,0.588926087798835).
utility(\+(tub),-20.532526608256386).
utility(smoke,-11.418494958221642).
utility(asia,1.258464492022623).
utility(bronc,18.292890222112607).
0.1::lung :- body_112(111,lung).
0.01::lung :- body_120(119,lung).
0.05::tub :- body_128(127,tub).
0.01::tub :- body_136(135,tub).
0.6::bronc :- body_144(143,bronc).
0.3::bronc :- body_152(151,bronc).
0.0::either :- body_160(159,either).
0.98::xray :- body_168(167,xray).
0.05::xray :- body_177(176,xray).
0.9::dysp :- body_185(184,dysp).
0.8::dysp :- body_194(193,dysp).
0.7::dysp :- body_202(201,dysp).
0.1::dysp :- body_210(209,dysp).
