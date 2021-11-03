# Application for Istio Multicluster Service Mesh

The home for istio multicluster service mesh Applications, based on the open-clutser-management.io Subscription, Channel and Placement API

## Prerequisites

- Red Hat Advanced Cluster Management for Kubernetes v2.3+ is installed
- Create managedclusterset named `mcsm` and enable `submariner-addon` for the connected clusters(`local-cluster`, `mcsmtest1` and `mcsmtest1`).
- Add `anyuid` SCC to the service accounts in `istio-operator` `istio-system` and `istio-apps` namespaces for the connected clusters by the following commands:

  ```
  oc adm policy add-scc-to-group anyuid system:serviceaccounts:istio-operator
  oc adm policy add-scc-to-group anyuid system:serviceaccounts:istio-system
  oc adm policy add-scc-to-group anyuid system:serviceaccounts:istio-apps
  ```

# Usage

1. Install istio operator by deploying the `istio-operator` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-operator
```

2. Install the istio control plane in hub cluster by deploying the `istio-multicluster-hub` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-multicluster-hub
```

3. Install the istio remote control plane configurations in managed clusters by deploying the `istio-multicluster-remote` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-multicluster-remote
```

4. Create remote secret for the central plane to access kube-apiserver of the managedclusters(`mcsmtest1` and `mcsmtest2`):

> Note: make sure export the following three environment variables `CTX_HUB_CLUSTER`, `CTX_MC1_CLUSTER` and `CTX_MC2_CLUSTER` be the kubernetes context of the connected clusters.

```
ISTIO_READER_SRT_NAME_FOR_MC1=$(oc --context=${CTX_MC1_CLUSTER} -n istio-system get serviceaccount/istiod -o jsonpath='{.secrets}' | jq -r '.[] | select(.name | test ("istiod-token-")).name')
istioctl x create-remote-secret --context=${CTX_MC1_CLUSTER} --name=${MC1_CLUSTER_NAME} --type=remote \
    --namespace=istio-system --service-account=istiod --secret-name=${ISTIO_READER_SRT_NAME_FOR_MC1} \
    --create-service-account=false | oc --context=${CTX_HUB_CLUSTER} apply -f -

ISTIO_READER_SRT_NAME_FOR_MC2=$(oc --context=${CTX_MC2_CLUSTER} -n istio-system get serviceaccount/istiod -o jsonpath='{.secrets}' | jq -r '.[] | select(.name | test ("istiod-token-")).name')
istioctl x create-remote-secret --context=${CTX_MC2_CLUSTER} --name=${MC2_CLUSTER_NAME} --type=remote \
    --namespace=istio-system --service-account=istiod --secret-name=${ISTIO_READER_SRT_NAME_FOR_MC2} \
    --create-service-account=false | oc --context=${CTX_HUB_CLUSTER} apply -f -
```

5. Patch the kube-apiserver of the managedclusters(`mcsmtest1` and `mcsmtest2`) due to a submariner [known issue](https://github.com/submariner-io/submariner/issues/1421).

6. Install the istio ingressgateway in managed cluster `mcsmtest1` by deploying the `istio-gateway` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-gateway
```

7. Install the `bookinfo` application by deploying the `bookinfo` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/bookinfo
```

8. Access the bookinfo application with your browser via the route of the istio ingressgateway.
