# Plateforme Oracle IA – Supervision, Sécurité et Optimisation Intelligente

**Réaliser par : Achraf EL AZZOUZI & Mehdi LAGHRISSI**

## Introduction

Ce projet présente une plateforme web innovante développée avec Python et Streamlit, dédiée aux administrateurs de bases de données Oracle (DBA). L'objectif principal est de centraliser la supervision des systèmes Oracle tout en automatisant l'analyse grâce à l'intelligence artificielle (IA), via un modèle de langage (LLM). Cette solution vise à simplifier les tâches complexes de gestion, d'audit et d'optimisation, en offrant une interface intuitive et des recommandations intelligentes.

## Modules Fonctionnels

La plateforme est organisée autour de six modules principaux, chacun répondant à un besoin spécifique des DBA :

### Dashboard Global

Ce module offre une vue d'ensemble synthétique de l'état du système Oracle. Il affiche des indicateurs clés tels que le niveau de sécurité, la disponibilité des services et l'état des sauvegardes, permettant une surveillance rapide et centralisée.

### Audit de Sécurité Oracle

Il analyse en profondeur les utilisateurs, rôles, privilèges et configurations système. Un score de sécurité est calculé automatiquement, avec détection des risques potentiels et recommandations générées par l'IA pour renforcer la protection des données.

### Optimisation des Performances

Ce module examine les requêtes lentes et propose des recommandations SQL automatiques pour améliorer les performances. Il aide à identifier les goulots d'étranglement et suggère des optimisations adaptées au contexte opérationnel.

### Stratégie de Sauvegarde Intelligente

En tenant compte des objectifs de point de récupération (RPO), de temps de restauration (RTO) et du budget disponible, ce module génère un plan de sauvegarde personnalisé. Il recommande des stratégies adaptées aux besoins spécifiques de l'entreprise.

### Assistant de Restauration

Face à un incident, cet outil produit des playbooks détaillés pour la reprise : restauration point-in-time (PITR), récupération de tables spécifiques ou récupération complète après un crash. Il fournit un support décisionnel en temps réel pour minimiser les interruptions.

### Chatbot IA Oracle

Le chatbot comprend les intentions des utilisateurs en langage naturel et les redirige automatiquement vers le module approprié. Il offre une assistance interactive pour répondre aux questions des DBA, facilitant l'accès aux fonctionnalités sans navigation complexe.

## Architecture

L'architecture de la plateforme est modulaire et flexible, permettant à chaque module de fonctionner de manière indépendante. Les rapports générés sont stockés sous forme de fichiers JSON ou Markdown, assurant une traçabilité et une réutilisabilité. Le moteur d'IA (LLM) est intégré comme couche d'analyse centrale, traitant les données pour produire des recommandations pertinentes et contextuelles.

## Valeur Ajoutée

Cette plateforme apporte une valeur significative aux DBA en réduisant considérablement le temps consacré aux tâches répétitives et en minimisant les erreurs humaines. Elle centralise les décisions critiques dans une interface unique, tout en intégrant l'IA pour une prise de décision assistée. Les recommandations automatiques améliorent l'efficacité opérationnelle, renforçant ainsi la sécurité, les performances et la résilience des systèmes Oracle.

## Conclusion

En résumé, la Plateforme Oracle IA transforme la gestion des bases de données en un processus intelligent et automatisé, offrant aux DBA un outil puissant pour superviser, sécuriser et optimiser leurs environnements. L'apport de l'IA se manifeste par des analyses prédictives et des suggestions personnalisées, ouvrant des perspectives prometteuses telles que l'intégration dans le cloud, l'extension vers les centres d'opérations de sécurité (SOC) et l'adoption des pratiques AIOps pour une gestion proactive et scalable. Ce projet démontre le potentiel de l'IA pour révolutionner les pratiques IT traditionnelles.
