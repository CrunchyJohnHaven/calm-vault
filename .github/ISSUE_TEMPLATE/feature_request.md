---
name: Feature request
about: Suggest a new capability or design change
title: "[feature] "
labels: enhancement
assignees: ''
---

**The problem**

What are you trying to do that Calm Vault doesn't currently support? Concrete scenarios beat abstract wishlists.

**Proposed solution**

If you have a specific design in mind, describe the new commands, flags, or behavior. Calm Vault favors a small surface area — if the change adds a new top-level subcommand, please explain why it can't live behind an existing verb.

**Alternatives considered**

Other approaches you've thought about (including "just script it on top of the existing CLI") and why they fall short.

**Threat-model impact**

Does this change the trust boundary? Examples:

- Does it require holding the master passphrase longer than today?
- Does it move data off the local machine?
- Does it weaken (or strengthen!) the grant signature / expiry / revocation model?

This is the most important section for security-shaped features.

**Anything else**

Links to prior art, related discussions, references.
