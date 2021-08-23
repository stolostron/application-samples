# Demonstrate a sample keycloak application
## Tool Requirements
- OpenShift CLI Version >= 4.3.0<br>_Needed for kustomize_

```bash
oc version
```

- OpenShift Data Foundation Version >= 4.4.0<br>_For general use case_
- OpenShift Data Foundation Version >= 4.7.0<br>_For Disaster Recovery use case_

```bash
oc get csv pn openshift-storage
NAME                  DISPLAY                       VERSION   REPLACES   PHASE
ocs-operator.v4.8.0   OpenShift Container Storage   4.8.0                Succeeded
```

## Summary
Demonstrate a keycloak application (frontend+backend) leveraging Red Hat OpenShift Data Foundation block device capabilites when deployed using ACM. This application offers a WEB UI while using a PostgreSQL database to store its information.

## Prerequisite

- 1+ managed-clusters total
- Those `Managed-Cluster` to target, must have a label with `metadata.labels.usage: development`
- Target clusters must have the PostgreSQL Operator Deployed
- Target clusters must have the Red Hat OpenShift Data Foundation or the Rook-Ceph Operator deployed and an operational Ceph cluster deployed

## Application Console: Create a new application
Using the application console, you can easily create an Application to run this demo.

#### Console
1. Open the Red Hat Advanced Cluster Management for Kubernetes console
2. Navigate on the left navigation menu to `Managed applications`
3. Click the `Create application` button
4. Enter the following values:
  * **Name:** `keycloak-odf`
  * **Namespace:** `keycloak-odf`
  * **Repository types:** `Git`
  * **URL:** `https://github.com/open-cluster-management/application-samples.git`
  * **Branch:** `main`
  * **Path:** `keycloak-odf`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name:** `usage`
  * **Label value:** `development`
5. Click `Save`

### Viewing
1. Navigate on the left navigation menu to `Managed applications`
2. Click the `keycloak-odf` Application name.
3. View the Topology
4. Click the `Route` node to obtain the application URL
5. Click the URL to see the keycloak sample application

