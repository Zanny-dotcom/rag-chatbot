# Claude Code Prompt: AI-Assisted Development Playbook

Paste this into Claude Code:

---

I want you to help me create a comprehensive, deeply detailed knowledge base called "The AI-Assisted Development Playbook" — a practitioner's guide to building real software using AI agents, specifically Claude Code.

This is based on MY real experience over the past year. I'm a self-taught solo developer who went from zero coding background (former trucker) to shipping multiple desktop applications using AI-assisted development. I want to document everything I've learned so it becomes a permanent reference and potential content foundation.

## My Background & Stack
- Self-taught, ~1 year of hands-on AI-assisted development
- Primary stack: Python, PySide6/PyQt6, OpenCV
- Main tool: Claude Code on Max 20x plan
- OS: Windows 11 (i5-9600K, RTX 2070)
- Editor: Claude Code via Windows Terminal split panes
- Version control: Git + GitHub (username: Zanny-dotcom)
- Notes: Obsidian

## Projects I've Built (reference these as real examples throughout)
- **Sapphire** — Macro recorder with pixel tracking, crop region capture, window-anchored coordinates
- **WhisperNowV2** — Local speech-to-text desktop app using faster-whisper, Silero VAD, CUDA
- **ColorMacro** — Color-detection-based macro automation (OpenCV, HSV detection, click-through overlays)
- **FloatingBalls** — PyQt6 overlay with draggable teleport buttons (first completed distributable project)
- **RuneLite fork/plugin** — Java-based plugin for an RSPS, first Java project
- **Finnish STT app** — Concept/prototype for commercial Finnish-language speech-to-text product
- **Discord bot** — Two-machine architecture (Mac Mini M4 backend + Windows bot) for game stat lookups

## What I Want Documented (be exhaustive on each section)

### Part 1: The Mental Model
- How to think about AI-assisted development vs traditional coding
- The shift from "learning to code" to "learning to direct AI to code"
- When AI accelerates you vs when it creates debt
- The skill stack that matters: problem decomposition, prompt engineering, architecture thinking, testing/verification
- Why hands-on building beats theory every time
- The real learning curve — what's actually hard and what's surprisingly easy

### Part 2: Claude Code Mastery
- How Claude Code actually works under the hood (context window, token usage, how it reads your codebase)
- The CLAUDE.md system — what it is, how to structure it, what to put in it, real examples from my projects
- SKILL.md patterns — documenting reusable approaches for Claude Code to follow
- Effective prompting patterns for Claude Code specifically (not generic prompt engineering)
- When to start new conversations vs continue existing ones
- How to handle context window limits strategically
- Common failure modes and how to recover from them
- The difference between asking Claude Code to build vs asking it to fix vs asking it to refactor

### Part 3: Multi-Agent Orchestration
- The concept: using multiple Claude Code instances simultaneously
- Windows Terminal split pane setup — how and why
- Git worktree strategy for parallel agent work
- How to divide work between agents effectively
- Coordination patterns — preventing agents from conflicting
- The Workflow Architect meta-system prompt approach
- Orchestration planning prompts — how to plan before you execute
- Real examples of orchestrated sessions from my projects
- When multi-agent helps vs when single-agent is better
- Cost/token considerations with multi-agent

### Part 4: Project Architecture & Patterns
- How to structure a Python desktop app project for AI-assisted development
- File organization patterns that work well with Claude Code
- The role of documentation in AI-assisted codebases
- How to maintain code quality when AI is writing most of the code
- Testing strategies when you're moving fast
- Dependency management and environment setup
- Building distributable applications (PyInstaller, packaging)

### Part 5: The Self-Taught Developer's Edge
- Why non-traditional backgrounds can be an advantage
- Building a portfolio through shipped projects, not credentials
- The gap between "AI can code" and "I shipped a product"
- How to evaluate and verify AI-generated code when you're still learning
- Building real understanding vs just getting code that works
- When to slow down and learn the fundamentals
- The progression: copy-paste → guided building → directing → architecting

### Part 6: Tools, Workflows & Infrastructure
- Git fundamentals for AI-assisted development
- GitHub as portfolio and collaboration tool
- Obsidian for knowledge management alongside development
- Windows Terminal configuration for multi-agent work
- Local AI experimentation (Ollama, faster-whisper, CUDA setup)
- MCP (Model Context Protocol) concepts and how they fit in

### Part 7: From Builder to Professional
- Transitioning from hobby projects to professional development
- How AI-assisted development skills translate to job applications
- Building credibility without a CS degree
- The projects-as-proof approach
- What companies actually care about vs what you think they care about
- The future of AI-assisted development and where to position yourself

## Format Requirements
- Write in first person from my perspective, but polished and authoritative
- Use my real project names and real experiences as examples throughout
- Be specific and actionable, not generic advice
- Include actual prompt examples, actual CLAUDE.md snippets, actual workflow descriptions
- Each section should be thorough enough to stand alone as a reference
- Use markdown formatting optimized for Obsidian
- Target 15,000-25,000 words total — this should be EXHAUSTIVE
- Output as a single markdown file

## Tone
- Direct, no fluff, practical
- Confident but honest about limitations and mistakes
- Written for other developers and aspiring developers, not beginners who need hand-holding
- The voice of someone who's actually done this, not someone theorizing

Start by creating an outline, confirm with me, then write the full document section by section.
