%% ProbLog program: PGM 1
%% Created on 2019-11-05 14:03:52.280759

0.81222222::plcg("1"); 0.08333333::plcg("2"); 0.10444444::plcg("3").
0.42314815::pKC("1"); 0.48166667::pKC("2"); 0.09518519::pKC("3").
0.2184223::pIP3("1"); 0.4473324::pIP3("2"); 0.3342453::pIP3("3") :- plcg("1").
0.07777778::pIP3("1"); 0.21111111::pIP3("2"); 0.71111111::pIP3("3") :- plcg("2").
0.4237589::pIP3("1"); 0.4397163::pIP3("2"); 0.1365248::pIP3("3") :- plcg("3").
0.3864333::pKA("1"); 0.3794311::pKA("2"); 0.2341357::pKA("3") :- pKC("1").
0.0603614::pKA("1"); 0.92272203::pKA("2"); 0.01691657::pKA("3") :- pKC("2").
0.0155642::pKA("1"); 0.95914397::pKA("2"); 0.02529183::pKA("3") :- pKC("3").
0.30690827::p38("1"); 0.06455266::p38("2"); 0.62853907::p38("3") :- pKA("1"), pKC("1").
0.656051::p38("1"); 0.343949::p38("2"); 0.0::p38("3") :- pKA("1"), pKC("2").
0.875::p38("1"); 0.125::p38("2"); 0.0::p38("3") :- pKA("1"), pKC("3").
0.919261822::p38("1"); 0.078431373::p38("2"); 0.002306805::p38("3") :- pKA("2"), pKC("1").
0.815::p38("1"); 0.185::p38("2"); 0.0::p38("3") :- pKA("2"), pKC("2").
0.803245436::p38("1"); 0.192697769::p38("2"); 0.004056795::p38("3") :- pKA("2"), pKC("3").
0.80747664::p38("1"); 0.09158879::p38("2"); 0.10093458::p38("3") :- pKA("3"), pKC("1").
0.3863636::p38("1"); 0.1590909::p38("2"); 0.4545455::p38("3") :- pKA("3"), pKC("2").
0.7692308::p38("1"); 0.2307692::p38("2"); 0.0::p38("3") :- pKA("3"), pKC("3").
0.06228766::raf("1"); 0.14722537::raf("2"); 0.79048698::raf("3") :- pKA("1"), pKC("1").
0.3694268::raf("1"); 0.3312102::raf("2"); 0.2993631::raf("3") :- pKA("1"), pKC("2").
0.875::raf("1"); 0.125::raf("2"); 0.0::raf("3") :- pKA("1"), pKC("3").
0.4475202::raf("1"); 0.3125721::raf("2"); 0.2399077::raf("3") :- pKA("2"), pKC("1").
0.5508333::raf("1"); 0.3929167::raf("2"); 0.05625::raf("3") :- pKA("2"), pKC("2").
0.8843813::raf("1"); 0.1156187::raf("2"); 0.0::raf("3") :- pKA("2"), pKC("3").
0.84299065::raf("1"); 0.1271028::raf("2"); 0.02990654::raf("3") :- pKA("3"), pKC("1").
0.75::raf("1"); 0.15909091::raf("2"); 0.09090909::raf("3") :- pKA("3"), pKC("2").
0.8461538::raf("1"); 0.1538462::raf("2"); 0.0::raf("3") :- pKA("3"), pKC("3").
0.2899207::jnk("1"); 0.2457531::jnk("2"); 0.4643262::jnk("3") :- pKA("1"), pKC("1").
0.5796178::jnk("1"); 0.4203822::jnk("2"); 0.0::jnk("3") :- pKA("1"), pKC("2").
0.0::jnk("1"); 1.0::jnk("2"); 0.0::jnk("3") :- pKA("1"), pKC("3").
0.5767013::jnk("1"); 0.4232987::jnk("2"); 0.0::jnk("3") :- pKA("2"), pKC("1").
0.6129167::jnk("1"); 0.3870833::jnk("2"); 0.0::jnk("3") :- pKA("2"), pKC("2").
0.04462475::jnk("1"); 0.93509128::jnk("2"); 0.02028398::jnk("3") :- pKA("2"), pKC("3").
0.996261682::jnk("1"); 0.003738318::jnk("2"); 0.0::jnk("3") :- pKA("3"), pKC("1").
0.8636364::jnk("1"); 0.1363636::jnk("2"); 0.0::jnk("3") :- pKA("3"), pKC("2").
0.1538462::jnk("1"); 0.8461538::jnk("2"); 0.0::jnk("3") :- pKA("3"), pKC("3").
0.996868476::pIP2("1"); 0.003131524::pIP2("2"); 0.0::pIP2("3") :- pIP3("1"), plcg("1").
1.0::pIP2("1"); 0.0::pIP2("2"); 0.0::pIP2("3") :- pIP3("1"), plcg("2").
0.2217573::pIP2("1"); 0.4937238::pIP2("2"); 0.2845188::pIP2("3") :- pIP3("1"), plcg("3").
0.98674822::pIP2("1"); 0.01325178::pIP2("2"); 0.0::pIP2("3") :- pIP3("2"), plcg("1").
0.95789474::pIP2("1"); 0.04210526::pIP2("2"); 0.0::pIP2("3") :- pIP3("2"), plcg("2").
0.0766129::pIP2("1"); 0.391129::pIP2("2"); 0.5322581::pIP2("3") :- pIP3("2"), plcg("3").
0.872442019::pIP2("1"); 0.12005457::pIP2("2"); 0.007503411::pIP2("3") :- pIP3("3"), plcg("1").
0.521875::pIP2("1"); 0.4625::pIP2("2"); 0.015625::pIP2("3") :- pIP3("3"), plcg("2").
0.02597403::pIP2("1"); 0.05194805::pIP2("2"); 0.92207792::pIP2("3") :- pIP3("3"), plcg("3").
0.7454545::mek("1"); 0.2545455::mek("2"); 0.0::mek("3") :- pKA("1"), pKC("1"), raf("1").
0.3846154::mek("1"); 0.1230769::mek("2"); 0.4923077::mek("3") :- pKA("1"), pKC("1"), raf("2").
0.26217765::mek("1"); 0.001432665::mek("2"); 0.736389685::mek("3") :- pKA("1"), pKC("1"), raf("3").
0.7068966::mek("1"); 0.2931034::mek("2"); 0.0::mek("3") :- pKA("1"), pKC("2"), raf("1").
0.2692308::mek("1"); 0.7307692::mek("2"); 0.0::mek("3") :- pKA("1"), pKC("2"), raf("2").
0.85106383::mek("1"); 0.10638298::mek("2"); 0.04255319::mek("3") :- pKA("1"), pKC("2"), raf("3").
0.8571429::mek("1"); 0.1428571::mek("2"); 0.0::mek("3") :- pKA("1"), pKC("3"), raf("1").
0.0::mek("1"); 1.0::mek("2"); 0.0::mek("3") :- pKA("1"), pKC("3"), raf("2").
0.3333333::mek("1"); 0.3333333::mek("2"); 0.3333333::mek("3") :- pKA("1"), pKC("3"), raf("3").
0.757732::mek("1"); 0.242268::mek("2"); 0.0::mek("3") :- pKA("2"), pKC("1"), raf("1").
0.343173432::mek("1"); 0.649446494::mek("2"); 0.007380074::mek("3") :- pKA("2"), pKC("1"), raf("2").
0.86538462::mek("1"); 0.10096154::mek("2"); 0.03365385::mek("3") :- pKA("2"), pKC("1"), raf("3").
0.714826::mek("1"); 0.285174::mek("2"); 0.0::mek("3") :- pKA("2"), pKC("2"), raf("1").
0.274655355::mek("1"); 0.720042418::mek("2"); 0.005302227::mek("3") :- pKA("2"), pKC("2"), raf("2").
0.2814815::mek("1"); 0.5851852::mek("2"); 0.1333333::mek("3") :- pKA("2"), pKC("2"), raf("3").
0.8256881::mek("1"); 0.1743119::mek("2"); 0.0::mek("3") :- pKA("2"), pKC("3"), raf("1").
0.1052632::mek("1"); 0.8947368::mek("2"); 0.0::mek("3") :- pKA("2"), pKC("3"), raf("2").
0.3333333::mek("1"); 0.3333333::mek("2"); 0.3333333::mek("3") :- pKA("2"), pKC("3"), raf("3").
0.997782705::mek("1"); 0.002217295::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("1"), raf("1").
1.0::mek("1"); 0.0::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("1"), raf("2").
0.9375::mek("1"); 0.0::mek("2"); 0.0625::mek("3") :- pKA("3"), pKC("1"), raf("3").
0.96969697::mek("1"); 0.03030303::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("2"), raf("1").
0.8571429::mek("1"); 0.1428571::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("2"), raf("2").
0.5::mek("1"); 0.5::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("2"), raf("3").
0.7272727::mek("1"); 0.2727273::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("3"), raf("1").
0.0::mek("1"); 1.0::mek("2"); 0.0::mek("3") :- pKA("3"), pKC("3"), raf("2").
0.3333333::mek("1"); 0.3333333::mek("2"); 0.3333333::mek("3") :- pKA("3"), pKC("3"), raf("3").
0.85066667::erk("1"); 0.13866667::erk("2"); 0.01066667::erk("3") :- mek("1"), pKA("1").
0.1177011::erk("1"); 0.691954::erk("2"); 0.1903448::erk("3") :- mek("1"), pKA("2").
0.07401033::erk("1"); 0.70051635::erk("2"); 0.22547332::erk("3") :- mek("1"), pKA("3").
0.3870968::erk("1"); 0.483871::erk("2"); 0.1290323::erk("3") :- mek("2"), pKA("1").
0.04893754::erk("1"); 0.72826787::erk("2"); 0.22279459::erk("3") :- mek("2"), pKA("2").
0.0::erk("1"); 0.1::erk("2"); 0.9::erk("3") :- mek("2"), pKA("3").
0.00862069::erk("1"); 0.18793103::erk("2"); 0.80344828::erk("3") :- mek("3"), pKA("1").
0.0::erk("1"); 0.75::erk("2"); 0.25::erk("3") :- mek("3"), pKA("2").
0.0::erk("1"); 0.0::erk("2"); 1.0::erk("3") :- mek("3"), pKA("3").
0.6722222::akt("1"); 0.3277778::akt("2"); 0.0::akt("3") :- erk("1"), pKA("1").
0.6204819::akt("1"); 0.3795181::akt("2"); 0.0::akt("3") :- erk("1"), pKA("2").
0.97674419::akt("1"); 0.02325581::akt("2"); 0.0::akt("3") :- erk("1"), pKA("3").
0.3349515::akt("1"); 0.6650485::akt("2"); 0.0::akt("3") :- erk("2"), pKA("1").
0.8214285714::akt("1"); 0.1781954887::akt("2"); 0.0003759398::akt("3") :- erk("2"), pKA("2").
0.94852941::akt("1"); 0.05147059::akt("2"); 0.0::akt("3") :- erk("2"), pKA("3").
0.0::akt("1"); 0.1182573::akt("2"); 0.8817427::akt("3") :- erk("3"), pKA("1").
0.177083333::akt("1"); 0.813802083::akt("2"); 0.009114583::akt("3") :- erk("3"), pKA("2").
0.1702128::akt("1"); 0.8297872::akt("2"); 0.0::akt("3") :- erk("3"), pKA("3").
