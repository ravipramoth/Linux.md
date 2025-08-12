# Git notes (updated: 2025-08-12)

## Quick setup (first time)
- Identity
  - git config --global user.name "Your Name"
  - git config --global user.email "you@example.com"
- Defaults
  - git config --global init.defaultBranch main
  - git config --global core.autocrlf true
  - git config --global pull.rebase false
- Helpful aliases
  - git config --global alias.lg "log --oneline --graph --decorate --all"
  - git config --global alias.st "status -sb"
- Verify: git config --list

## Create or clone
- git init
- git clone <repo-url>

## File lifecycle
- git status (or: git status -s)
- git add <file>  |  git add .
- git commit -m "message"
- git log --oneline --graph --decorate --all
- git show
- Diff working vs index: git diff
- Diff staged vs HEAD: git diff --staged
- Diff commits/path: git diff <A> <B> -- <path>

## Branches
- List: git branch
- Create+switch: git switch -c feature/x   (or: git checkout -b feature/x)
- Switch: git switch feature/x
- Rename: git branch -m new-name
- Delete: git branch -d old-branch  (or: -D to force)

## Merge
- Update main and merge:
  - git switch main
  - git merge feature/x
- Keep merge commit: git merge --no-ff feature/x
- Fast-forward only: git merge --ff-only feature/x
- Resolve conflicts: edit -> git add -> git commit
- Abort merge: git merge --abort

## Rebase
- Rebase feature on latest main:
  - git switch feature/x
  - git fetch origin
  - git rebase origin/main
- Conflicts: fix -> git add <file> -> git rebase --continue
- Abort: git rebase --abort
- Interactive squash/reword: git rebase -i HEAD~N

## Stash (WIP)
- Save: git stash push -m "wip: msg"
- Include untracked: git stash push -u -m "wip: msg"
- Keep index (don’t stash staged): git stash push --keep-index -m "wip"
- List stashes: git stash list
- Apply vs pop: git stash apply  |  git stash pop
- Drop specific: git stash drop stash@{n}
- Partial/interactive: git stash -p
- From stash to branch: git stash branch fix-branch stash@{0}

## Tags
- Lightweight: git tag v1.0.0
- Annotated: git tag -a v1.0.0 -m "First release"
- Signed: git tag -s v1.0.0 -m "First release"
- List: git tag --list
- Push: git push origin v1.0.0  |  git push origin --tags
- Delete: git tag -d v1.0.0  |  git push origin :refs/tags/v1.0.0

## Remotes
- Add/list: git remote add origin <url>  |  git remote -v
- First push: git push -u origin main
- Fetch: git fetch origin
- Pull (merge): git pull
- Pull (rebase): git pull --rebase

## Undo/restore
- Unstage: git restore --staged <file>
- Discard file changes: git restore <file>
- Amend last: git commit --amend
- Revert commit: git revert <commit>
- Revert a merge: git revert -m 1 <merge-commit-sha>
- Reset soft/mixed/hard: git reset --soft <c> | git reset <c> | git reset --hard <c>
- Clean untracked: git clean -fd
- Recover with reflog: git reflog

## Bisect (find bad commit)
- git bisect start
- git bisect bad
- git bisect good <good-sha>
- Iterate until first bad commit is found
- git bisect reset

## .gitignore examples
```
logs/
*.log
!keep.me
.DS_Store
Thumbs.db
.vscode/
node_modules/
venv/
dist/
build/
```

## Everyday workflow
```bash
git switch -c feature/add-api
# edit files
git add .
git commit -m "feat: add API client"
git fetch origin
git rebase origin/main
git push -u origin feature/add-api
# after merge
git switch main
git pull --ff-only
git branch -d feature/add-api
```

## Troubleshooting
- Push rejected: git fetch origin; git rebase origin/main; resolve; push
- Detached HEAD: git switch -c rescue
- Restore a file from another branch: git restore -s origin/main -- path/to/file
