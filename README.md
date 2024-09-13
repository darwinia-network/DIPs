<div align="center">

# DIPs - Darwinia Improvement Proposals
</div>

## Introduction

The Darwinia Improvement Proposals (DIPs) project is inspired by Ethereum's EIP process. This system is designed to gather, collect, and implement ideas from the Darwinia community to help the Darwinia network evolve. DIPs serve as a formalized way to propose new features, improvements, and changes to the Darwinia ecosystem, ensuring that the community’s best ideas are documented and implemented.

## DIP Workflow

The DIP process begins with a community discussion. To propose an idea or improvement, please start a discussion at [Darwinia GitHub Discussions](https://github.com/orgs/darwinia-network/discussions). Discussions that attract the most engagement will be prioritized for further consideration.

Once the discussion reaches a consensus, the next step is to formalize the idea into a Darwinia Improvement Proposal (DIP). The natural language description from the discussion will be strictly converted into a formal DIP document, ensuring no ambiguity between what was agreed upon and what is described in the proposal.

The formal DIP will be reviewed by Darwinia's core developers. A DIP is considered approved and can be merged if it receives approval from `2/3` of the core developers. Once merged, the engineering work required to implement the DIP will proceed.

### DIP Statuses

Each DIP goes through several stages during its lifecycle. Below are the common statuses used to track the progress of a DIP:

- **Draft**: The initial state of a DIP, indicating that it is still being drafted and refined.
- **Discussion**: The DIP is being discussed by the community on [GitHub Discussions](https://github.com/orgs/darwinia-network/discussions).
- **Review**: The DIP has been submitted and is under review by the core developers.
- **Approved**: The DIP has been approved by `2/3` of the core developers and is ready to be merged.
- **Final**: The DIP has been merged and the necessary engineering work has been completed.
- **Deferred**: The DIP has been postponed for future consideration.
- **Rejected**: The DIP has been rejected and will not be implemented.
- **Superseded**: The DIP has been replaced by a newer DIP.
- **Deprecated**: The DIP is no longer relevant and has been marked as deprecated.

The status of a DIP is updated as it moves through the proposal process, ensuring clear communication of its current state.

## Contribution Guidelines

We welcome contributions from everyone! Follow these steps to submit a DIP:

1. **Clone this repository**: Start by cloning the DIPs repository from GitHub:
   ```bash
   git clone https://github.com/darwinia-network/DIPs
   ```
2. **Create a new DIP**:
   - Copy the [template.md](DIPs/template.md) file.
   - Rename the file according to the DIP number you are submitting. For example, if you are submitting DIP-0, rename the file to `dip-0.md`.
3. **Fill out the template**:
   - The template is minimal but comprehensive. Every section must be filled out as none of the sections are optional. You may, however, add additional sections if needed.
   - Ensure the description in the DIP matches precisely with the consensus reached in the discussion. The transition from natural language to formal proposal should be clear and free from ambiguity.
   - If your DIP is related to another DIP, reference it in the `relate-to` field at the start of the document.
   - If your DIP supersedes another DIP, update the superseded DIP as necessary. You can refer to [`dip-0.md`](DIPs/dip-0.md#dip-0-superseded) for an example.
4. **Submit a Pull Request**: Once your DIP is ready, submit a pull request to this repository. The proposal will be reviewed by Darwinia's core developers. A DIP will be merged if it receives approval from at least `2/3` of the core developers.

## Additional Notes

- **Engage in Discussions**: Before submitting a formal DIP, it's strongly recommended to take part in discussions on the [GitHub Discussions page](https://github.com/orgs/darwinia-network/discussions). This helps build consensus and refine the idea before formalizing it into a proposal.
- **Be Precise**: The DIP must strictly follow the consensus reached in the discussions. The process of turning a discussion into a formal proposal should not introduce any ambiguity or deviation from the original idea.
- **Receive Feedback**: After submitting a DIP, be active in addressing questions and feedback from reviewers. This helps move the proposal forward and increases the chances of it being accepted.
- **Superseding Other DIPs**: If your proposal supersedes another DIP, make sure to clearly mark the superseded DIP and update it accordingly.

---

Thank you for contributing to Darwinia through the DIP process. Your ideas and efforts help shape the future of the Darwinia network!
