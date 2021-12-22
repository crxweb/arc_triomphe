# arc_triomphe

Exemple Python de webscrapping et de requêtes API permettant de collecter les données des chevaux de course ayant participer au prix de l'Arc de triomphe.


Réalisé en 2020 dans le cadre d'une collecte de données pour l'apprentissage des différents algorithmes en intelligence artificielle.

Le site france galop a été utilisé pour réaliser cette collecte.

France Galop permet de consulter les fiches chevaux, jockey, propriétaire avec des restrictions si l'utilisateur n'est pas abonné.

Ainsi une personne non abonnée ne peut pas remonter l'historique d'un cheval au delà d'environ 10 années.

En consultant les requêtes ajax effectuées par le navigateur il a été aisé de mettre en évidence les services disponibles permettant de réaliser la collecte sans bénéficier du privilège abonné.

Il a donc été possible ici de remonter l'historique de 1993 à 2020 jusqu'à ce que le site protège l'accès à ses web service.



