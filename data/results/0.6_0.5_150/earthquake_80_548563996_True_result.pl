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
query(burglary).
query(earthquake).
query(alarm).
query(maryCalls).
query(johnCalls).


utility(\+(earthquake),-20).
utility(alarm,26).
utility(\+(alarm),-13).

utility(johnCalls,-29).
utility(\+(johnCalls),-44).
body_62(61,alarm) :- body_7(4,alarm).
body_70(69,alarm) :- body_19(15,alarm).
body_78(77,alarm) :- body_30(26,alarm).
body_85(84,alarm) :- body_42(37,alarm).
body_93(92,maryCalls) :- body_50(49,maryCalls).
body_102(101,maryCalls) :- body_60(58,maryCalls).
body_110(109,johnCalls) :- body_68(67,johnCalls).
body_119(118,johnCalls) :- body_78(76,johnCalls).
utility(burglary,-29.12349779289866).
utility(\+(burglary),1.943406074129074).
utility(maryCalls,20.62787076675274).
0.95::alarm :- body_62(61,alarm).
0.94::alarm :- body_70(69,alarm).
0.29::alarm :- body_78(77,alarm).
0.001::alarm :- body_85(84,alarm).
0.7::maryCalls :- body_93(92,maryCalls).
0.01::maryCalls :- body_102(101,maryCalls).
0.9::johnCalls :- body_110(109,johnCalls).
0.05::johnCalls :- body_119(118,johnCalls).
