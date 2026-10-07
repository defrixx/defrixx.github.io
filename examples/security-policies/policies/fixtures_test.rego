package examples.tests

import data.examples.pod
import data.examples.aws_trust

# An unknown policy name remains false and fails an expected-allow case.
default decision(_) := false

decision(case) := pod.allow if {
    case.policy == "pod"
} else := aws_trust.allow if {
    case.policy == "aws_trust"
}

test_fixture_cases[name] if {
    some case in data.fixtures.cases
    name := case.name
    actual := decision(case) with input as case.input
    actual == case.allowed
}
