# Observer
## Application Info
Observer takes an unstructured data file as input (like a pdf) and outputs a list of Observation objects. Each observation includes standard fields that are extracted from the document together with metadata like the document name and page number. It is intended to be used as a component in a data processing pipeline.


## Architecture
### Introduction
Observer is packaged as a python module including a script that runs as it's CLI. It expects API credentials to be handled by some other process so it can assume permissions from it's runtime environment to access foundation models on Amazon Bedrock. Observer chunks input data and uses it to prompt FM's and aggregate observations from the data.

See README.md in the project for more details.

https://gitlab.aws.dev/famestad/observer
### Architecture Diagram
![Architecture Diagram](/assets/Observer2.png)

## Dataflow
### Introduction
The tool runs script that can be local or deployed into a cloud runtime as part of a pipeline. 

It reads a local pdf file that was staged by some outside process (ie: manual or a prior step in the pipeline).

Outputs can be written to a local file or to a dynamodb table. When using Amazon DynamoDB, it is assumed that AWS credentials are available in the environment that allow table read/ write access.
### Dataflow Diagram
![Dataflow Diagram](/assets/Observer.png)


## Assumptions


| Assumption Number | Assumption | Linked Threats | Linked Mitigations | Comments |
| --- | --- | --- | --- | --- |
| <a name="A-0003"></a>A-0003 | The tool is targeted to the correct output resources |  | [**M-0002**](#M-0002): README.md shares best practice to use different roles for local testing and automated pipelines to mitigate risk of incorrect target.<br/>[**M-0001**](#M-0001): README.md advises to ensure principal of least access in establishing controls.  |  |
| <a name="A-0002"></a>A-0002 | Access controls for the environment are managed through an outside process. | [**T-0002**](#T-0002): A system user with access to multiple environments can execute with incorrect credentials, which leads to unintended table updates, negatively impacting reliability of system data |  |  |
| <a name="A-0001"></a>A-0001 | The application will assume privileges from it's environment. | [**T-0001**](#T-0001): An authorized actor with access to the aws account can craft a malicious pdf, which leads to unintended behavior, negatively impacting stability of the system |  | <p>A local user can use temporary credentials to invoke the script. Deployed to AWS, an IAM role can be assigned to the compute instance.</p> |
| <a name="A-0004"></a>A-0004 | Access to add or update questions is limited to resources with a business need | [**T-0003**](#T-0003): A malicious actor who can add new questions to the prompts can inject a prompt attach, which leads to unintended outputs, negatively impacting reliability of system data |  |  |


## Threats


| Threat Number | Threat | Mitigations | Assumptions | Status | Priority | STRIDE | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <a name="T-0003"></a>T-0003 | A malicious actor who can add new questions to the prompts can inject a prompt attach, which leads to unintended outputs, negatively impacting reliability of system data | [**M-0001**](#M-0001): README.md advises to ensure principal of least access in establishing controls.  | [**A-0004**](#A-0004): Access to add or update questions is limited to resources with a business need |  Identified |  |  |  |
| <a name="T-0002"></a>T-0002 | A system user with access to multiple environments can execute with incorrect credentials, which leads to unintended table updates, negatively impacting reliability of system data | [**M-0002**](#M-0002): README.md shares best practice to use different roles for local testing and automated pipelines to mitigate risk of incorrect target. | [**A-0002**](#A-0002): Access controls for the environment are managed through an outside process. |  Identified |  |  |  |
| <a name="T-0001"></a>T-0001 | An authorized actor with access to the aws account can craft a malicious pdf, which leads to unintended behavior, negatively impacting stability of the system | [**M-0001**](#M-0001): README.md advises to ensure principal of least access in establishing controls.  | [**A-0001**](#A-0001): The application will assume privileges from it's environment. |  Identified |  |  |  |


## Mitigations


| Mitigation Number | Mitigation | Threats Mitigating | Assumptions | Status | Comments |
| --- | --- | --- | --- | --- | --- |
| <a name="M-0003"></a>M-0003 | Prompt includes html tags to delineate input from prompt template with instructions for how to use the provided inputs. |  |  | Identified |  |
| <a name="M-0002"></a>M-0002 | README.md shares best practice to use different roles for local testing and automated pipelines to mitigate risk of incorrect target. | [**T-0002**](#T-0002): A system user with access to multiple environments can execute with incorrect credentials, which leads to unintended table updates, negatively impacting reliability of system data | [**A-0003**](#A-0003): The tool is targeted to the correct output resources | Identified |  |
| <a name="M-0001"></a>M-0001 | README.md advises to ensure principal of least access in establishing controls.  | [**T-0001**](#T-0001): An authorized actor with access to the aws account can craft a malicious pdf, which leads to unintended behavior, negatively impacting stability of the system<br/>[**T-0003**](#T-0003): A malicious actor who can add new questions to the prompts can inject a prompt attach, which leads to unintended outputs, negatively impacting reliability of system data | [**A-0003**](#A-0003): The tool is targeted to the correct output resources | Identified |  |


## Impacted Assets


| Assets Number | Asset | Related Threats |
| --- | --- | --- |
| AS-0001 | reliability of system data | [**T-0003**](#T-0003): A malicious actor who can add new questions to the prompts can inject a prompt attach, which leads to unintended outputs, negatively impacting reliability of system data<br/>[**T-0002**](#T-0002): A system user with access to multiple environments can execute with incorrect credentials, which leads to unintended table updates, negatively impacting reliability of system data |
| AS-0002 | stability of the system | [**T-0001**](#T-0001): An authorized actor with access to the aws account can craft a malicious pdf, which leads to unintended behavior, negatively impacting stability of the system |

