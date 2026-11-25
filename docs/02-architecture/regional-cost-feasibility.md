# IMP-001 — Regional and cost feasibility (initial desk review)

Date: 2026-11-25 | Status: partial evidence; open #8; no AWS account access, paid deployment or inference.

| Capability | Published evidence | Remaining gate |
|---|---|---|
| AgentCore Runtime microVMs / Gateway / Observability | AWS regional matrix lists Canada Central support | Verify account limits, runtime/SDK, IAM, MCP target and actual checkpoint integration with synthetic authorized sandbox later |
| Bedrock Runtime API | ca-central-1 supported | Select actual model by eval; check model-level in-region support and processing paths; do not silently use global/cross-region profiles for private data |
| AgentCore Policy | Regional support listed but AWS documents global cross-region inference from Canada Central | Do not send private content through this feature without reviewed residency and privacy evidence; deterministic authorization mandatory |
| Managed AgentCore Web Search Tool/API | Regional matrix does not list Canada Central support | Select a separately permitted provider with cost/terms/privacy review; mock source until then |
| Lambda Python 3.13 / CDK runtime constant | Publicly documented | Verify artifact dependency compatibility and complete service/CDK limits in later validation |
| DynamoDB PITR | Table deletion while enabled creates 35-day system backup | Maximum 30-day requirement unchanged; prove compliant alternative or remain blocked for real private data |
| Signed document URLs | Design requires immediate revocation | Test already issued links/version-specific denial and concurrent requests; expiry alone is not sufficient |

## Cost envelope

Reference 40 searches and 30 application preparations/month. Approved targets USD 0.25 and USD 0.50 per respective run: USD 25 variable allowance and USD 25 shared allowance, total USD 50. This is not a vendor price estimate. AgentCore consumption charges, Gateway calls, Bedrock tokens, search fees, API/Lambda, DynamoDB, storage, backup, telemetry, ECR, transfer and applicable taxes must be priced using concrete chosen model/tool and regional rates. Free tier not assumed. Model, licensed search provider and usage are not selected/measured, so cannot certify feasibility. Record units and actual rates before authorizing a synthetic paid sandbox. No budget exception. Local mocks do not incur AWS charges.

Sources: [AgentCore regional matrix](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html), [Bedrock endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints-region-availability.html), [model regional availability](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html), [cross-region processing](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/cross-region-inference.html), [AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/), [Lambda runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html), [CDK runtime](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Runtime.html), [PITR](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery_Howitworks.html). Reviewed 2026-11-25; verify again before deployment.
