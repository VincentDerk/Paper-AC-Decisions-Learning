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
query(either).
query(tub).
query(asia).
query(xray).
query(dysp).
query(lung).
query(smoke).
utility(bronc,17).
utility(\+(bronc),3).



utility(asia,-47).



utility(\+(dysp),-18).


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
utility(\+(either),-29.116672209733057).
utility(tub,-0.798162746789862).
utility(\+(tub),-25.98709572662885).
utility(xray,-4.384766818602044).
utility(\+(xray),-22.400491654816662).
utility(dysp,-43.262167522380835).
utility(lung,3.127536416086146).
utility(smoke,47.94635534025526).
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
