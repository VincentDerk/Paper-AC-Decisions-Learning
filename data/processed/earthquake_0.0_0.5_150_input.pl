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
query(johnCalls).
query(burglary).
query(alarm).
query(earthquake).
utility(maryCalls,44).
utility(\+(maryCalls),t(V_0)) :- true.
utility(\+(burglary),t(V_0)) :- true.
utility(alarm,t(V_0)) :- true.
utility(\+(earthquake),10).
0.7::maryCalls :- body_50(49,maryCalls).
0.9::johnCalls :- body_68(67,johnCalls).
0.95::alarm :- body_7(4,alarm).
0.001::alarm :- body_42(37,alarm).
0.29::alarm :- body_30(26,alarm).
0.05::johnCalls :- body_78(76,johnCalls).
0.01::maryCalls :- body_60(58,maryCalls).
0.94::alarm :- body_19(15,alarm).
