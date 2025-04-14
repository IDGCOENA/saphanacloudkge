# SAP HANACloud Knowledge Graph Engine(KGE)
THis code repository contains the python scripts for different scenarios discussed in Discovery Mission "Building Intelligent Data Applications with SAP HANA Cloud Knowledge Graphs"

# KGE_Mission

**Pre-requisites:**

1. SAP Generative Hub subscription has been set up, and the AICORE tokens are stored locally. If not, please follow these steps for:
   - [Initial setup](https://help.sap.com/docs/ai-launchpad/sap-ai-launchpad/initial-setup?q=generative%20ai%20hub) 
   - Setting up [roles](https://help.sap.com/docs/ai-launchpad/sap-ai-launchpad/activate-generative-ai-hub-for-sap-ai-launchpad?q=generative%20ai%20hub&locale=en-US)

**Please note GenAI Hub will be used only for KGE retrieval scenarios and NOT for generating KGs. In order to Generate KGs, please subscribe to Azure OpenAI(GPT4o) or AWS Bedrock
  (Anthropic Claude 3.7 Sonnet).**
   
   
2. To **generate KGs, you need to set up Azure Open AI/AWS Bedrock** and execute the scripts. For additional information, please refer to the "SET UP" Tiles in the 
   Discovery Mission.
                     
3. SAP HANA CLoud Instance has been set up by following these [steps](https://developers.sap.com/tutorials/hana-cloud-deploying.html).

4. All the Python scripts have been validated using Google Colabs. Either set up local python environment has been set up or use [Google Colabs](https://colab.research.google.com/) to execute the python scripts. **If you are using Visual Studio or your local Python environments, please make sure you set up a separate virtual environment as the necessary packages might conflict with existing installed version**
5. Install the Python Package for [Generative AI Hub - SDK](https://pypi.org/project/generative-ai-hub-sdk/). 
6. If you are using GenAI hub, configure the ai-core-sdk using the ai-core instance keys. If you are using Microsoft Visual Studio, then you can execute "aicore            configure" from terminal. Incase you are using Google Colab, you can set up using 
* os.environ['AICORE_AUTH_URL'] = 'https://*************.authentication.eu10.hana.ondemand.com'
* os.environ['AICORE_CLIENT_ID'] = 'sb-************************'
* os.environ['AICORE_RESOURCE_GROUP'] = 'default'
* os.environ['AICORE_CLIENT_SECRET'] = 'df********************************GfCt1g='
* os.environ['AICORE_BASE_URL'] = 'https://******************entral-1.aws.ml.hana.ondemand.com/v2'
* os.environ['HANA_VECTOR_USER'] = 'XXXXXXXXXX'   --> Your SAP HANA Cloud User
* os.environ['HANA_VECTOR_PASS'] = 'XXXXXXXXXXXXXXX' --> Your SAP HANA Cloud password 
* os.environ['HANA_HOST_VECTOR'] = 'XXXXXXXXXXXXXXXXXXXXX-eu10.hanacloud.ondemand.com'   --> Your SAP HANA Cloud host          
8. Install the python packages as mentioned in the Python Scripts
9. Setting up the .env file so you dont have to hardcode the credentials for accessing SAP HANA Cloud(Optional)


**Executing the Python Scripts**
           
1. There are 6 scenarios for python scripts provided as mentioned in the Implementation Review of the Discovery Mission. For executing scenarios [1,2,4,5], you need to setup up SAP HANA Cloud and SAP GenAI HuB
2. For executing scenarios 3 and 6, you need to setup up SAP HANA Cloud and Azure OpenAI/OpenAI
3. For Scenario 7 which is the CAP app for RAG based, the code is provided both for how to execute using GenAI Hub or Azure OpenAI.


| Scenarios | Description | GenAI Hub  |  AzureOpenAI/AWS Bedrock | SAP HANA Cloud 
| :---         |     :---:      |          ---: |           ---:   | ---: |
| Scenario1    | Transform unstructured PDF documents into semantic knowledge graphs using Python with Azure OpenAI's GPT-4o. The process extracts entities and relationships from documents, converts them to RDF triples, and visualizes the semantic connections between concepts in the original content.|    | X | 
| Scenario2     |Continuing from Scenario 1's triple generation, we'll now load these semantic triples into SAP HANA Cloud using SPARQL. Once imported, you can view and interact with the triples directly through the Database Explorer interface.|     |   | X
| Scenario3    | Transform unstructured PDF documents into semantic knowledge graphs using Python with AWS Bedrock's Anthropic Claude 3.7 Sonnet. The process extracts entities and relationships from documents, converts them to RDF triples, and visualizes the semantic connections between concepts in the original content. The generated triples are later ingested into SAP HANA Cloud.Once imported, you can view and interact with the triples directly through the Database Explorer interface.|    |  X  | X
| Scenario4    | Query semantic triples in SAP HANA Cloud using natural language. The system converts user queries into SPARQL commands, executes them against the database, and enhances results through Anthropic Claude (AWS Bedrock) processing before presenting refined insights to business users.|   |  X | 
| Scenario5   | Query semantic triples in SAP HANA Cloud using natural language. The system converts user queries into SPARQL commands, executes them against the database, and enhances results through GenAI Hub(Anthropic Claude)processing before presenting refined insights to business users| X |  | 
| Scenario6   | In this scenario, we process Tabular KGs.We process tabular data from SFLIGHT schema's SBOOK and SCUSTOM tables by generating a semantic ontology in turtle(ttl) format. The generated ttl file is ingested as KG in SAP HANA Cloud. We have also provide the code to load the ttl file in to S3 Cloud Storage using Python.And to load the file from S3 into SAP HANA Cloud using Import from DB Explorer. This approach can be extended to Calculative Views metadata or OData structures for advanced scenarios.|    |  | X
| Scenario7    | Retrieval augmented generation (RAG) Application based on SAP CAP to test ingested data from Scenarios 1-4|  X  |  X




4. Please make sure you have access to Large Language Models(LLM) either through 1.GenAI Hub or 2.Azure OpenAI or 3.OpenAI.
5. In order to set up the LLM access, please refer the SetUp section of the mission.
6. Please make sure you import the schema provided as part of the mission. It is available as part of SetUp section under the tile "Setup Data Access for Embedding"
7. Once the SAP HANA Cloud, access to LLM, and Schema, you can execute the scripts seamlessly. 

