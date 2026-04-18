from llm.client import call_llm

prompt = """
You are a strict information extraction system.

Extract ONLY technical skills from each job description.

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No comments
- Output must be a JSON array
- Return exactly one object per input job
- Keep the exact same job_id values
- Each item must have:
  - "job_id": string
  - "skills": array of strings
- "skills" must always be a real JSON array, never a string
- Only technical skills: programming languages, frameworks, libraries, cloud, databases, DevOps, data tools
- No soft skills
- No duplicates inside each skills list
- If no technical skill is found, return an empty list for that job
- Never omit a job


Job description:
"Bienvenue chez JCDecaux !  \nAu sein de la Direction DataCorp, chargée de l'exploitation et de la valorisation des données à travers le groupe, nous recherchons un Data Engineer - Data Solutions (H/F) pour intégrer une équipe dynamique composée de Data Engineers, Data Scientists, Data Analysts et DevOps. Vous contribuerez à concevoir, industrialiser et opérer des Data Solutions destinées à nos clients internes (filiales) : ETL custom, algorithmes et méthodologies de production de données opérationnelles, génération d'insights, modèles de Machine Learning (prédiction, classification, optimisation, etc.).\n\nAu quotidien vous serez amené(e) à :\n-       Concevoir, développer et industrialiser des Data Solutions de bout-en-bout (de l'ingestion au monitoring) pour répondre aux besoins opérationnels des filiales.\n-       Construire et maintenir des pipelines de données (batch et/ou temps réel) robustes, performants et monitorés, pour alimenter ces solutions (ETL/ELT, APIs, pub/sub).\n-       Co-concevoir avec les Data Scientists et Data Analysts des algorithmes et méthodologies (segmentation, scoring, prévisions, optimisation, règles métier avancées, etc.) et les transformer en produits data industrialisés.\n-       Mettre en production des modèles de Machine Learning (MLOps) : packaging, déploiement, orchestration, suivi de performance, versioning des modèles et des datasets.\n-       Participer à la définition des architectures cibles des Data Solutions en vous appuyant sur la Data Platform \"Lakehouse\" de JCDecaux et sur les services Cloud disponibles.\n-       Optimiser la performance, la qualité, la fiabilité et les coûts d'exécution des Data Solutions (optimisation de requêtes, partitionnement, caching, choix de formats, dimensionnement infra).\n-       Évoluer à proximité des Product Owners dans la définition et delivery des Data Solutions..\n-       Contribuer à l'élaboration de bonnes pratiques d'architecture, de code, de tests et de monitoring (patterns de data products, data contracts, CI/CD, observabilité data) ;\n-       Assurer une veille technologique sur les architectures de data products, les bonnes pratiques Data Engineering / MLOps / ML Engineering, tester de nouveaux outils et partager vos retours (communautés internes, conférences, POC).\nAmoureux(se) de la Data, vous êtes motivé(e) par la création de solutions concrètes et utilisées au quotidien par les équipes opérationnelles. Vous aimez autant bâtir des pipelines robustes que transformer un algorithme en produit data fiable, scalable et maintenable.\nCurieux(se), autonome, vous avez le goût de l'optimisation et des approches algorithmiques, et vous savez travailler en proximité avec le métier pour comprendre les besoins et les traduire en solutions techniques pérennes.\nDe formation Bac +5 minimum de type école d'ingénieur ou université (informatique, mathématiques appliquées, data, statistiques, opérations de recherche ou équivalent), vous disposez d'au moins 3 ans d'expérience dans le traitement de données en environnement industriel, incluant le développement de solutions ou produits data sur une infrastructure Big Data ou Cloud.\nVous maîtrisez un environnement Cloud (AWS, Azure ou GCP) et avez déjà participé au déploiement d'applications ou services data en production.\nCompétences requises:\nMaîtrise des langages Python et SQL, avec de bonnes pratiques de développement (tests, packaging, revue de code, logging).\nMaîtrise des technologies de Data Engineering et de transformation :\nOutils de modélisation / transformation (dbt ou équivalent)\nConception d'ETL/ELT custom (Airflow, Dagster, etc.)\nStockage et traitement à l'échelle (Data Lake S3, Snowflake, Redshift ou équivalent)\n\nBonne compréhension des approches algorithmiques et des briques Data Science / ML :\nManipulation de données (pandas, PySpark, etc.)\nMise en production de modèles ...",
    
"""

response = call_llm(prompt)
print(response)