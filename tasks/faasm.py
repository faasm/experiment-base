from invoke import task
from subprocess import check_output
from tasks.util.net import get_k8s_service_ip, do_post
import time

UPLOAD_PORT=8002
INVOKE_PORT=80

def get_faasm_invoke_host_port():
    host = get_k8s_service_ip("istio-system", "istio-ingressgateway")
    port = INVOKE_PORT
    return host, port


def get_knative_headers(service_name):
    cmd = "kn service describe faasm-{} -o url -n faasm".format(service_name)
    url = check_output(cmd, shell=True).decode("utf-8").strip()[7:]
    print(url)
    return {"Host": "{}".format(url)}


@task
def invoke(ctx, user, func, debug=False, time=False):
    """
    Invoke a function execution in the faasm runtime with knative
    """
    host, port = get_faasm_invoke_host_port()
    url = "http://{}".format(host)

    headers = get_knative_headers("worker")
    print(headers)

    msg = {
        "user": user,
        "function": func,
        "async": False,
    }

    return do_post(url, msg, headers=headers, json=True, debug=debug)
