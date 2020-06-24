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
query(burglary).
query(johnCalls).
query(alarm).
query(earthquake).


utility(\+(johnCalls),48).


body_60(59,alarm) :- body_7(4,alarm).
body_67(66,alarm) :- body_19(15,alarm).
body_75(74,alarm) :- body_30(26,alarm).
body_83(82,alarm) :- body_42(37,alarm).
body_91(90,maryCalls) :- body_50(49,maryCalls).
body_100(99,maryCalls) :- body_60(58,maryCalls).
body_108(107,johnCalls) :- body_68(67,johnCalls).
body_117(116,johnCalls) :- body_78(76,johnCalls).
utility(\+(maryCalls),-27.24415581230083).
utility(burglary,20.706360960899023).
utility(earthquake,-32.61897704443802).
utility(\+(earthquake),28.450005436694127).
0.95::alarm :- body_60(59,alarm).
0.94::alarm :- body_67(66,alarm).
0.29::alarm :- body_75(74,alarm).
0.001::alarm :- body_83(82,alarm).
0.7::maryCalls :- body_91(90,maryCalls).
0.01::maryCalls :- body_100(99,maryCalls).
0.9::johnCalls :- body_108(107,johnCalls).
0.05::johnCalls :- body_117(116,johnCalls).
