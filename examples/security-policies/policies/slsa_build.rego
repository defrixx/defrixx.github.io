package examples.slsa_build

# Synthetic policy contract only. Verification is trusted verifier output,
# never a claim supplied by an artifact producer. No cryptography is performed.
default allow := false

allow if {
    object.keys(input) == {"verification", "statement"}
    object.keys(input.verification) == {"signature_verified", "issuer", "signer"}
    input.verification.signature_verified == true
    input.verification.issuer == data.configuration.slsa.issuer
    input.verification.signer == data.configuration.slsa.signer
    input.statement._type == "https://in-toto.io/Statement/v1"
    input.statement.predicateType == "https://slsa.dev/provenance/v1"
    is_array(input.statement.subject)
    count(input.statement.subject) == 1
    input.statement.subject[0].digest.sha256 == data.configuration.slsa.sha256
    input.statement.predicate.runDetails.builder.id == data.configuration.slsa.builder
    input.statement.predicate.buildDefinition.buildType == data.configuration.slsa.build_type
    input.statement.predicate.buildDefinition.externalParameters == {
        "source": data.configuration.slsa.source,
        "revision": data.configuration.slsa.revision,
    }
}
