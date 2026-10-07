package examples.pod

# Narrow stateless Linux Pod profile, not a replacement for Pod Security Admission.
default allow := false

allow if {
    object.keys(input) == {"apiVersion", "kind", "metadata", "spec"}
    input.apiVersion == "v1"
    input.kind == "Pod"
    object.keys(input.metadata) == {"name", "namespace"}
    is_string(input.metadata.name)
    input.metadata.name != ""
    input.metadata.namespace == data.configuration.namespace
    input.spec.serviceAccountName == data.configuration.service_account
    input.spec.automountServiceAccountToken == false
    count(object.keys(input.spec) - {"serviceAccountName", "automountServiceAccountToken", "securityContext", "containers", "initContainers", "hostNetwork", "hostPID", "hostIPC", "volumes", "os"}) == 0
    object.get(input.spec, "hostNetwork", false) == false
    object.get(input.spec, "hostPID", false) == false
    object.get(input.spec, "hostIPC", false) == false
    object.get(input.spec, "volumes", []) == []
    object.get(input.spec, "os", {"name": "linux"}) == {"name": "linux"}
    input.spec.securityContext == {"runAsNonRoot": true, "seccompProfile": {"type": "RuntimeDefault"}}
    is_array(input.spec.containers)
    count(input.spec.containers) > 0
    every container in input.spec.containers { safe_container(container) }
    init := object.get(input.spec, "initContainers", [])
    is_array(init)
    every container in init { safe_container(container) }
}

safe_container(container) if {
    count(object.keys(container) - {"name", "image", "securityContext", "command", "args"}) == 0
    is_string(container.name)
    container.name != ""
    regex.match("^[a-z0-9][a-z0-9./:_-]*@sha256:[a-f0-9]{64}$", container.image)
    sc := container.securityContext
    count(object.keys(sc) - {"allowPrivilegeEscalation", "readOnlyRootFilesystem", "capabilities", "privileged", "runAsNonRoot", "runAsUser", "seccompProfile"}) == 0
    sc.allowPrivilegeEscalation == false
    sc.readOnlyRootFilesystem == true
    sc.capabilities == {"drop": ["ALL"]}
    object.get(sc, "privileged", false) == false
    object.get(sc, "runAsNonRoot", true) == true
    uid := object.get(sc, "runAsUser", 1)
    is_number(uid)
    uid > 0
    object.get(sc, "seccompProfile", {"type": "RuntimeDefault"}) == {"type": "RuntimeDefault"}
}
