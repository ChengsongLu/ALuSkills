---
name: write-weekly-report
description: Write a concise weekly progress report from the current repository's Git commit history. Use when the user asks for a weekly report or a summary of a week's commits.
---

# Write Weekly Report

Summarize what was committed to the repository during the reporting window,
using commit history as the only evidence.

## Determine the window

- Use the user's specified range when given.
- Otherwise start at the most recent previous Friday 18:30 (inclusive) and end
  at the latest commit (inclusive). When today is Friday after 18:30, the start
  is still the previous week's Friday 18:30.
- Interpret times in the user's time zone. Use commits reachable from current
  `HEAD` unless the user specifies another branch or revision; state that baseline.
- If no commit falls in the window, use the requested end or current time and
  report that no commits were found. Never use a last commit before the start
  to produce an inverted range. An unborn branch is an empty history.

## Collect evidence

1. List the hash, date, and title of every commit in the window.
2. When a title is insufficient, inspect that commit's stat or diff as needed.
3. Do not report outcomes that the commit record cannot support. A commit
   does not prove deployment, production availability, or successful validation.
   Do not count merge summaries and their underlying changes twice.

## Write the report

- Merge related commits by feature, module, or topic.
- Keep only the effective conclusion after later evolution. Do not list
  intermediate implementations that were later overwritten or reverted as
  separate achievements.
- Output the covered date range and revision baseline first, then an explicitly numbered list with no
  sub-lists or extra commentary.
- Each item is usually one sentence about a completed capability, workflow
  improvement, or key fix. Unless the user asks for a detailed version, omit
  minor changes and implementation details.
- Write in the language of the user's request.
