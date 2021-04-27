# Managed your secrets in Red Hat ACM

## Problem
How do I define secrets in my ACM hub cluster and securly distribute them to my managed clusters?

## Solution
Red Hat ACM Namespace channel has a special secret feature.  This takes a secret from the namespace you define for the channel and delivers it as a secret to the managed-clusters matching the placement rule.

## The pieces
### app.yaml
This defines the Application object that groups all the subscriptions you want to use to distribute your secrets together.

### channel.yaml
This defines a namespace `my-secrets-ch` where you are exptect to create the secrets you want to distrbute.  The channel name will be `my-secret`, so the channel path you define in the subscription is `NAMESPACE/SECRET` or `my-secrets-ch/my-secret`.

### placement.yaml
This defines the target clusters where you want your secret(s) delivered. You can have one placement rule or many.  Placement rules can be shared between subscriptions.  You can modify the labelSelector or the MatchExpression to define the target clusters.

### namespace.yaml
This defines the `my-secret-ch` namespace for the channel and `my-secret` namespace where the example subscription will be created.

### subscription.yaml
This defines a subscription. It has a reference to the `my-secret-ch/my-secret` channel. It also has a `placementRef` that points to the placement rule. By default a subscription will pull all secrets in the channel. So if you want to limit a subscription to specific secrets you create the channel namespace `my-secret-ch` you would add an annotation to the actual YAML secret created in the `my-secret-ch` namespace.

In the subscription to choose a secret by annotation use:
```yaml
  packageFilter:
    annotations:
      secretname: my-secret
```
Any secret with the metadata.annotations.`secretname`: `my-secret` will be delivered to the clusters defined in the placement rule the subscription references. 

### secret.yaml
Define one or more secrets to apply the channel namespace `my-secret-ch`. You need to include the following annotation always: 
```yaml
metadata:
  annotations:
    apps.open-cluster-management.io/deployables: "secret"
    secretname: my-secret    # This is an optional filter, that just needs to match the
                             # subscrpition packageFilter mentioned above.
```

### Note
The key to remember, to have your secrets in the Hub channel delivered, they need the `aps.open-cluster-management.io/deployables` annotation, and optionally additional annotations for filtering secrets for delivery.
