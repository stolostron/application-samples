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

## Application Console: Create a new application
Using the application console, you can easily create an Application to run this demo.

#### Console
1. Open the Red Hat Advanced Cluster Management for Kubernetes console
2. Navigate on the left navigation menu to `Managed applications`
3. Click the `Create application` button
4. Enter the following values:
  * **Name:** `mortgage`
  * **Namespace:** `mortgage`
  * **Repository types:** `Git`
  * **URL:** `https://github.com/open-cluster-management/application-samples.git`
  * **Branch:** `main`
  * **Path:** `mortgage`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name:** `usage`
  * **Label value:** `development`
5. Click `Save`

### Viewing
1. Navigate on the left navigation menu to `Managed applications`
2. Click the `mortgage` Application name.
3. View the Topology
4. Click the `Route` node to obtain the application URL
5. Click the URL to see the helloworld sample app

