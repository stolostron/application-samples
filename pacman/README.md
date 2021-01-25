# Demonstrate multi resource application
## Tool Requirements
- OpenShift CLI Version >= 4.3.0<br>_Needed for kustomize_
```bash
oc version
```

## Summary
This provides a Pac-man application, where GitOps flows can be used to change the playing board from blue to green.

## Prerequisite
- 1+ managed-clusters
- Those `Managed-Cluster` to target, must have a label with `metadata.labels.usage: development`
- A fork of this repository

## Application Console: Create a new subscription
Using the application console, you can easily create an Application that runs Pac-man on your cluster(s). You can then update the deployment, and change the `image` from `latest` to `green`, using a Git merge.  This change will then be propogated to any subscribed clusters.

#### Console
1. Open the Red Hat Advanced Cluster Management for Kubernetes console
1. Navigate on the left navigation menu to `Managed applications`
2. Choose `Create application`
3. Enter the following values:
  * **Name:** `pacman`
  * **Namespace:** `pacman`
  * **Repository types** `Git`
  * **URL** `https://github.com/REPO_FORK_NAME/application-samples.git`
  * **Branch** `main`
  * **Path** `pacman`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name** `usage`
  * **Label value** `development`
4. Click `Save`

### Viewing
- Navigate on the left navigation menu to `Managed applications`
- Click the `pacman` Application name.
- View the Topology
- Click the `Route` nodes to obtain the Pac-man URL
- Click the URL to see a Red Hat landing page with nginx version

### Changing the background colour
- In Github, using your fork of this repository, edit the `./pacman/deployment.yaml` and **change** the image tag from `latest` to `green`
- Commit your change
- Within 60s the background of the Pac-man board will change to green (don't forget to refresh your browser)
- The demo is ready to be run again
