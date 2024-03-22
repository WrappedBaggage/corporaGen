Hei, 
Ettersom vi skal se på hvordan vi tenker å prompte dette programmet sender jeg deg den AI genererte mail med reply python scriptet jeg har lagd. Er nok ikke det mest ryddige scriptet så jeg har lagt ved kommentarer og skriver en oversikt for å gjøre det meste mulig tydelig. 

Hele scriptet kjøres fra "scenario_mail_reply.py". 

Den starter med å kjøre "scenario_generator.py" der den bruker fine tunet navn- og bedriftsnavngeneratorer fra "generator_functions.py". Med disse så lager den et scenario forholdsvis likt til Sarah Mitchell casen vi hadde i DFPP. Dette scenarioet, samt navn, emailadresser og brukernavn blir lagret i en variabler som gjenbrukes senere.

"scenario_mail.py" er første prosessen for email generation. Querien er ganske spesifik i hva den spørr etter så må vi finne på noe lurt hvis vi skal ha stor variasjon i outputen, men samtidig sørge for at den er relevant.

"scenario_mail_reply.py" lager en reply basert på subject og message body som ble returned av scenario_mail funksjonen i "scenario_mail.py".