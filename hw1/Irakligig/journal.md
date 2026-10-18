Pattern Journal · Irakligig

Week 1 · Date not provided

Pattern: Context as Budget

Where I used it: When working with an AI assistant on a coding task, I can give it too much information or leave out details that matter. The useful part of this pattern is choosing what the AI needs before asking it to write code. A short description of the goal, the relevant files, and the expected result can be more useful than a long prompt with unrelated details.

What I'd do differently: I would explain the task and its limits first, then add more context only when the AI needs it.

Week 2 · Date not provided

Pattern: Spec to Ship

Where I used it: For my Python Club Events Lookup, I wrote the spec and golden questions before asking Claude to build the code. I ran the tests myself, and all 11 passed. I also broke the code on purpose to check that a test could fail. This showed me that getting a working result is not enough. I need a way to check whether the result does what I asked for.

What I'd do differently: I would include more edge cases in my golden questions before asking Claude to write the code.

Week 3 · Date not provided

Pattern: Uncertainty-Aware UX

Where I used it: In a multimodal AI task, the model may receive information from more than one type of input, such as text and images. The important thing is that the app should not act completely certain when the input is unclear. It should make uncertainty visible instead of giving an answer that sounds correct but may be wrong.

What I'd do differently: I would test unclear or incomplete inputs, not just examples where the answer is obvious. I would also check how the app responds when it cannot interpret an input properly.

Week 4 · Date not provided

Pattern: Grounded Generation

Where I used it: For a document-based question-answering app, I would want answers to come from the documents the app can access. Citations would help me check where an answer came from. If the documents do not contain the answer, the app should say that instead of making something up. A golden set would help me check these behaviors consistently.

What I'd do differently: I would include questions whose answers are missing from the documents and verify that the app refuses to guess. I would also check whether the citations support the actual answers.
