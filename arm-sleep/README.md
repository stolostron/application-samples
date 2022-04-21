# Demonstrate a sleep application on arm arch cluster
## Tool Requirements
- OpenShift CLI Version >= 4.3.0<br>_Needed for kustomize_
```bash
oc version
```

## Summary
Demonstrate a arm multi-arch supported application for deploying a sleep pod with its relatvie service account, role and rolebinding
```
% oc get pods
NAME                           READY   STATUS    RESTARTS   AGE
arm-sleep-7fb5495db4-zl2jj   1/1     Running   0          4m32s
```

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
  * **Name:** `arm-sleep`
  * **Namespace:** `arm-sleep`
  * **Repository types:** `Git`
  * **URL:** `https://github.com/open-cluster-management/application-samples.git`
  * **Branch:** `main`
  * **Path:** `arm-sleep`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name:** `usage`
  * **Label value:** `development`
5. Click `Save`

### Viewing
1. Navigate on the left navigation menu to `Managed applications`
2. Click the `arm-sleep` Application name.
3. View the Topology

