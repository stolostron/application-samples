# Demonstrate a mortgage application
## Tool Requirements
- OpenShift CLI Version >= 4.3.0<br>_Needed for kustomize_
```bash
oc version
```

## Summary
Demonstrate a mortgage web application for getting started with ACM applications. This is a sample J2EE application that accepts mortgage request information and determines approval. There are two built in users; bob and deb. Any password will work.

## Prerequisite
- 1+ managed-clusters total
- Those `Managed-Cluster` to target, must have a label with `metadata.labels.usage: development`

## Application Console: Create a new subscription
Using the application console, you can easily create an Application to run this demo.

#### Console
1. Open the Red Hat Advanced Cluster Management for Kubernetes console
1. Navigate on the left navigation menu to `Managed applications`
2. Choose `Create application`
3. Enter the following values:
  * **Name:** `mortgage`
  * **Namespace:** `mortgage`
  * **Repository types** `Git`
  * **URL** `https://github.com/open-cluster-management/application-samples.git`
  * **Branch** `master`
  * **Path** `mortgage`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name** `usage`
  * **Label value** `development`
4. Click `Save`

### Viewing
- Navigate on the left navigation menu to `Managed applications`
- Click the `mortgage` Application name.
- View the Topology
- Click the `Route` nodes to obtain the application URL
- Click the URL to see the helloworld sample app

