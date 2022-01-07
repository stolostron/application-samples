# Part of the Pacman application found in this repository

## This example, Deploys nginx with an internal service, that allows reading the Cloud provider and Region json. This is designed to work with the modified Pacman application.
1. Add the subscription to your Red Hat Advanced Cluster Management for Kubernetes HUB
```
clone https://github.com/mbaldessari/application-samples.git
oc apply -k application-samples/subscriptoins/cloud-provider
```
### results
This will automatically provision the nginx with cloud provider and region identifier to:
### Amazon AWS
- us-east-1
- us-east-2
- us-east-3
- us-west-1
- eu-central-1
- eu-west-3

### Google GCP
- europe-west3

### Azure
- centralus

### Related
Pacman deployment with an Ansible job in: `ansible/`