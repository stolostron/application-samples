# Demonstrate development to production promotion process
## Tool Requirements
- OpenShift CLI Version >= 4.3.0<br>_Needed for kustomize_
```bash
oc version
```

## Summary
Demonstrate promoting a new version of nginx from development to production

## Prerequisite
- 2x managed-clusters total
  - One Managed-Cluster with the `metadata.labels.usage: development`
  - One Managed-Cluster with the `metadata.labels.usage: production`
- A fork of this repository

## Application Console: Create a new subscription
Using the application console, you can easily create an Application that runs nginx on two different clusters and each nginx is a different version (development & production). You can then update the development nginx version to production, using a Git merge.

#### Console
1. Open the Red Hat Advanced Cluster Management for Kubernetes console
1. Navigate on the left navigation menu to `Managed applications`
2. Choose `Create application`
3. Enter the following values:
  * **Name:** `nginx`
  * **Namespace:** `nginx`
  * **Repository types** `Git`
  * **URL** `https://github.com/REPO_FORK_NAME/application-samples.git`
  * **Branch** `main`
  * **Path** `nginx`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name** `usage`
  * **Label value** `development`
4. Select `Add another repository`
  * **Repository types** `Git`
  * **URL** `https://github.com/REPO_FORK_NAME/application-samples.git`
  * **Branch** `production`
  * **Path** `nginx`
  * Select `Deploy application resources only on clusters matching specified labels`
  * **Label name** `usage`
  * **Label value** `production`
5. Click `Save`

### Viewing
- Navigate on the left navigation menu to `Managed applications`
- Click the `nginx-placement` Application name.
- View the Topology
- Click the `Route` nodes to obtain the nginx URL
- Click the URL to see a Red Hat landing page with nginx version

### Upgrading the production with the version running in development
- In Github, using your fork of this repository, create a Pull request to merge the contents of the `main` branch into the `production` branch
- This is also where branch control can be introduced, to limit who can approve a merge to the `production` branch
- Complete the merge
- After 60s the production deployment of the nginx application will have updated. Open the Red Hat landing page via the route and refresh the page to override the browser cache

### Reseting the demo
- In Github, using your fork of this repository, edit the `./nginx/deployment.yaml` and set the `image:` version back to `14.1` from `16.1`
- Commit your change
- Within 60s the production nginx will revert to the 14.1 image
- The demo is ready to be run again
