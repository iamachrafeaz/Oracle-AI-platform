
# security_users_roles

Utilisateurs, rôles, profils, least privilege

Contexte / Objectif
Ce document présente la gestion des utilisateurs Oracle, des rôles, des privilèges et des profils. Il se concentre sur la sécurité d’accès, le principe du least privilege et les pratiques recommandées pour contrôler l’accès aux ressources de la base.

Points clés

* Un utilisateur Oracle correspond à un compte d’accès + un schéma associé.
* Les rôles regroupent un ensemble de privilèges pour simplifier leur gestion.
* Types de privilèges :

  * System privileges : création, modification, administration globale.
  * Object privileges : SELECT, INSERT, UPDATE, EXECUTE sur un objet spécifique.
* Les profils régulent les paramètres de sécurité : politiques de mots de passe, limites de ressources, nombre de sessions.
* Le least privilege limite chaque utilisateur uniquement aux droits nécessaires à son rôle.

Bonnes pratiques

* Ne jamais accorder de rôles puissants (DBA, RESOURCE) sans justification formelle.
* Créer des rôles applicatifs dédiés (lecture, reporting, batch).
* Appliquer des règles de mot de passe strictes via des profils personnalisés.
* Révoquer régulièrement les privilèges inutilisés ou hérités.
* Activer l’audit pour tous les comptes privilégiés ou critiques.
* Séparer les comptes administratifs et applicatifs (éviter un compte unique polyvalent).

Exemples Oracle SQL
Créer un utilisateur :
CREATE USER app_user IDENTIFIED BY StrongPwd#2025;

Créer un rôle applicatif :
CREATE ROLE reporting_role;

Assigner des privilèges à un rôle :
GRANT SELECT ON sales TO reporting_role;

Accorder un rôle à un utilisateur :
GRANT reporting_role TO app_user;

Créer un profil sécurisé :
CREATE PROFILE secure_profile
LIMIT FAILED_LOGIN_ATTEMPTS 5
PASSWORD_LIFE_TIME 30
PASSWORD_REUSE_TIME 90
SESSIONS_PER_USER 2;

Associer un profil à un utilisateur :
ALTER USER finance_user PROFILE secure_profile;

Pièges à éviter

* Accorder des privilèges `ANY` (CREATE ANY TABLE, DROP ANY VIEW…) sans contrôle strict.
* Réutiliser un rôle trop générique pour plusieurs applications.
* Utiliser des mots de passe faibles ou similaires entre comptes.
* Oublier de limiter l’accès aux vues système sensibles (V$ views).
* Désactiver l’audit sur des comptes à privilèges élevés.

Quand utiliser ?

* Pour sécuriser les environnements de production et pré-production.
* Lors de la création de nouveaux comptes utilisateurs ou comptes techniques.
* Lorsqu’un audit détecte des privilèges excessifs.
* Pour respecter les exigences de conformité (ISO, RGPD, PCI-DSS).
* Dans les processus DevOps / CI-CD pour automatiser la gouvernance des accès.

Résumé essentiel
La gestion des utilisateurs, des rôles et des profils constitue la base de la sécurité Oracle. En appliquant les principes de least privilege, des profils stricts et une gouvernance rigoureuse des privilèges, on réduit considérablement les risques d’accès non autorisé, d’abus de droits ou de compromission.

