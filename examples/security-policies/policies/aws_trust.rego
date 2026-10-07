package examples.aws_trust

# Deliberately accepts one exact GitHub branch federation profile.
default allow := false

allow if {
    object.keys(input) == {"Version", "Statement"}
    input.Version == "2012-10-17"
    is_array(input.Statement)
    count(input.Statement) == 1
    statement := input.Statement[0]
    object.keys(statement) == {"Effect", "Principal", "Action", "Condition"}
    statement.Effect == "Allow"
    statement.Principal == {"Federated": data.configuration.aws_provider}
    statement.Action == "sts:AssumeRoleWithWebIdentity"
    statement.Condition == {"StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": data.configuration.github_subject,
    }}
}
