# RBD demo application with dashboard

## Prepare your demo
Fork my repo at `https://github.com/jeanchlopez/application-samples`.

```
git clone https://github.com/{username}/application-samples
cd application-samples
git checkout ramendemo
git fetch
git pull
```
Create a new project on OpenShift cluster with ACM installed:

```
oc new-project ramendemo-mysql
```

## Deploying MySQL Server

In ACM create new application:

- Name = `ramendemo-mysql`
- Namespace = `ramendemo-mysql`
- Git = `https://github.com/{username}/application-samples`
- Branch = `ramendemo`
- Path = `ramendemo/mysql`
- `Deploy on local cluster`

## Deploying Grafana dashboard

Due to an issue with the Grafana operator (`https://github.com/grafana-operator/grafana-operator/issues/655`)
the dashboard can not be configured via ACM.

You will have to deploy the Grafana dashboard in the same namespace as the one where the MySQl server was deployed.
```
cd ramendemo/grafana
oc project ramendemo-mysql
```

Deploy the Grafana operator:

```
oc create -f operator.yaml
```

Wait for the operator to be deployed and show a `Succeeded` Phase.

```
oc get csv -n ramendemo-mysql
```

Example output:

```
NAME                                   DISPLAY                         VERSION   REPLACES                               PHASE
grafana-operator.v4.1.1                Grafana Operator                4.1.1     grafana-operator.v4.1.0                Succeeded
```

Once the Grafana operator is deployed, create Grafana resources. Order of yaml files is datasource, next dashboard, then grafana instance.

```
oc create -f grafana-mysql-datasource-for-ramendemo.yaml -n ramendemo-mysql
oc create -f grafana-mysql-dashboard-for-ramendemo.yaml -n ramendemo-mysql
oc create -f grafana-instance.yaml -n ramendemo-mysql
```

Wait for the Grafana pod to restart. If you need to connect with admin privilege use the following credentials.

- User name = `admin`
- Password = `ramendemo`

Do this to find the URL to reach the Grafana UI:

```
oc get route grafana-route in ramendemo-mysql
```

Copy the resulting route into a browser tab to validate you have access to Grafana.

NOTE:  Make sure you sure to use `https` for the Grafana route.

## Configure MySQl address for test application

Update the `rbdloop.yaml` with parameters matching your environment.

To do this find the route for your mysql instance:

```
oc get route ramendemo-mysql -n ramendemo-mysql
```
Use the resulting route to modify `rbdloop.yaml`as shown below (example SQL_SERVER value).

NOTE: Make sure you are in the `ramendemo` directory.

```
cat rbdloop.yaml
[…]
      - name: SQL_SERVER
        value: "ramendemo-mysql-ramendemo-mysql.apps.hub.makestoragegreatagain.com"
      - name: SQL_PORT
        value: "30136"
[…]
```
Now `rbdloop.yaml` needs to be committed to your forked repo.

```
git add rbdloop.yaml
git commit -m "Modified rbdloop.yaml"
git push origin ramendemo
```

## Deploy the application

Create a new project on OpenShift cluster with ACM installed.

```
oc new-project rbdloop-dashboard
```
NOTE: Make sure you are in the `ramendemo` directory.

You now need to create a DRPlacementControl (DRPC)and PlacementRule for the `rbdloop` application.

NOTE: Make sure to modify the DRPC YAML file and modify `cluster1` to be accurate for your environment. Modify to use the cluster name in ACM for your preferredCluster. 

```
oc create -f rbdloop-drpc.yaml -n rbdloop-dashboard
```

Now create the PlacementRule:

```
oc create -f rbdloop-placementrule.yaml -n rbdloop-dashboard
```

In ACM create the new `rbdloop` application.

- Name = `rbdloop`
- Namespace = `rbdloop-dashboard`
- Git = `https://github.com/{username}/application-samples`
- Branch = `ramendemo`
- Path = `ramendemo`
- Select an existing placement configuration = `rbdloop-placement`

Go back to Grafana and navigate to the `Ramen Demo Application Dashboard` to monitor cluster Failover and Relocate operations.
