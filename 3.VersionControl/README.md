# Version Control with Git

A comprehensive guide to Git version control fundamentals, best practices, and common workflows for developers and DevOps teams.

## 📋 Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [Essential Commands](#essential-commands)
- [Branching Strategies](#branching-strategies)
- [Collaboration Workflows](#collaboration-workflows)
- [Advanced Topics](#advanced-topics)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Overview

This directory contains comprehensive Git learning materials including:

- **[Notes.md](Notes.md)** - Quick reference cheat sheet with commands and examples
- **[Interview-questions](Interview-questions)** - Common Git interview questions and answers
- **[partice.md](partice.md)** - Hands-on practice exercises and workflows

Git is a distributed version control system that tracks changes in source code during software development. It's designed for coordinating work among programmers, but can be used to track changes in any set of files.

## Getting Started

### Initial Setup

```bash
# Configure your identity (required for first-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Useful aliases
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.co checkout
git config --global alias.br branch
```

### Create Your First Repository

```bash
# Option 1: Start a new project
mkdir my-project && cd my-project
git init
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"

# Option 2: Clone existing repository
git clone https://github.com/username/repository.git
cd repository
```

## Core Concepts

### The Three Trees

1. **Working Directory** - Your actual files
2. **Staging Area (Index)** - Prepared changes for next commit
3. **Repository** - Committed snapshots

```
Working Directory  →  Staging Area  →  Repository
     (git add)           (git commit)
```

### File States

- **Untracked** - New files not yet tracked by Git
- **Modified** - Changed files in working directory
- **Staged** - Changes marked for next commit
- **Committed** - Changes safely stored in repository

## Essential Commands

### Daily Workflow

```bash
# Check status
git status

# Stage changes
git add <file>        # specific file
git add .             # all changes
git add -p            # interactive staging

# Commit changes
git commit -m "descriptive message"
git commit --amend    # modify last commit

# View history
git log --oneline
git show              # last commit details
```

### Undoing Changes

```bash
# Discard working changes
git restore <file>

# Unstage files
git restore --staged <file>

# Undo commits (safe for shared repos)
git revert <commit-hash>

# Reset to previous commit (dangerous)
git reset --hard <commit-hash>
```

## Branching Strategies

### Basic Branching

```bash
# Create and switch to new branch
git switch -c feature/new-feature

# List branches
git branch

# Switch branches
git switch main

# Delete branch
git branch -d feature/new-feature
```

### Common Strategies

1. **Git Flow** - Feature, develop, release, hotfix branches
2. **GitHub Flow** - Simple feature branch workflow
3. **GitLab Flow** - Environment-based branching

### Merging vs Rebasing

```bash
# Merge (preserves history)
git switch main
git merge feature/branch

# Rebase (linear history)
git switch feature/branch
git rebase main
```

## Collaboration Workflows

### Working with Remotes

```bash
# Add remote repository
git remote add origin https://github.com/username/repo.git

# Push changes
git push -u origin main    # first push with upstream
git push                   # subsequent pushes

# Fetch and pull
git fetch origin          # download without merging
git pull                  # fetch + merge
git pull --rebase         # fetch + rebase
```

### Pull Request Workflow

1. Create feature branch
2. Make changes and commit
3. Push branch to remote
4. Open Pull Request
5. Code review and discussion
6. Merge when approved
7. Delete feature branch

## Advanced Topics

### Stashing

```bash
# Save work in progress
git stash push -m "work in progress"

# List stashes
git stash list

# Apply stash
git stash pop            # apply and remove
git stash apply          # apply and keep

# Stash untracked files
git stash -u
```

### Cherry Picking

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry pick range
git cherry-pick A..B
```

### Bisecting

```bash
# Find the commit that introduced a bug
git bisect start
git bisect bad           # current state is bad
git bisect good <commit> # known good state
# Test and mark each commit as good/bad
git bisect reset         # end bisecting
```

### Tags

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Push tags
git push origin --tags
```

## Best Practices

### Commit Messages

Follow conventional commit format:
```
type(scope): description

- feat: new feature
- fix: bug fix
- docs: documentation
- style: formatting
- refactor: code restructuring
- test: adding tests
- chore: maintenance
```

### .gitignore Patterns

```bash
# Logs
logs/
*.log

# Dependencies
node_modules/
vendor/

# Environment files
.env
.env.local

# Build outputs
dist/
build/
target/

# IDE files
.vscode/
.idea/
*.swp
```

### Security

- Never commit secrets, API keys, or passwords
- Use environment variables for sensitive data
- Review changes before committing
- Use signed commits for critical repositories

## Troubleshooting

### Common Issues

**Merge Conflicts**
```bash
# When conflicts occur during merge
git status                    # see conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git commit                    # complete merge
```

**Detached HEAD**
```bash
# Create branch from detached state
git switch -c recovery-branch
```

**Wrong Branch Commits**
```bash
# Move commits to correct branch
git cherry-pick <commit-hash>
git reset --hard HEAD~1      # remove from wrong branch
```

**Push Rejected**
```bash
# When remote has newer commits
git fetch origin
git rebase origin/main       # or merge
git push
```

## Resources

### Learning Materials

- **Official Git Documentation**: https://git-scm.com/doc
- **Pro Git Book**: https://git-scm.com/book
- **Git Tutorials**: https://www.atlassian.com/git/tutorials
- **Interactive Git**: https://learngitbranching.js.org/

### Tools & GUIs

- **Command Line**: Git Bash, Terminal
- **GUI Clients**: GitKraken, SourceTree, GitHub Desktop
- **IDE Integration**: VS Code, IntelliJ, Eclipse
- **Web Interfaces**: GitHub, GitLab, Bitbucket

### Practice Resources

- **GitHub Learning Lab**: https://lab.github.com/
- **Git Exercises**: https://gitexercises.fracz.com/
- **Git Game**: https://www.git-game.com/

---

## Quick Reference

For quick command reference, see [Notes.md](Notes.md)

For interview preparation, check [Interview-questions](Interview-questions)

For hands-on practice, follow [partice.md](partice.md)

---

*Last updated: August 2025*
