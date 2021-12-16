# RBD demo application with dashboard

## Prepare your demo
Fork my repo at `https://github.com/jeanchlopez/application-samples`

```
git clone https://github.com/{username}/application-samples
cd application-samples
git checkout ramendemo
git fetch
git pull
```

## Deploying MySQL Server

In ACM create new application

- Name = `ramendemo-mysql`
- Namespace = `ramendemo-mysql`
- Git = `https://github.com/{username}/application-samples`
- Branch = `ramendemo`
- Path = `ramendemo/mysql`

Deploy to local cluster

## Deploying Grafana dashboard

Due to an issue with the Grafana operator (`https://github.com/grafana-operator/grafana-operator/issues/655`)
the dashboard can not be configured via ACM.

You will have to deploy the Grafana dashboard in the same namespace as the one where the MySQl server was deployed.

```
cd grafana
oc project ramendemo-mysql
Deploy the Grafana operator
oc create -f ./operator.yaml
```

Wait for the operator to be deployed with an oc get csv -n mysql command

Once the operator is deployed, customize the operator

```
oc create -k .
```

Wait for the Grafana pod to restart. If you need to connect with admin privilege use the following credentials.

- User name = `admin`
- Password = `ramendemo`

Do an `oc get route -n ramendemo-mysql` to check where to reach the Grafana UI

## Configure MySQl address for test application

Update the `rbdloop.yaml` with parameters matching your environment

```
cd ../app
cat rbdloop.yaml
[…]
      - name: SQL_SERVER
        value: "ramendemo-mysql-mysql.apps.makestoragegreatagain.com"
      - name: SQL_PORT
        value: "30136"
#      - name: SQL_URL
#        value: "https://gist.githubusercontent.com/jeanchlopez/0cdd2a30562b735c3bb384bd734282b7/raw/c5d79fbe37fb6e243908a88bee4e66f7d692003e/sqlserver.url”
[…]
```

### Option 1

Your environment always uses the same base domain and you use the default `./mysql/mysql.kustomization.yaml` from this repo.

Change the value for the `SQL_SERVER` environment variable value that matches your name space and your base domain.

e.g. You have deployed with ACM the MySQL server

- Namespace = mysqljc
- Base domain = ocstraining.com

You would set the `SQL_SERVER` value to `ramendemo-mysql-mysqljc.apps.ocstraining.com`.

### Option 2

You have a `gist` available with the MySQL Server address. The URL must point to a raw gist.

Verify the path to your raw gist like this

```
curl https://gist.githubusercontent.com/jeanchlopez/0cdd2a30562b735c3bb384bd734282b7/raw/c5d79fbe37fb6e243908a88bee4e66f7d692003e/sqlserver.url
ramendemo-mysql-mysql.apps.perf3.chris.ocs.ninja:30136
```

Remove the comment in front of the `SQL_URL` environment variable.

e.g. 

```
      - name: SQL_URL
        value: "https://gist.githubusercontent.com/jeanchlopez/0cdd2a30562b735c3bb384bd734282b7/raw/c5d79fbe37fb6e243908a88bee4e66f7d692003e/sqlserver.url”
```

Update your `gist` with the correct MySQL server address (Remember that this repo configures port 30136 by default for the MySQL DB so just change the FQDN

## Deploy the app

In ACM create new application

- Name = `{Your Choice}`
- Namespace = `{Your Choice}`
- Git = `https://github.com/{username}/application-samples`
- Branch = `ramendemo`
- Path = `ramendemo/app`

