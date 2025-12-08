\# BioGuard — DNA-Inspired Intrusion Detection System



This project implements a simple end-to-end IDS pipeline:



\- data\_pipeline: feature extraction + ingest API

\- model: autoencoder anomaly detection

\- detector\_service: REST API using trained model

\- automations: webhook that logs/blocks suspicious IPs



This repo is configured for deployment on Render using render.yaml.



