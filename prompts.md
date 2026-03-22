# Prompts

## 2026-03-22

Please add following:

- please always create a plan and test plan for new features in docs/plans
- please always create unit tests
- please after completion of a feauture (with a test plan) create a separate pass where you analyse the tests, quality, readability and reliability of the code and the test, please write this analysis as a last part of the plan the code

Please move both files into iiko-api-sample.
This will be our working directory for this project.

We are planning to create a set of scripts. Each script is a tool that does one thing using iiko-api. Each tool will become a command line script. When we debug couple of scripts we will create mcp server where these scripts become pbulished tools of mcp server. Please detect and collect common functionality into the shared lib. For each script please create a skill in skill directory - the skill will describe what and how we were doing it.
Each new script is a feature.
First 2 tools:

- create new guest (add guest - with checking if it already exists etc)
- check balance by the track number

Please describe what you will do in a plan.

Please add following rule to Agents.md:

- duplicate all documentation in English and Russian in separate doc files. Keep them in sync. For Readme.md files keep 2 separate sections (do not duplicate Readme,md files).

After that please continue with refining open questions and start implementing Task 2 from the plan.

what other parameters guest can have?

Please put priority to the https://api-ru.iiko.seevices over the go library, we suspect that go lib might be outdated, for example 
consentStatus and shouldReceivePromoActionsInfo for marketing/consent state iiko package - github.com/themgmd/iiko-go - Go Packages
and
referrerId and userData for integration-specific metadata iiko package - github.com/themgmd/iiko-go - Go Packages
is not look familiar

let's continue
