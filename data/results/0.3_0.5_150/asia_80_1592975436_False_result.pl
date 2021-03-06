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
query(dysp).
query(tub).
query(bronc).
query(xray).
query(lung).
query(either).
query(asia).
query(smoke).
utility(dysp,23).


utility(bronc,45).

utility(lung,11).

utility(\+(either),20).


body_108(107,lung) :- body_5(4,lung).
body_116(115,lung) :- body_15(13,lung).
body_124(123,tub) :- body_23(22,tub).
body_132(131,tub) :- body_33(31,tub).
body_140(139,bronc) :- body_41(40,bronc).
body_148(147,bronc) :- body_51(49,bronc).
body_156(155,either) :- body_78(73,either).
body_164(163,xray) :- body_86(85,xray).
body_173(172,xray) :- body_96(94,xray).
body_181(180,dysp) :- body_106(103,dysp).
body_190(189,dysp) :- body_118(114,dysp).
body_198(197,dysp) :- body_129(125,dysp).
body_206(205,dysp) :- body_141(136,dysp).
utility(\+(dysp),52.37660277933893).
utility(tub,49.76884539826897).
utility(\+(bronc),-46.60952683237664).
utility(either,36.414120512223306).
utility(asia,-3.331350957003687).
utility(smoke,17.34305627493682).
0.1::lung :- body_108(107,lung).
0.01::lung :- body_116(115,lung).
0.05::tub :- body_124(123,tub).
0.01::tub :- body_132(131,tub).
0.6::bronc :- body_140(139,bronc).
0.3::bronc :- body_148(147,bronc).
0.0::either :- body_156(155,either).
0.98::xray :- body_164(163,xray).
0.05::xray :- body_173(172,xray).
0.9::dysp :- body_181(180,dysp).
0.8::dysp :- body_190(189,dysp).
0.7::dysp :- body_198(197,dysp).
0.1::dysp :- body_206(205,dysp).
