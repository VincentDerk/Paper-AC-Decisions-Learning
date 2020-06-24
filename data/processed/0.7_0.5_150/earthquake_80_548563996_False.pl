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
query(maryCalls).
query(earthquake).
query(alarm).
query(johnCalls).
query(burglary).
utility(maryCalls,17).
utility(\+(maryCalls),3).
utility(\+(earthquake),-20).
utility(alarm,26).
utility(\+(alarm),-13).
utility(johnCalls,-47).
utility(burglary,-29).
utility(\+(burglary),-44).
0.95::alarm :- body_7(4,alarm).
0.94::alarm :- body_19(15,alarm).
0.29::alarm :- body_30(26,alarm).
0.001::alarm :- body_42(37,alarm).
0.7::maryCalls :- body_50(49,maryCalls).
0.01::maryCalls :- body_60(58,maryCalls).
0.9::johnCalls :- body_68(67,johnCalls).
0.05::johnCalls :- body_78(76,johnCalls).
