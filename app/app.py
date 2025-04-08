#!/usr/bin/env python3
from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)


@app.route("/validate", methods=["POST"])
def validate():
    request_json = request.get_json()
    uid = request_json["request"]["uid"]

    # Allow everything (you can add logic here)
    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {"uid": uid, "allowed": True},
    }

    return jsonify(response)


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("/certs/tls.crt", "/certs/tls.key")
    app.run(host="0.0.0.0", port=8443, ssl_context=context)
