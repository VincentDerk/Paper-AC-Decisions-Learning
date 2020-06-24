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
query(burglary).
query(johnCalls).
query(earthquake).
query(maryCalls).


utility(\+(burglary),-20).
utility(johnCalls,26).
utility(\+(johnCalls),-13).

utility(maryCalls,-29).
utility(\+(maryCalls),-44).
body_62(61,alarm) :- body_7(4,alarm).
body_70(69,alarm) :- body_19(15,alarm).
body_78(77,alarm) :- body_30(26,alarm).
body_85(84,alarm) :- body_42(37,alarm).
body_93(92,maryCalls) :- body_50(49,maryCalls).
body_102(101,maryCalls) :- body_60(58,maryCalls).
body_110(109,johnCalls) :- body_68(67,johnCalls).
body_119(118,johnCalls) :- body_78(76,johnCalls).
utility(alarm,0.154129791219867).
utility(\+(alarm),1.002782431347593).
utility(earthquake,0.35563757163633).
0.95::alarm :- body_62(61,alarm).
0.94::alarm :- body_70(69,alarm).
0.29::alarm :- body_78(77,alarm).
0.001::alarm :- body_85(84,alarm).
0.7::maryCalls :- body_93(92,maryCalls).
0.01::maryCalls :- body_102(101,maryCalls).
0.9::johnCalls :- body_110(109,johnCalls).
0.05::johnCalls :- body_119(118,johnCalls).
