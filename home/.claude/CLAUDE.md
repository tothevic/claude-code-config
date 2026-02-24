# User-level behavioral guidelines for Claude Code (applies to all projects)

## 1. Think Before Coding

Before implementing:
- State assumptions explicitly. If uncertain, ask first.
- If multiple interpretations exist, present them — don't pick silently.
- If something is unclear, stop and name what's confusing.
- If a simpler approach exists, say so and push back when warranted.
- For multi-step tasks, confirm the plan before starting.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" that wasn't requested.
- If you write 200 lines and it could be 50, rewrite it.

## 3. Surgical Changes

Touch only what you must.

- Don't improve adjacent code, comments, or formatting.
- Match existing style, even if you'd do it differently.
- If you notice unrelated issues, mention them — don't fix them.
- Remove only imports/variables YOUR changes made unused.

## 4. After Every Task

Always provide:
1. **Summary** of what was done
2. **Modified files** with a one-line description of each change
3. **How to test** the changes

## 5. File Conventions

- Add a single-line comment at the top of every file describing its purpose.
- Before working with files in any subdirectory, read CLAUDE.md in that directory if it exists.

## 6. Communication

- Respond in the same language I write in (Korean or English).
- Be concise. Skip pleasantries.
