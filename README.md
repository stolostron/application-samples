# Application Samples
The home for Application samples, based on the open-cluster-management.io Subscription, Channel and Placement API

## Requirements
- `open-cluster-management.io` or Red Hat Advanced Cluster Management for Kubernetes.
- Clusters labelled as `development`, `test` and/or `production`
```yaml
metadata:
  labels:
    usage: development
```

# How to use
1. The first time you want to start using the Subscriptions from the CLI, add the channel (source) repository.
```bash
oc apply -k subscriptions/channel
```
2. Now apply the subscription you want to demonstrate
```bash
oc apply -k subscriptions/DEMO_APP_NAME
```
3. You can also add these applications using the Red Had Advanced Cluster Management for Kubernetes console.
