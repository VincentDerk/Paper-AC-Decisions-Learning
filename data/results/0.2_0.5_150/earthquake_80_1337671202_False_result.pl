0.02::earthquake.
0.01::burglary.
body_7(4,alarm) :- burglary, earthquake.
body_19(15,alarm) :- burglary, \+earthquake.
body_30(26,alarm) :- \+burglary, earthquake.
body_42(37,alarm) :- \+burglary, \+earthquake.
body_50(49,maryCalls) :- alarm.
body_60(58,maryCalls) :- \+alarm.
body_68(67,johnCalls) :- alarm.
body_78(76,johnCalls) :- \+alarm.
query(johnCalls).
query(maryCalls).
query(burglary).
query(alarm).
query(earthquake).
utility(johnCalls,0).
utility(\+(johnCalls),49).
utility(alarm,-37).

body_56(55,alarm) :- body_7(4,alarm).
body_64(63,alarm) :- body_19(15,alarm).
body_72(71,alarm) :- body_30(26,alarm).
body_80(79,alarm) :- body_42(37,alarm).
body_88(87,maryCalls) :- body_50(49,maryCalls).
body_97(96,maryCalls) :- body_60(58,maryCalls).
body_105(104,johnCalls) :- body_68(67,johnCalls).
body_114(113,johnCalls) :- body_78(76,johnCalls).
utility(earthquake,-47.214338122484016).
0.95::alarm :- body_56(55,alarm).
0.94::alarm :- body_64(63,alarm).
0.29::alarm :- body_72(71,alarm).
0.001::alarm :- body_80(79,alarm).
0.7::maryCalls :- body_88(87,maryCalls).
0.01::maryCalls :- body_97(96,maryCalls).
0.9::johnCalls :- body_105(104,johnCalls).
0.05::johnCalls :- body_114(113,johnCalls).
