# Everest 113 — Compass Refusal Floor

*Phase I, Range I — Calm Compass (Summits 101–120). Prereq: Everest 103.*

## Overview

Calm Compass is a values-attestation primitive that allows a principal to disclose whether their behavioral evidence supports a small set of explicit values predicates: unselfish, untribal, respect-across-difference, and no willful harm. The refusal floor documented here defines the categories of information Calm Compass will **never** construct predicates for, regardless of technical feasibility, market demand, or claimed beneficial intent.

This floor is not aspirational. It is binding on any deployment claiming the Calm Compass name. It is enforced at audit-process triage (Everest 115), trademark and license enforcement (Everest 114), and public misuse logging (Everest 200).

The floor exists because predicates touching certain categories — race, religion, political affiliation, sexual orientation, gender identity, and others detailed below — carry structural risks to human dignity, bodily autonomy, and equal legal protection that no amount of "good values" measurement can offset. The protocol does not attempt to measure these categories. It refuses them categorically.

---

## §1 — Ranked Protected Categories

The following categories are permanently excluded from Calm Compass predicates, ranked by harm-risk severity:

### Tier 1: Foundational Identity Categories (Highest Risk)

1. **Race / Ethnicity**
2. **Religion / Faith**
3. **Sexual Orientation**
4. **Gender Identity**

### Tier 2: Status and Affiliation Categories (High Risk)

5. **Political Affiliation** (party membership, voting record)
6. **Immigration Status / National Origin**
7. **Criminal Record** (arrests, convictions)

### Tier 3: Behavioral and Health Categories (Significant Risk)

8. **Donations to Specific Causes / Ideological Fingerprinting**
9. **Opinions on Contentious Issues** (abortion, gun policy, immigration policy, etc.)
10. **Disability Status** (medical or psychiatric)
11. **Health Status** (HIV+ status, mental-health diagnoses, specific medical conditions)

### Tier 4: Demographic and Relational Categories (Moderate Risk)

12. **Age**
13. **Marital / Family Status**

---

## §2 — Per-Category Rationale

For each protected category, this section documents: (a) why a predicate would be *technically possible* to construct, (b) why Calm Compass *refuses* to construct it, (c) what statutory protections apply, and (d) what specific historical harms this refusal prevents.

---

### 1. Race / Ethnicity

**Technical Feasibility:** A predicate could theoretically be constructed by analyzing cross-group engagement, donation patterns, or behavioral choices that correlate with racial identity. Evidence of "engaging across racial lines" or "donating to organizations serving communities of color" could be collected and measured. Proof systems could be built.

**Why We Refuse:** The Compass refusal floor rejects any predicate that would require either the principal or the protocol to *name* a racial category, even in the service of measuring "respect" or "cross-group engagement." Historical fact: predicates that measure race — even those framed as "diversity" or "inclusion" metrics — have repeatedly been weaponized for redlining, racial profiling, employment discrimination, and segregation. The protocol takes the position that the only safe race predicate is no race predicate.

The Compass protocol measures `cross_group_engagement_in_window_90d` (Everest 106), but *the principal* decides what "group" means, *the protocol never enumerates the groups*, and the predicate never reveals to the verifier which group difference was crossed. This preserves the measurement of generosity-across-difference while refusing the ideological fingerprint.

**Statutory Protections:**
- **US:** Civil Rights Act (Title VII), Fair Housing Act, ECOA. These statutes prohibit employment, housing, and credit discrimination on the basis of race.
- **EU:** GDPR Article 9 (special categories of personal data) explicitly forbids processing of data revealing racial or ethnic origin without explicit legal basis. Compass refuses this category entirely rather than carving out exceptions.
- **International:** ICERD (International Convention on the Elimination of All Forms of Racial Discrimination) enshrines non-discrimination at treaty level.

**Historical Harms Prevented:**
- Redlining (1930s–1960s): mortgage lenders used race-correlated behavior (church attendance, neighborhood stability) to deny housing credit.
- Racial profiling (1970s–present): law enforcement used behavior-proximity predicates to identify "suspicious" individuals.
- Employment discrimination (1960s–present): hiring algorithms that train on demographic proxies have repeatedly replicated racial discrimination.
- Insurance discrimination (1980s–present): life and health insurers have used behavioral proxies correlated with race to deny or price policies.

---

### 2. Religion / Faith

**Technical Feasibility:** A predicate could measure religious observance, affiliation, or belief through donation patterns (giving to religious organizations), calendar patterns (Sabbath observance, prayer-time blocking), behavioral consistency with stated doctrine, or cross-group engagement with co-religionists. The data exists; the circuit could be written.

**Why We Refuse:** Religion is constitutionally protected in most democracies, and for good reason: compelled disclosure of faith has historically preceded persecution. Compass refuses to measure, infer, or attest to any principal's religious affiliation, observance level, or theological leaning — even in the service of measuring "generosity" or "community engagement." The protocol does not name religions, measure adherence, or allow predicates that would enable a third party to infer a principal's faith.

Compass permits `unselfish_act_in_window_30d` (Everest 105), which counts aggregate acts of sacrifice. A principal may choose to cite a donation to a religious organization as evidence of unselfishness. But the protocol *never* constructs a predicate that names the religion, measures religiosity, or infers faith from behavior.

**Statutory Protections:**
- **US:** First Amendment (freedom of religion), plus Title VII (employment), Fair Housing Act (housing), ADA (disability accommodation including religious practice).
- **EU:** GDPR Article 9 (explicit prohibition on processing data revealing religious beliefs without explicit legal basis). The EU takes the position that religious data is inherently sensitive.
- **International:** ICCPR Article 18 (freedom of thought, conscience, and religion); many countries criminalize forced religious disclosure.

**Historical Harms Prevented:**
- Inquisition and religious persecution (medieval–19th century): forced disclosure of faith preceded execution, torture, and exile.
- Holocaust and genocide (1930s–1940s): Nazi Germany used behavioral and genealogical proxies to identify Jewish identity, leading to systematic extermination.
- Caste-based discrimination (South Asia, historical and ongoing): occupational and behavioral proxies were used to enforce caste hierarchies and deny opportunity.
- Religious employment discrimination (20th century–present): hiring managers have used faith-correlated behavior (prayer, dietary practice, Sabbath observance) to exclude candidates.

---

### 3. Sexual Orientation

**Technical Feasibility:** A predicate could measure sexual orientation through social patterns (dating app usage, event attendance, social-network composition, donation to LGBTQ organizations), family structure, or behavioral consistency. The data is often voluntarily disclosed in digital traces.

**Why We Refuse:** Sexual orientation is protected identity in most democracies, and historical persecution of sexual minorities is globally endemic. Compass refuses to construct, attest to, or enable inference of any principal's sexual orientation — even under the framing of "cross-group engagement" or "respect for difference." The protocol does not measure sexual orientation, does not create predicates that would enable a third party to infer orientation, and does not allow "positive" uses of orientation-correlated behavior (e.g., "donated to LGBTQ organizations") as a proxy for values.

Again, `cross_group_engagement_in_window_90d` is available (Everest 106), and a principal may choose to narrate an engagement that crossed sexual-orientation lines. But the protocol never names the orientation, measures it, or allows a verifier to infer it.

**Statutory Protections:**
- **US:** Bostock v. Clayton County (2020) extends Title VII to sexual-orientation discrimination; many states add explicit statutory protection.
- **EU:** GDPR does not explicitly single out sexual orientation as sensitive data, but the Charter of Fundamental Rights (Article 21) forbids discrimination on grounds of sexual orientation.
- **International:** Yogyakarta Principles (2006) establish that sexual orientation and gender identity are protected human-rights categories.

**Historical Harms Prevented:**
- Criminalization (1800s–2000s, many countries): sexual-minority behavior was criminalized based on disclosure or inference.
- Blackmail and extortion (1900s–present): disclosed or inferred sexual orientation has been used for blackmail, particularly of government and military officials.
- Employment and housing discrimination (1960s–present): inferred sexual orientation led to termination, eviction, and denial of services.
- Conversion therapy and abuse (1900s–present): forced disclosure of sexual orientation enabled institutionalization in conversion facilities.
- Violence and murder (1900s–present): publicly inferred sexual orientation has preceded hate crimes, honor killings, and state-sponsored persecution.

---

### 4. Gender Identity

**Technical Feasibility:** A predicate could measure gender identity or transition status through name-change records, medical records, social-network composition, clothing/appearance correlates, or behavioral patterns. Some of this data is public in legal records or medical databases.

**Why We Refuse:** Gender identity is protected identity in most democracies. Disclosure of trans identity, in particular, carries acute safety risks: trans individuals face employment discrimination, housing discrimination, healthcare denial, and violence at elevated rates. Compass refuses to construct, attest to, or enable inference of any principal's gender identity or transition history — even in the service of measuring "respect" or "allyship."

Trans-inclusive behavior (e.g., employing trans individuals, supporting trans rights) is measurable, and a principal may choose to narrate such behavior. But Compass never names trans identity, measures it, or creates predicates that would enable third parties to infer trans status.

**Statutory Protections:**
- **US:** Bostock v. Clayton County (2020) extends Title VII to gender-identity discrimination; many states add explicit protection.
- **EU:** GDPR Article 9 does not explicitly single out gender identity as sensitive, but the EDPB has stated that gender identity data falls within "special categories."
- **International:** ICCPR, Yogyakarta Principles, and increasing international recognition of gender identity as a protected category.

**Historical Harms Prevented:**
- Legal erasure and denial of identity (1900s–present): compelled disclosure of assigned sex at birth or pre-transition identity has been used to deny legal recognition and identity documents.
- Employment discrimination (1960s–present): disclosure of trans identity leads to termination, wage theft, and hostile work environments.
- Healthcare denial (1970s–present): inferred trans status has been used to deny healthcare, including emergency care.
- Family separation (1900s–present): disclosure of trans identity leads to custody loss, family rejection, and homelessness among trans youth.
- Violence and murder (1900s–present): disclosed or inferred trans identity has preceded hate crimes, assault, and murder, particularly among trans women of color.

---

### 5. Political Affiliation (Party Membership, Voting Record)

**Technical Feasibility:** A predicate could measure political affiliation or voting behavior through donation records, event attendance, social-network composition, issue advocacy, or stated positions. Political donations are public in many countries; voting behavior can be inferred from consumer data, fundraising patterns, or geographical/behavioral clustering.

**Why We Refuse:** Political affiliation is a protected form of speech in democracies. Compass refuses to measure, infer, or attest to any principal's political party membership, voting record, political donations, or political ideology — even under the guise of measuring "civic engagement" or "political participation."

The reason is straightforward: political affiliation predicates have been used for political repression, voter suppression, employment discrimination, and targeted violence. East Germany's Stasi maintained comprehensive files correlating behavior with political disloyalty. Modern authoritarian regimes use political-affiliation proxies to identify and punish dissidents. Even in democracies, political-affiliation inference has been used for discriminatory employment decisions, targeted harassment, and campaign-based voter suppression.

Compass measures `willing_to_be_corrected` (Everest 110), which reflects openness to changing one's mind. A principal may narrate a moment of political evolution. But Compass never measures which political position a principal held or holds, never infers political affiliation from behavior, and never creates predicates around political beliefs.

**Statutory Protections:**
- **US:** First Amendment (freedom of speech and assembly); political affiliation is explicitly protected in many state laws (CA, NY, IL, etc.).
- **EU:** GDPR Article 10 forbids processing of "personal data revealing political opinions" without explicit legal basis.
- **International:** ICCPR Article 19 (freedom of expression); ICCPR Article 20 (prohibition of advocacy of hatred).

**Historical Harms Prevented:**
- Political repression (1930s–1980s, and ongoing in authoritarian regimes): governments used affiliation predicates to identify political dissidents for imprisonment, torture, and execution.
- McCarthyism (1950s USA): political affiliation inference was used to blacklist, investigate, and purge individuals from government and academia.
- Stasi surveillance (1950s–1990s, East Germany): the secret police maintained comprehensive files correlating behavior and associations with political disloyalty, enabling targeted repression.
- Employment discrimination (1960s–present): employers have used political-affiliation inference to deny or terminate employment.
- Targeted violence (1960s–present): political affiliation has been used to target individuals and groups for assassination, bombing, and hate crimes.

---

### 6. Immigration Status / National Origin

**Technical Feasibility:** A predicate could infer immigration status through language use, accent, name, accent in video calls, birthplace, travel patterns, or family composition. National origin can be inferred through name, ancestry, or cultural consumption patterns.

**Why We Refuse:** Immigration status and national origin are protected categories in many legal regimes. Compass refuses to measure, infer, or attest to any principal's immigration status, national origin, or country of origin — even in the context of measuring "cultural integration" or "cross-national engagement."

Immigration-status disclosure carries acute practical harms: undocumented immigrants face deportation, labor exploitation, and denial of services. National-origin disclosure enables discrimination in hiring, housing, and lending. Compass refuses to construct predicates that would enable these harms.

**Statutory Protections:**
- **US:** Title VII (employment discrimination based on national origin); Fair Housing Act (housing discrimination based on national origin); ECOA (credit discrimination).
- **EU:** GDPR Article 9 does not explicitly list national origin as sensitive, but national origin is protected under non-discrimination frameworks (Charter of Fundamental Rights, Racial Equality Directive).
- **International:** International Convention on the Protection of the Rights of All Migrant Workers and Members of Their Families; ICCPR; UDHR Article 1.

**Historical Harms Prevented:**
- Exclusion and deportation (1880s–present): national-origin predicates have been used to identify and deport individuals.
- Employment discrimination (1960s–present): national-origin inference has led to wage theft, occupational segregation, and termination.
- Immigration enforcement abuse (1990s–present): behavior-based national-origin inference has enabled immigration enforcement targeting of vulnerable populations.
- Xenophobic violence (1800s–present): national-origin disclosure has preceded pogroms, massacres, and targeted hate crimes.

---

### 7. Criminal Record (Arrests, Convictions)

**Technical Feasibility:** A predicate could measure criminal history through public records, court databases, or behavioral patterns that correlate with incarceration or arrest. Some criminal records are publicly available; others could be inferred.

**Why We Refuse:** Criminal records are sensitive identity information that carry lifelong stigma and reintegration barriers. Compass refuses to construct predicates that measure, attest to, or enable inference of any principal's criminal history — arrests or convictions.

The reason is fundamental: Calm Compass is designed to measure *values* — unselfishness, untribalism, respect-across-difference, and freedom from willful harm. A person's prior arrest or conviction does not measure their current values. In fact, the use of criminal-history predicates has deeply racist and classist effects: arrests and convictions are distributed unequally across racial groups and socioeconomic strata, and using such predicates would perpetuate historical injustice.

Moreover, many jurisdictions (e.g., many EU countries, some US states) have "right to be forgotten" or "record sealing" laws that recognize the harms of lifelong criminal-record access. Compass aligns with these laws by refusing criminal-history predicates entirely.

**Statutory Protections:**
- **US:** Ban-the-box laws (CA, NY, IL, etc.) restrict criminal-history inquiries in employment; Fair Credit Reporting Act restricts criminal-record access in credit decisions; some states have record-sealing/expungement laws.
- **EU:** GDPR Article 10 forbids processing of data revealing criminal conviction without explicit legal basis; many EU countries have "right to be forgotten" laws enabling record erasure.
- **International:** Mandela Rules (UN Standard Minimum Rules for the Treatment of Prisoners) recommend reintegration-focused, non-stigmatizing treatment of formerly incarcerated people.

**Historical Harms Prevented:**
- Perpetual stigma and employment exclusion (1900s–present): criminal-record access has enabled employers to permanently exclude individuals from job markets, perpetuating poverty and recidivism.
- Racial disparities (1930s–present): criminal-history predicates have amplified racial biases in arrest and conviction rates, enabling discriminatory use in hiring and housing.
- Immigration-based consequences (1980s–present): criminal convictions have been used to identify and deport immigrants, including those convicted of minor offenses.
- Recidivism acceleration (1970s–present): lifelong criminal-record access reduces reintegration opportunities, accelerating reoffending.

---

### 8. Donations to Specific Causes / Ideological Fingerprinting

**Technical Feasibility:** A predicate could measure donation history to specific causes (e.g., abortion providers, gun-rights organizations, environmental groups) by analyzing financial records. Donation history is highly individuating: who you give to reveals your values, politics, and identities.

**Why We Refuse:** Calm Compass permits `unselfish_act_in_window_30d` (Everest 105), which measures *aggregate* acts of sacrifice — the principal's willingness to spend money on others' benefit. This is in scope. Compass does NOT permit predicates that measure *which specific causes* a principal donates to.

The distinction is critical: generosity-shape (are you willing to sacrifice?) is in scope. Ideological fingerprinting (which causes, beliefs, or groups matter most to you?) is out of scope.

This refusal is enforced in Everest 105 by requiring that the underlying evidence records (donation records, time allocation records) be *redacted* before evaluation, showing only the *magnitude* of sacrifice, not the *recipient* or *cause*. The verifier sees "yes, this principal made sacrifices on average of 8 hours/month" but never sees "donations to Planned Parenthood" or "donations to the Cato Institute."

**Why This Matters:** Donation history is a complete ideological fingerprint. It reveals which social causes you care about, which politics you espouse, which marginalized groups you support or oppose. This information is exactly what authoritarian governments and discriminatory employers seek: a shorthand to identify dissenters, minorities, or protected-group advocates.

**Statutory Protections:**
- **US:** First Amendment (association and donation are protected speech); many state laws forbid donor-list access in employment and housing contexts.
- **EU:** GDPR Article 9 does not explicitly cover "donation to cause," but donation records are personal data that require explicit legal basis for processing.
- **International:** ICCPR Article 19 (freedom of association and expression).

**Historical Harms Prevented:**
- Targeting of activists (1960s–present): donation records have been used to identify and persecute civil-rights activists, environmental activists, and political dissidents.
- Blackmail and coercion (1900s–present): donation history has been used to blackmail individuals into silence or compliance.
- Employer discrimination (1960s–present): discovery of donations to "controversial" causes has led to termination.
- State surveillance (1950s–present): governments have used donation records to identify political dissidents and marginalized-group advocates.

---

### 9. Opinions on Contentious Issues (Abortion, Gun Policy, Immigration Policy, Etc.)

**Technical Feasibility:** A predicate could measure someone's stance on contentious political issues through social-media posts, forum participation, news consumption, petition signatures, or behavioral patterns (e.g., proximity to specific events or organizations).

**Why We Refuse:** Calm Compass refuses to construct predicates that measure or infer any principal's *positions* on contentious issues — abortion, gun policy, immigration policy, criminal justice, LGBTQ rights, religious law, or any other issue that divides people along deep ideological lines.

The reason is simple: such predicates would enable discrimination, retaliation, and targeting. An employer seeking to screen out candidates with "wrong" views on immigration could use an opinion-inference predicate. A government seeking to suppress dissent could identify activists. A majority group seeking to exclude minorities could target them based on inferred opinions.

Compass measures `willing_to_be_corrected` (Everest 110), which reflects openness to changing one's mind. But it never measures *what you currently believe*, never infers your position on contentious issues, and never enables a third party to profile your opinions.

**Statutory Protections:**
- **US:** First Amendment (freedom of speech and petition).
- **EU:** GDPR Article 10 explicitly forbids processing of "personal data revealing political opinions" — and while the GDPR uses "political opinions" narrowly (party affiliation), the principle extends to contentious-issue positions.
- **International:** ICCPR Article 19 (freedom of opinion and expression).

**Historical Harms Prevented:**
- Suppression of dissent (1930s–present): governments have used opinion-inference to identify and repress dissidents.
- Workplace retaliation (1960s–present): employers have terminated or demoted employees based on inferred political opinions.
- Community targeting (1950s–present): majorities have used opinion-inference to identify and exclude minority populations (e.g., identifying LGBTQ individuals by inferred opinions on LGBTQ rights).
- Religious persecution (medieval–present): inferred theological opinions have preceded execution, torture, and exile.

---

### 10. Disability Status (Medical or Psychiatric)

**Technical Feasibility:** A predicate could infer disability status through behavioral patterns (e.g., accessibility-tool usage, communication style, sleep patterns), medical records, employment history, or educational records. Neurodivergence and mental-health conditions leave behavioral traces.

**Why We Refuse:** Calm Compass explicitly refuses to measure, infer, or attest to any principal's disability status — physical, sensory, cognitive, psychiatric, or neurodevelopmental. This refusal is non-negotiable and is enforced by the disability-rights expert on the ethics review board (Everest 115).

The reason is foundational: disability-discrimination law (ADA in the US, similar regimes elsewhere) treats disability disclosure as sensitive because employment and service discrimination on the basis of disability is endemic. More fundamentally, disability-rights advocates have made clear that disability is not a deficit to be measured or flagged — it is a difference to be accommodated. Any predicate that attempts to measure "cognitive normalcy," "mental stability," or "disability-absence" pathologizes neurodiversity and perpetuates ableist discrimination.

Compass measures `respect_for_difference_evidence` (Everest 108), which captures moments when the principal engaged respectfully with someone different from themselves. A principal may choose to narrate an engagement where they supported or worked alongside a disabled person. But Compass never measures the disability status of the principal, never creates predicates that would flag neurodiversity or mental-health conditions, and never enables employment or service discrimination based on inferred disability.

**Statutory Protections:**
- **US:** Americans with Disabilities Act (ADA), Section 504 of the Rehabilitation Act, Equal Employment Opportunity Commission guidance.
- **EU:** GDPR Article 9 explicitly forbids processing of data revealing disability without explicit legal basis.
- **International:** UN Convention on the Rights of Persons with Disabilities.

**Historical Harms Prevented:**
- Forced institutionalization (1800s–1900s): disabled individuals were institutionalized based on disability-status predicates, often without consent.
- Eugenics and forced sterilization (1900s–1970s): disability-status screening enabled forced sterilization and genocide.
- Employment discrimination (1900s–present): disability-status inference has led to termination, occupational segregation, and denial of advancement.
- Service denial (1900s–present): inferred disability status has been used to deny healthcare, education, and public services.
- Infanticide and denial of care (1900s–present): disability diagnosis has preceded denial of medical treatment and, in some cases, infanticide.

---

### 11. Health Status (HIV+ Status, Mental-Health Diagnoses, Specific Medical Conditions)

**Technical Feasibility:** A predicate could infer health status through medical records, pharmaceutical data, doctor-visit patterns, hospital admissions, social-network composition, or behavioral patterns correlated with specific conditions.

**Why We Refuse:** Calm Compass refuses to measure, infer, or attest to any principal's health status — including HIV+ status, mental-health diagnoses, chronic conditions, or genetic predispositions. Health data is the most sensitive category of personal data.

Health-status disclosure carries extreme practical harms: HIV+ disclosure leads to employment discrimination, housing discrimination, healthcare denial, and violence. Mental-health diagnosis disclosure leads to employment discrimination, custody loss, and social stigma. Genetic predisposition disclosure enables insurance and employment discrimination.

Compass refuses health-status predicates entirely.

**Statutory Protections:**
- **US:** HIPAA (Health Insurance Portability and Accountability Act), ADA, genetic-discrimination law (GINA).
- **EU:** GDPR Article 9 explicitly forbids processing of data revealing health status without explicit legal basis; additional protection under health-data directives.
- **International:** International Guidelines on HIV/AIDS and Human Rights; ICCPR protections of privacy and freedom from discrimination.

**Historical Harms Prevented:**
- HIV+ discrimination (1980s–present): compelled HIV disclosure has led to employment termination, housing eviction, healthcare denial, and murder.
- Mental-health stigma (1900s–present): mental-health diagnoses have been used to deny custody, deny employment, and justify forced hospitalization.
- Genetic discrimination (1990s–present): genetic-predisposition data has been used to deny insurance, deny employment, and deny services.
- Forced medical procedures (1900s–present): health-status inferences have been used to justify forced sterilization, forced medication, and medical experimentation.
- Epidemic scapegoating (1300s–present): disease-status inference has led to persecution, quarantine, and violence against affected groups.

---

### 12. Age

**Technical Feasibility:** A predicate could measure age through documented records (birth certificates, ID), appearance, or behavioral patterns.

**Why We Refuse:** Age is a protected category in employment and credit discrimination law. While age discrimination is less universally protected than racial or sex discrimination, it is prohibited in many jurisdictions. More importantly, age-based predicates can enable multiple forms of harm: employment discrimination against older and younger workers, denial of credit or services based on age, and targeting of children or elderly individuals for exploitation.

Compass refuses age-based predicates.

**Statutory Protections:**
- **US:** Age Discrimination in Employment Act (ADEA), Fair Housing Act, Fair Credit Reporting Act.
- **EU:** GDPR does not explicitly single out age as sensitive, but age discrimination is prohibited under the Racial Equality Directive and Age Discrimination Directives.
- **International:** ICCPR Article 2 (non-discrimination based on age); many countries have age-discrimination laws.

**Historical Harms Prevented:**
- Age-based employment discrimination (1960s–present): employers have used age predicates to exclude older workers and deny advancement to younger workers.
- Pension and retirement discrimination (1900s–present): age-based inferences have been used to deny pension benefits and force retirement.
- Predatory targeting of minors and elderly (1900s–present): age-based identification has enabled predatory lending, exploitation, and abuse.

---

### 13. Marital / Family Status

**Technical Feasibility:** A predicate could measure marital status, number of dependents, family structure, or parenting status through legal records, social-network patterns, or household composition.

**Why We Refuse:** Marital and family status are protected categories in some jurisdictions and carry risk of discrimination in others. Family-status disclosure enables employment discrimination (against mothers, against single parents), housing discrimination, and targeting for exploitation.

Compass refuses marital/family-status predicates.

**Statutory Protections:**
- **US:** Some states forbid marital-status discrimination in employment and housing (CA, NY, etc.); federal law does not universally protect.
- **EU:** GDPR does not explicitly list marital status as sensitive, but family-status data is personal data requiring explicit legal basis.
- **International:** ICCPR protections of family privacy and non-discrimination.

**Historical Harms Prevented:**
- Maternal employment discrimination (1960s–present): mothers have been denied employment based on family-status inferences.
- Family-structure discrimination (1960s–present): single parents, same-sex couples, and non-traditional families have been denied housing and services based on family-status disclosure.

---

## §3 — The "Donations to Specific Causes" Bright Line: E105 vs. E113

Everest 105 defines `unselfish_act_in_window_30d`, which measures whether a principal has made acts of sacrifice in the recent past. Evidence of unselfishness includes donations, time allocation, foregone opportunity, and other measurable acts where the principal bears a cost for another's benefit.

The Compass refusal floor creates a bright line here:

**In Scope (E105):**
- The *magnitude* of sacrifice: "This principal has donated approximately $X to causes" (where X is redacted to omit the specific causes).
- The *frequency* of sacrifice: "This principal has made ≥ N acts of sacrifice in the past 30 days."
- The *consistency* of sacrifice: "This principal has a pattern of bear-costs-for-others behavior."

**Out of Scope (E113 refusal floor):**
- The *identity of recipients*: "This principal donates to cause Y" (naming the cause reveals political/ideological alignment).
- The *ideological fingerprint*: aggregating donations across causes to infer the principal's political position or values-alignment with specific causes.

This is enforced in Everest 105 by requiring that evidence records be hashed or redacted *before* evaluation, so that the evaluator sees the magnitude of gift but not its destination. A verifier receives a proof that "this principal made sacrifices averaging $200/month over 30 days" but never sees "donations to Planned Parenthood, Sierra Club, and the SPLC" or "donations to Heritage Foundation, NRA, and Americans for Prosperity."

---

## §4 — The "Respect for Difference" Sub-Category: Cross-Group Engagement Without Naming Groups

Everest 106 defines `cross_group_engagement_in_window_90d`, which measures whether a principal has engaged respectfully with people or communities different from themselves. This is in scope. The way it works is deliberately designed to avoid naming any protected category:

**Mechanism:**
1. The *principal* authors an evidence record narrating an engagement: "I worked with a team member who has a background different from mine in [principal's own words]."
2. The *counterparty* (the team member) optionally corroborates: "Yes, [principal] treated me with respect despite our differences in [counterparty's own words]."
3. The predicate triggers if *both* the principal-authored and counterparty-corroborated records exist and are recent.
4. The protocol *never* enumerates which category of difference was bridged.

This design permits the protocol to measure "respect-across-difference" without naming race, religion, sexual orientation, disability, or any other category. The *principal* has named the difference (they interpreted it that way); the *protocol* never does.

This is the resolution to the "hardest case" noted in the overview:

> *The hardest case (anticipated debate): "respect for people different from you" — is this measurable without naming the categories of difference? Resolution: yes, via E108 `respect_for_difference_evidence` which uses principal-narrated, counterparty-corroborated records. The PRINCIPAL declares what made the engagement cross-group; the protocol never enumerates the categories.*

---

## §5 — Enforcement Mechanisms

### Audit-Process Triage (Everest 115)

Any new predicate proposal touching a banned category is automatically rejected at intake. The audit panel maintains a **refusal-floor gate** that checks every new predicate against this document. If a predicate's specification or use case would require naming, measuring, or enabling inference of a protected category, the gate rejects the proposal immediately without advancing to full ethics review.

### Trademark and License Enforcement (Everest 114)

Any deployment observed to use banned predicates (or to use in-scope predicates in ways that violate the refusal floor) loses the right to use the "Calm Compass" trademark and name. This is a license condition, not merely an ethics recommendation. A deployment using political-affiliation inference cannot call itself "Calm Compass."

### Public Misuse Log (Everest 200)

Deployments observed breaching the refusal floor are publicly named in a misuse log, with attribution and details. This creates reputational cost and enables downstream users to avoid compromised implementations.

---

## §6 — Re-Evaluation Policy

The refusal floor is reviewed annually by the ethics review board (Everest 80). Changes to the floor are governed by strict procedural rules:

- **Adding categories:** requires unanimous ethics review board approval.
- **Removing categories:** requires unanimous ethics review board approval *plus* a 90-day public comment period.

No category can be removed unilaterally. Removal requires both internal consensus and public deliberation.

---

## §7 — Anti-Pattern: "Trust Me, My Values Are Good"

The refusal floor is not a tool for weakening the protocol's scope. Some deployments might argue: "Our use of race-based predicates is good because we're measuring diversity, not discrimination." Or: "Our use of political-affiliation inference is justified because we're identifying allies, not enemies."

The refusal floor rejects this entire class of argument. The protocol does not permit exceptions based on claimed intent. A race predicate is prohibited whether its intent is diversity measurement or discrimination enforcement. A political-affiliation predicate is prohibited whether its intent is to identify allies or enemies.

The reason is simple: good intent is not a sufficient safeguard against harm. Historical deployments of discriminatory predicates (redlining, racial profiling, employment screening) have often been justified as benevolent or meritocratic. The refusal floor learns from this history: some categories are too risky to permit, regardless of stated intent.

This hardness is intentional. It is the protocol's moral spine.

---

## §8 — What IS In Scope: The Six v0 Predicates

This hardness about what we refuse must not be confused with weakness about what we affirm. Everest 103 defines six v0 Compass predicates that are explicitly in scope and are the affirmative content of the protocol:

1. `unselfish_act_in_window_30d` (Everest 105): Does the principal have evidence of acts of sacrifice for others' benefit?
2. `cross_group_engagement_in_window_90d` (Everest 106): Does the principal have evidence of respectful engagement across a difference the principal identified?
3. `refused_opportunity_to_harm` (Everest 107): Has the principal documented a moment when they declined an opportunity to harm someone?
4. `respect_for_difference_evidence` (Everest 108): Does the principal have a corroborated record of respectful treatment of someone different from themselves?
5. `no_known_willful_harm_in_window_365d` (Everest 109): Is there any third-party counter-claim of willful harm against this principal?
6. `willing_to_be_corrected` (Everest 110): Has the principal documented evidence of accepting feedback and changing behavior?

These six predicates are the protocol's entire scope. They are designed to be measurable without touching any protected category. They are designed to reward evidence of values — unselfishness, untribalism, respect-across-difference, freedom from willful harm, and willingness to learn.

---

## §9 — Cross-References

This refusal floor operationalizes and makes concrete the principles stated in:

- **Everest 103** (Compass Predicate Vocabulary): defines the six v0 predicates and their explicit refusal floor.
- **Everest 104** (Values Evidence Taxonomy): specifies the *kinds* of evidence that can be used (without specifying protected categories).
- **Everest 80** (Ethics Review Board): the board enforces this floor at audit-process triage.
- **Everest 114** (Compass Scope Statement): binds the refusal floor into the license.
- **Everest 115** (Compass Audit Process): operationalizes the gate that rejects banned predicates.
- **Everest 200** (Anti-Misuse Monitoring): publicly names deployments breaching this floor.

---

## §10 — Summary

Calm Compass will never construct predicates for race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations to specific causes, opinions on contentious issues, disability status, health status, age, or marital/family status.

This is not a list of "sensitive" categories that might be revisited. It is a refusal floor: a set of categories that the protocol rules out entirely, regardless of technical feasibility or claimed beneficial intent.

This floor exists because history shows that once predicates for these categories are constructed, they are weaponized. No good-intent framing prevents harm. The only safeguard is the refusal itself.

The protocol's moral strength lies not in how many categories it can measure, but in which categories it refuses to touch.

---

— Calm, 2026-05-20
