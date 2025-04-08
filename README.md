# k8s_Bouncer – Minimal Kubernetes Admission Webhook

k8s_Bouncer is a lightweight admission webhook server for Kubernetes, implemented in Python using Flask. It is intended to be used with Kubernetes' `ImagePolicyWebhook` and `ValidatingAdmissionWebhook` admission plugins to validate or deny Kubernetes API requests based on custom logic.

This project provides a simple example of how to build, deploy, and integrate a webhook server into a Kubernetes cluster with proper TLS and admission configurations.

---

## Features

- Compatible with Kubernetes admission plugins: `ImagePolicyWebhook` and `ValidatingAdmissionWebhook`
- Customizable logic in Python
- HTTPS with support for manually generated TLS certificates
- Designed to run as a Deployment within a Kubernetes cluster

---

## Project Structure

```
.
├── Dockerfile                      # Docker image definition
├── README.md                       # This file
├── app
│   └── requirements.txt            # Python dependencies
│   └── app.py                      # Flask-based webhook server
└── k8s_resources
    ├── deployment.yaml             # Deployment manifest
    └── service.yaml                # Service manifest
```

---

## Prerequisites

- A self-managed Kubernetes cluster with access to the kube-apiserver's configuration
- TLS certificate and key for securing the webhook endpoint
- `ImagePolicyWebhook` plugin enabled in the API server configuration

---

## Build and Push the Webhook Image

1. Clone the repository:

   ```bash
   git clone https://github.com/geek-kb/k8s_bouncer.git
   cd k8s_bouncer
   ```

2. Build the Docker image:

   ```bash
   docker build -t your-dockerhub-username/bouncer:latest .
   ```

3. Push the image to your container registry:

   ```bash
   docker push your-dockerhub-username/bouncer:latest
   ```

---

## Deploying to Kubernetes

1. Create a TLS secret (replace with your actual certificate and key):

   ```bash
   kubectl create secret tls bouncer-tls \
     --cert=path/to/tls.crt \
     --key=path/to/tls.key \
     -n bouncer
   ```

2. Apply the Deployment and Service manifests:

   ```bash
   kubectl apply -f k8s_resources/
   ```

---

## Example API Server Configuration

The following configuration is required on the API server to enable image policy validation:

### `admission-config.yaml`

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: ImagePolicyWebhook
    configuration:
      imagePolicy:
        kubeConfigFile: "/etc/kubernetes/image-policy/kubeconfig"
        allowTTL: 50
        denyTTL: 50
        retryBackoff: 500
        defaultAllow: false
```

### Kube-apiserver Flags

Ensure the API server is launched with the following flags:

```
--enable-admission-plugins=ImagePolicyWebhook
--admission-control-config-file=/etc/kubernetes/admission-config.yaml
```

This setup is only applicable to self-managed Kubernetes distributions (such as kubeadm or bare metal).

---

## Customizing Logic

The webhook server logic is defined in `app/app.py`. It currently accepts all incoming pod creation requests. You can customize it to inspect images, namespaces, or any other request attribute and decide whether to allow or deny the request.

---

## Testing

You can test the webhook behavior by attempting to create a pod:

```bash
kubectl run test --image=nginx --restart=Never
```

Webhook decisions and activity can be observed via pod logs:

```bash
kubectl logs -l app=bouncer -n bouncer
```

---

## License

This project is released under the MIT License.
