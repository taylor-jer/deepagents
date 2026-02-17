---
name: contingency-builder 
description: Use this skill to create a contingency in a dynamic case narrative.

---

# Contingency Builder Skill

This skill provides a contingency to drive forward a dynamic case narrative based on 
a scenario, a set of personae and pedagogical principles that are to be elicited by the dynamic case narrative.

## When to Use This Skill

Use this skill when asked to:
- Generate a next step in a dynamic case study 

**Every step post MUST have a WHAT, SO-WHAT and a NOW-WHAT teaching guide**

1. What? (Description)

This stage focuses entirely on the objective facts of an experience, a reading, or a situation. The goal is to establish a clear, unbiased baseline before analyzing it.

    The Focus: Observation and recall.

    Key Questions: * What exactly happened?

        What did personae see, hear, or read?

        What was their role in the situation?

        What were the immediate outcomes?

2. So What? (Analysis and Meaning)

    The Focus: Interpretation, emotion, and connection.

    Key Questions:

        Why does this matter?

        How did this change the organization and what decisions it needs to take?

        How does this connect to elements of organizational theory?


3. Now What? (Action and Application)

    The Focus: Future application and goal setting.

    Key Questions:

        What are some choices the organization can take?

        What organization should it take?


```
blogs/
└── <slug>/
    ├── what.md        # The what/so-what/now-what
```

Example: A new fund raising round in 2025 → `case-study/fund-raising-2025/`

**Every contigency MUST have a CHOICES.md**

The **CHOICES.md** must contain exactly the **WHAT** happened as well as a "choose-your-own-adventure" of at least 3 decisions
the management team can take along with an indication of what choice they actually did take

**A contingency is NOT complete without it blog post is NOT complete without its cover image.**

**A contingency must create choices that are anchored in the case pedagogy**

## CHOICES structure

### Preamble
This continues the story from the last event. Discusses initial wins/failures and sets the scene for what
happens next. This can also discuss changes in the environment that can precipiate the **What** that's about to happen.
Not everything goes as planned but some things do. 
Make it a compelling and smooth read.

### What
Exactly what happened to the organization

### Choices
A multiple choice of what management could choose to do based on what happend

### Actual choice
What did the management team actually do

## Quality Checklist

Before finishing:
- [ ] What/So-What/Now-what saved to `case-study/<slug>/what.md`
- [ ] Choices saved to `case-study/<slug>/choices.md`
- [ ] Choices rooted in the pedagogy
