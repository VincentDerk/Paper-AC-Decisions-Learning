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
query(alarm).
query(earthquake).
query(maryCalls).
query(johnCalls).
query(burglary).
utility(alarm,23).
utility(\+(alarm),50).
utility(earthquake,26).
utility(maryCalls,45).
utility(\+(maryCalls),-43).
utility(burglary,11).
0.95::alarm :- body_7(4,alarm).
0.94::alarm :- body_19(15,alarm).
0.29::alarm :- body_30(26,alarm).
0.001::alarm :- body_42(37,alarm).
0.7::maryCalls :- body_50(49,maryCalls).
0.01::maryCalls :- body_60(58,maryCalls).
0.9::johnCalls :- body_68(67,johnCalls).
0.05::johnCalls :- body_78(76,johnCalls).
