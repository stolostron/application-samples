# Application for Istio Multicluster Service Mesh

The home for istio multicluster service mesh Applications, based on the open-clutser-management.io Subscription, Channel and Placement API

## Requirements

- `open-cluster-management.io` or Red Hat Advanced Cluster Management for Kubernetes v2.3+
- `submariner-addon` enabled for the connected clusters(`local-cluster`, `mcsdemo1` and `mcsdemo2`) in the mesh in managedclusterset named `mcsm-demo`.

# How to use

1. Replace the `<istio-chart-repository-url>` in `subscriptions/istio-multicluster-servicemesh/istio-operator/channel.yaml` and then deploy the `istio-operator` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-operator
```

> Note: this is broken now, please use `istio-operator` helm chart to install it in each clusters.

2. Deploy the `istio-multicluster` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/istio-multicluster
```

3. Create remote secret for the central plane to access kube-apiserver of the managedclusters(`mcsdemo1` and `mcsdemo2`):

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

4. Patch the kube-apiserver of the managedclusters(`mcsdemo1` and `mcsdemo2`) due to a submariner [known issue](https://github.com/submariner-io/submariner/issues/1421).

5. Create `istio-apps` namespace in in managedclusters(`mcsdemo1` and `mcsdemo2`) with istio sidecar injection label and also create `networkattachmentdefinition` for istio-cni.

```
oc --context=${CTX_MC1_CLUSTER} create ns istio-apps
oc --context=${CTX_MC1_CLUSTER} label ns istio-apps istio-injection=enabled

oc --context=${CTX_MC2_CLUSTER} create ns istio-apps
oc --context=${CTX_MC2_CLUSTER} label ns istio-apps istio-injection=enabled

cat <<EOF > istio-cni-NetworkAttachmentDefinition.yaml
apiVersion: "k8s.cni.cncf.io/v1"
kind: NetworkAttachmentDefinition
metadata:
  name: istio-cni
EOF

oc --context=${CTX_MC1_CLUSTER} -n istio-apps apply -f istio-cni-NetworkAttachmentDefinition.yaml
oc --context=${CTX_MC2_CLUSTER} -n istio-apps apply -f istio-cni-NetworkAttachmentDefinition.yaml

oc --context=${CTX_MC1_CLUSTER} adm policy add-scc-to-group anyuid system:serviceaccounts:istio-apps
oc --context=${CTX_MC2_CLUSTER} adm policy add-scc-to-group anyuid system:serviceaccounts:istio-apps
```

> Note: this step is just workaround and will not be needed in future.

6. Deploy the `bookinfo` Application:

```
oc apply -k subscriptions/istio-multicluster-servicemesh/bookinfo
```

7. Apply the `bookinfo-gateway` in Hub cluster and access the bookinfo from the following URL:

```
oc --context=${CTX_MC1_CLUSTER} -n istio-apps apply -f 1-bookinfo-gateway
GATEWAY_URL=$(oc --context=${CTX_MC1_CLUSTER} -n istio-apps get route ingressgateway -o jsonpath="{.spec.host}")
echo "http://${GATEWAY_URL}/productpage"
```

8. Then you can deploy the istio configuration under `[1-6]-bookinfo-*` directories to validate the istio functions.

> Note: the number prefix is the apply order.
