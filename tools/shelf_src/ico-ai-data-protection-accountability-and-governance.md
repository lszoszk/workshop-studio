---
id: ico-ai-data-protection-accountability-and-governance
title: "ICO guidance on AI and data protection: accountability, governance, DPIAs, controllers and processors, third-party AI"
publisher: "UK Information Commissioner's Office (ICO)"
url: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/what-are-the-accountability-and-governance-implications-of-ai/
licence: OGL-3.0
licence_url: https://ico.org.uk/global/copyright-and-re-use-of-materials/
retrieved: 2026-11-02
kind: excerpt
topics: [data-protection, gdpr, dpia, ai-governance, procurement, controller-processor]
---
> Excerpt from "What are the accountability and governance implications of AI?", a chapter of the ICO's "Guidance on AI and data protection". Original: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/what-are-the-accountability-and-governance-implications-of-ai/
> Reuse notice requested by the publisher: Information Commission's Office, What are the accountability and governance implications of AI?, 15 March 2023, licensed under the Open Government Licence. Contains public sector information licensed under the Open Government Licence v3.0.
> Retrieved 2026-11-02 from the Internet Archive copy of the page taken on 21 September 2026, because the live ico.org.uk site refuses automated requests (HTTP 403). Licence confirmed on the ICO page "Copyright and re-use of materials" (https://ico.org.uk/global/copyright-and-re-use-of-materials/), Internet Archive copy of 26 October 2026: all text is under the OGL v3.0 except where stated; images are excluded.
> Trimmed; "[…]" marks cuts. Check the live page before relying on it.

Due to changes made by the Data (Use and Access) Act, this guidance is under review and may be subject to change. The Plans for new and updated guidance page will tell you about which guidance will be updated and when this will happen.

[…]

## At a glance

This section is about the accountability principle, which makes you responsible for complying with data protection law and for demonstrating that compliance in any AI system that processes personal data. A data protection impact assessment (DPIA) is an ideal way to demonstrate your compliance. The section will also explain the importance of identifying and understanding controller/ processor relationships. Finally, it covers striking the required balance between the right to data protection and other fundamental rights in the context of your AI system.

## Who is this section for?

This section is aimed at senior management and those in compliance-focused roles, including DPOs, who are accountable for the governance and data protection risk management of an AI system. There are some terms and techniques described that may require the input of a technical specialist.

[…]

### What do we need to consider when undertaking data protection impact assessments for AI?

DPIAs are a key part of data protection law’s focus on accountability and data protection by design.

You should not see DPIAs as simply a box ticking compliance exercise. They can effectively act as roadmaps for you to identify and control the risks to rights and freedoms that using AI can pose. They are also an ideal opportunity for you to consider and demonstrate your accountability for the decisions you make in the design or procurement of AI systems.

#### Why are DPIAs required under the data protection law?

In the vast majority of cases, the use of AI will involve a type of processing likely to result in a high risk to individuals’ rights and freedoms, and will therefore trigger the legal requirement for you to undertake a DPIA. You will need to make this assessment on a case by case basis. In those cases where you assess that a particular use of AI does not involve high risk processing, you still need to document how you have made this assessment.

If the result of an assessment indicates residual high risk to individuals that you cannot sufficiently reduce, you must consult with the ICO prior to starting the processing.

In addition to conducting a DPIA, you may also be required to undertake other kinds of impact assessments or do so voluntarily. For example, public sector organisations are required to undertake equality impact assessments, while other organisations voluntarily undertake ‘algorithm impact assessments’. Similarly, the machine learning community has proposed ‘model cards’ and ‘datasheets’ which describe how ML models may perform under different conditions, and the context behind the datasets they are trained on, which may help inform an impact assessment. There is no reason why you cannot combine these exercises, so long as the assessment encompasses all the requirements of a DPIA.

The ICO has produced detailed guidance on DPIAs that explains when they are required and how to complete them. This section sets out some of the things you should think about when carrying out a DPIA for the processing of personal data in AI systems.

#### How do we decide whether to do a DPIA?

We acknowledge that not all uses of AI will involve types of processing that are likely to result in a high risk to rights and freedoms. However, you should note that Article 35(3)(a) of the UK GDPR requires you to undertake a DPIA if your use of AI involves:

- systematic and extensive evaluation of personal aspects based on automated processing, including profiling, on which decisions are made that produce legal or similarly significant effects;
- large-scale processing of special categories of personal data; or
- systematic monitoring of publicly-accessible areas on a large scale.

Beyond this, AI can also involve several processing operations that are themselves likely to result in a high risk, such as use of new technologies or novel application of existing technologies, data matching, invisible processing, and tracking of location or behaviour. When these involve things like evaluation or scoring, systematic monitoring, and large-scale processing, the requirement to do a DPIA is triggered.

In any case, if you have a major project that involves the use of personal data it is also good practice to do a DPIA. Read our list of processing operations ‘likely to result in high risk’ for examples of operations that require a DPIA, and further detail on which criteria are high risk in combination with others.

**Further reading outside this guidance**

See ‘How do we decide whether to do a DPIA?’ in our detailed guidance on DPIAs.

[…]

### How should we understand controller / processor relationships in AI?

#### Why is controllership important for AI systems?

Often, several different organisations will be involved in developing and deploying AI systems which process personal data.

The UK GDPR recognises that not all organisations involved in the processing will have the same degree of control or responsibility. It is important to be able to identify who is acting as a controller, a joint controller or a processor so you understand which UK GDPR obligations apply to which organisation.

#### How do we determine whether we are a controller or a processor?

You should use our existing guidance on controllers and processors to help you with this. This is a complicated area, but some key points from that guidance are:

- You should take the time to assess, and document, the status of each organisation you work with in respect of all the personal data processing activities you carry out.
- If you exercise overall control of the purpose and means of the processing of personal data – you decide what data to process, why and how – you are a controller.
- If you don’t have any purpose of your own for processing the data and you only act on a client’s instructions, you are likely to be a processor – even if you make some technical decisions about how you process the data.
- Organisations that determine the purposes and means of processing will be controllers regardless of how they are described in any contract about processing services.

As AI usually involves processing personal data in several different phases or for several different purposes, it is possible that you may be a controller or joint controller for some phases or purposes, and a processor for others.

[…]

#### Outsourcing and third-party AI systems

When you either buy an AI solution from a third party, or outsource it altogether, you need to conduct an independent evaluation of any trade-offs as part of your due diligence process. You are also required to specify your requirements at the procurement stage, rather than addressing trade-offs afterwards.

Recital 78 of the UK GDPR says producers of AI solutions should be encouraged to:

- take into account the right to data protection when developing and designing their systems; and
- make sure that controllers and processors are able to fulfil their data protection obligations.

You should ensure that any system you procure aligns with what you consider to be the appropriate trade-offs. If you are unable to assess whether the use of a third party solution would be data protection compliant, then you should, as a matter of good practice, opt for a different solution. Since new risks and compliance considerations may arise during the course of the deployment, you should regularly review any outsourced services and be able to modify them or switch to another provider if their use is no longer compliant in your circumstances.

For example, a vendor may offer a CV screening tool which effectively scores promising job candidates but may ostensibly require a lot of information about each candidate to assist with the assessment. If you are procuring such a system, you need to consider whether you can justify collecting so much personal data from candidates, and if not, request the provider modify their system or seek another provider.
